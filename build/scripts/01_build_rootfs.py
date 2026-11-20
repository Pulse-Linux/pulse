#!/usr/bin/env python3
"""
Pulse Linux Root Filesystem Builder
Downloads and stages base Debian Bookworm packages, GNOME desktop stack,
and basic apps & utilities: Nautilus, GNOME Terminal, Gedit, GNOME Calculator,
Eye of GNOME, GNOME System Monitor, File Roller, Network Manager, etc.
Injects Pulse Linux OS identity, themes, 4K wallpapers, GDM3 autologin,
and Pulse CLI management tools.
"""

import os
import sys
import gzip
import shutil
import tarfile
import urllib.request
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BUILD_CACHE = REPO_ROOT / "build" / "cache"
WORK_DIR = REPO_ROOT / "build" / "work"
ROOTFS_DIR = WORK_DIR / "rootfs"
PACKAGES_INDEX = BUILD_CACHE / "Packages.gz"

DEBIAN_MIRROR = "http://deb.debian.org/debian"

TOP_LEVEL_PACKAGES = [
    # Core system & libc
    "base-files", "base-passwd", "bash", "coreutils", "dash", "debianutils",
    "diffutils", "findutils", "grep", "gzip", "hostname", "init-system-helpers",
    "kmod", "login", "passwd", "procps", "sed", "systemd", "systemd-sysv",
    "tar", "util-linux", "libpam0g", "libpam-modules", "libpam-runtime",
    "libc6", "libcap2", "libselinux1", "libsepol2", "libpcre2-8-0",
    "libsystemd0", "libudev1", "busybox-static", "sudo", "iproute2",
    "e2fsprogs", "udev", "libaudit1", "libcrypt1", "libkmod2", "libzstd1",
    "liblzma5", "libbz2-1.0", "zlib1g", "libgcc-s1", "libblkid1", "libuuid1",
    "libsmartcols1", "libfdisk1", "libmount1", "libcap-ng0", "libncursesw6",
    "libtinfo6", "libpam-modules-bin", "adduser", "debian-archive-keyring",

    # Python 3 minimal stack for Pulse CLI & Tools
    "python3-minimal", "python3", "libpython3.11-minimal", "libpython3.11-stdlib",
    "libexpat1", "libffi8", "libssl3", "libsqlite3-0",

    # Hardware & networking
    "pciutils", "usbutils", "iputils-ping", "net-tools", "curl", "wget",

    # GNOME Core & Session & Display Manager
    "gnome-shell", "gnome-session", "gnome-session-bin", "gdm3",
    "mutter", "gsettings-desktop-schemas", "desktop-file-utils",

    # Basic Apps & Utilities requested
    "nautilus",              # File manager
    "gnome-terminal",        # Terminal emulator
    "gedit",                 # Text editor
    "nano",                  # CLI text editor
    "vim-tiny",              # CLI text editor
    "gnome-calculator",      # Calculator
    "eog",                   # Image viewer
    "gnome-system-monitor",  # System monitor
    "htop",                  # CLI system monitor
    "file-roller",           # Archive manager
    "p7zip-full",            # 7z archives
    "unzip", "zip",          # Zip archives
    "network-manager",       # Network manager
    "network-manager-gnome", # Network applet

    # Display server, fonts & icons
    "xwayland",
    "adwaita-icon-theme", "fonts-cantarell", "fonts-dejavu-core"
]

def load_package_metadata():
    if not PACKAGES_INDEX.exists():
        print(f"Downloading Debian package index from {DEBIAN_MIRROR}...")
        url = f"{DEBIAN_MIRROR}/dists/bookworm/main/binary-amd64/Packages.gz"
        urllib.request.urlretrieve(url, PACKAGES_INDEX)

    pkg_map = {}
    with gzip.open(PACKAGES_INDEX, "rt", encoding="utf-8", errors="ignore") as f:
        current = {}
        for line in f:
            if line.strip() == "":
                p_name = current.get("Package")
                if p_name:
                    pkg_map[p_name] = current
                current = {}
            elif ":" in line:
                k, v = line.split(":", 1)
                current[k.strip()] = v.strip()
    return pkg_map

def resolve_dependencies(pkg_map, root_pkgs):
    def get_deps(pkg_name):
        meta = pkg_map.get(pkg_name)
        if not meta:
            return []
        deps = []
        dep_str = meta.get("Depends", "") + ", " + meta.get("Pre-Depends", "")
        for part in dep_str.split(","):
            part = part.strip()
            if not part:
                continue
            first_alt = part.split("|")[0].strip()
            clean_name = first_alt.split("(")[0].strip()
            if clean_name:
                deps.append(clean_name)
        return deps

    resolved = set()
    to_visit = list(root_pkgs)

    while to_visit:
        curr = to_visit.pop(0)
        if curr in resolved or curr not in pkg_map:
            continue
        resolved.add(curr)
        for d in get_deps(curr):
            if d not in resolved and d in pkg_map:
                to_visit.append(d)

    return sorted(list(resolved))

def download_file(url, dest_path, retries=3):
    if dest_path.exists() and dest_path.stat().st_size > 0:
        return dest_path
    
    tmp_path = dest_path.with_suffix(".tmp")
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "PulseLinuxBuilder/1.0 (+https://pulselinux.org)"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp, open(tmp_path, "wb") as out:
                shutil.copyfileobj(resp, out)
            tmp_path.rename(dest_path)
            return dest_path
        except Exception as e:
            if attempt == retries - 1:
                if tmp_path.exists():
                    tmp_path.unlink()
                raise RuntimeError(f"Failed downloading {url}: {e}")

def download_packages_parallel(pkg_list, pkg_map):
    BUILD_CACHE.mkdir(parents=True, exist_ok=True)
    
    tasks = []
    for pkg in pkg_list:
        meta = pkg_map.get(pkg)
        if not meta:
            continue
        filename = meta.get("Filename")
        if not filename:
            continue
        dest = BUILD_CACHE / Path(filename).name
        url = f"{DEBIAN_MIRROR}/{filename}"
        tasks.append((pkg, url, dest))

    total = len(tasks)
    needed = [t for t in tasks if not (t[2].exists() and t[2].stat().st_size > 0)]
    print(f"Total packages in dependency graph: {total}")
    print(f"Already cached: {total - len(needed)} | Need to download: {len(needed)}")

    if needed:
        print(f"Downloading {len(needed)} packages concurrently (16 workers)...")
        completed = 0
        with ThreadPoolExecutor(max_workers=16) as executor:
            future_to_pkg = {executor.submit(download_file, url, dest): pkg for pkg, url, dest in needed}
            for future in as_completed(future_to_pkg):
                pkg = future_to_pkg[future]
                try:
                    future.result()
                    completed += 1
                    if completed % 50 == 0 or completed == len(needed):
                        print(f"  [{completed}/{len(needed)}] packages downloaded...")
                except Exception as e:
                    print(f"  [ERROR] {pkg}: {e}")
                    raise
        print("  ✓ All package archives retrieved successfully.")

def extract_deb(deb_path, target_dir):
    cmd = f"dpkg-deb -x '{deb_path}' '{target_dir}'"
    res = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Failed extracting {deb_path}: {res.stderr}")

def setup_users_and_groups():
    etc_dir = ROOTFS_DIR / "etc"
    etc_dir.mkdir(parents=True, exist_ok=True)

    # Standard passwd
    passwd_content = """root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
pulse:x:1000:1000:Pulse User:/home/pulse:/bin/bash
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
"""
    (etc_dir / "passwd").write_text(passwd_content)

    # Standard group
    group_content = """root:x:0:
daemon:x:1:
bin:x:2:
sys:x:3:
adm:x:4:pulse
tty:x:5:
disk:x:6:
kmem:x:15:
dialout:x:20:pulse
cdrom:x:24:pulse
sudo:x:27:pulse
audio:x:29:pulse
video:x:44:pulse
plugdev:x:46:pulse
netdev:x:100:pulse
users:x:1000:
pulse:x:1000:
kvm:x:108:pulse
nogroup:x:65534:
"""
    (etc_dir / "group").write_text(group_content)

    # Passwords: 'pulse' encrypted with standard SHA-512 crypt
    pw_hash = "$6$pulse$zeBvplZPe5c/3GLaMbFwjO49psOZIOrfeVLV9Qv6bSL5NwvPH5yyljdU.p4RLhfxwPUZNz3wwYyOaKg7cdhGR/"
    shadow_content = f"""root:{pw_hash}:19700:0:99999:7:::
daemon:*:19700:0:99999:7:::
bin:*:19700:0:99999:7:::
sys:*:19700:0:99999:7:::
sync:*:19700:0:99999:7:::
pulse:{pw_hash}:19700:0:99999:7:::
nobody:*:19700:0:99999:7:::
"""
    shadow_file = etc_dir / "shadow"
    if shadow_file.exists():
        shadow_file.chmod(0o644)
    shadow_file.write_text(shadow_content)
    shadow_file.chmod(0o600)

    # Sudoers configuration
    sudoers_d = etc_dir / "sudoers.d"
    sudoers_d.mkdir(parents=True, exist_ok=True)
    pulse_sudoer = sudoers_d / "pulse"
    if pulse_sudoer.exists():
        pulse_sudoer.chmod(0o644)
    pulse_sudoer.write_text("pulse ALL=(ALL:ALL) NOPASSWD: ALL\n")
    pulse_sudoer.chmod(0o440)

def inject_pulse_system_files():
    etc_dir = ROOTFS_DIR / "etc"
    
    # 1. OS identity
    shutil.copy2(REPO_ROOT / "configurations" / "etc" / "os-release", etc_dir / "os-release")
    shutil.copy2(REPO_ROOT / "configurations" / "etc" / "issue", etc_dir / "issue")
    shutil.copy2(REPO_ROOT / "configurations" / "etc" / "issue.net", etc_dir / "issue.net")
    shutil.copy2(REPO_ROOT / "configurations" / "etc" / "lsb-release", etc_dir / "lsb-release")

    # Pulse configuration
    pulse_cfg_dir = etc_dir / "pulse"
    pulse_cfg_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REPO_ROOT / "configurations" / "etc" / "pulse" / "pulse.conf", pulse_cfg_dir / "pulse.conf")

    # Repository list
    apt_dir = etc_dir / "apt"
    apt_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REPO_ROOT / "repositories" / "conf" / "pulse.list", apt_dir / "sources.list")

    # Hostname & hosts
    (etc_dir / "hostname").write_text("pulse\n")
    (etc_dir / "hosts").write_text("127.0.0.1\tlocalhost\n127.0.1.1\tpulse\n::1\tlocalhost ip6-localhost ip6-loopback\n")

    # 2. Pulse CLI executable
    bin_dir = ROOTFS_DIR / "usr" / "local" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    pulse_bin_dest = bin_dir / "pulse"
    shutil.copy2(REPO_ROOT / "scripts" / "pulse-cli" / "pulse", pulse_bin_dest)
    pulse_bin_dest.chmod(0o755)

    pulse_gui_dest = bin_dir / "pulse-theme-gui"
    shutil.copy2(REPO_ROOT / "scripts" / "pulse-theme-gui" / "pulse-theme-gui", pulse_gui_dest)
    pulse_gui_dest.chmod(0o755)

    # Symlinks in /usr/bin
    usr_bin = ROOTFS_DIR / "usr" / "bin"
    usr_bin.mkdir(parents=True, exist_ok=True)
    for tool in ["pulse", "pulse-theme-gui"]:
        sym = usr_bin / tool
        if sym.exists() or sym.is_symlink():
            sym.unlink()
        sym.symlink_to(f"/usr/local/bin/{tool}")

    # 3. Wallpapers staging
    bg_dir = ROOTFS_DIR / "usr" / "share" / "backgrounds" / "pulse"
    bg_dir.mkdir(parents=True, exist_ok=True)
    for wp in (REPO_ROOT / "branding" / "wallpapers").glob("*.svg"):
        shutil.copy2(wp, bg_dir / wp.name)
    
    # GNOME background properties XML
    gnome_bg_props = ROOTFS_DIR / "usr" / "share" / "gnome-background-properties"
    gnome_bg_props.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REPO_ROOT / "branding" / "wallpapers" / "pulse-wallpapers.xml", gnome_bg_props / "pulse-wallpapers.xml")

    # 4. Themes staging
    themes_dir = ROOTFS_DIR / "usr" / "share" / "themes"
    themes_dir.mkdir(parents=True, exist_ok=True)
    for theme_folder in (REPO_ROOT / "branding" / "themes").iterdir():
        if theme_folder.is_dir() and not theme_folder.name.startswith("."):
            dest_theme = themes_dir / theme_folder.name
            if dest_theme.exists():
                shutil.rmtree(dest_theme)
            shutil.copytree(theme_folder, dest_theme)

    # 5. GNOME GSettings Defaults Override
    glib_schemas_dir = ROOTFS_DIR / "usr" / "share" / "glib-2.0" / "schemas"
    glib_schemas_dir.mkdir(parents=True, exist_ok=True)
    override_content = """[org.gnome.desktop.interface]
gtk-theme='Pulse-Dark'
color-scheme='prefer-dark'
icon-theme='Adwaita'
font-name='Cantarell 11'
monospace-font-name='DejaVu Sans Mono 10'

[org.gnome.desktop.background]
picture-uri='file:///usr/share/backgrounds/pulse/pulse-dark-4k.svg'
picture-uri-dark='file:///usr/share/backgrounds/pulse/pulse-dark-4k.svg'
picture-options='zoom'

[org.gnome.desktop.screensaver]
picture-uri='file:///usr/share/backgrounds/pulse/pulse-dark-4k.svg'

[org.gnome.shell]
favorite-apps=['org.gnome.Nautilus.desktop', 'org.gnome.Terminal.desktop', 'gedit.desktop', 'org.gnome.Calculator.desktop', 'eog.desktop', 'org.gnome.SystemMonitor.desktop', 'org.gnome.FileRoller.desktop', 'pulse-theme.desktop']

[org.gnome.desktop.wm.preferences]
button-layout=':minimize,maximize,close'
"""
    (glib_schemas_dir / "99_pulse-defaults.gschema.override").write_text(override_content)

    # Compile schemas
    if shutil.which("glib-compile-schemas"):
        subprocess.run(["glib-compile-schemas", str(glib_schemas_dir)], check=False)

    # 6. GDM3 Autologin configuration
    gdm3_etc = etc_dir / "gdm3"
    gdm3_etc.mkdir(parents=True, exist_ok=True)
    daemon_conf = """[daemon]
AutomaticLoginEnable = true
AutomaticLogin = pulse
WaylandEnable = true

[security]

[xdmcp]

[chooser]

[debug]
"""
    (gdm3_etc / "daemon.conf").write_text(daemon_conf)

    # PAM autologin configuration
    pam_dir = etc_dir / "pam.d"
    pam_dir.mkdir(parents=True, exist_ok=True)
    pam_autologin = """auth sufficient pam_permit.so
account sufficient pam_permit.so
password sufficient pam_permit.so
session sufficient pam_permit.so
"""
    (pam_dir / "gdm-autologin").write_text(pam_autologin)
    (pam_dir / "gdm-password").write_text(pam_autologin)

    # Default systemd target: graphical.target
    systemd_system = etc_dir / "systemd" / "system"
    systemd_system.mkdir(parents=True, exist_ok=True)
    default_target = systemd_system / "default.target"
    if default_target.exists() or default_target.is_symlink():
        default_target.unlink()
    default_target.symlink_to("/lib/systemd/system/graphical.target")

    # 7. Desktop launchers on /usr/share/applications and /home/pulse/Desktop
    apps_dir = ROOTFS_DIR / "usr" / "share" / "applications"
    apps_dir.mkdir(parents=True, exist_ok=True)
    user_desktop = ROOTFS_DIR / "home" / "pulse" / "Desktop"
    user_desktop.mkdir(parents=True, exist_ok=True)

    for desktop_file in (REPO_ROOT / "desktop" / "applications").glob("*.desktop"):
        shutil.copy2(desktop_file, apps_dir / desktop_file.name)
        shutil.copy2(desktop_file, user_desktop / desktop_file.name)
        (user_desktop / desktop_file.name).chmod(0o755)

    if shutil.which("update-desktop-database"):
        subprocess.run(["update-desktop-database", str(apps_dir)], check=False)

    # 8. User profile & .bashrc
    home_pulse = ROOTFS_DIR / "home" / "pulse"
    home_pulse.mkdir(parents=True, exist_ok=True)
    bashrc_content = """# Pulse Linux User Session
if [ -f /etc/bash.bashrc ]; then
    . /etc/bash.bashrc
fi

# Print Pulse System Welcome
pulse info
echo -e "\\033[1;36mType \\033[1;35mpulse doctor\\033[1;36m to run diagnostics, \\033[1;35mpulse theme\\033[1;36m to switch themes, or \\033[1;35mpulse --help\\033[1;36m for options.\\033[0m\\n"

PS1='\\[\\033[38;2;120;82;255m\\]\\u@\\h\\[\\033[0m\\]:\\[\\033[38;2;0;210;255m\\]\\w\\[\\033[0m\\]\\$ '
"""
    (home_pulse / ".bashrc").write_text(bashrc_content)

    # Fstab
    (etc_dir / "fstab").write_text("""# Pulse Linux Live Filesystem
overlay / overlay defaults 0 0
tmpfs /tmp tmpfs defaults,nosuid,nodev 0 0
""")

def build_rootfs():
    print(f"\n{'-'*60}")
    print("  Pulse Linux: Building Full Root Filesystem (GNOME Edition)")
    print(f"{'-'*60}\n")

    ROOTFS_DIR.mkdir(parents=True, exist_ok=True)
    pkg_map = load_package_metadata()

    # 1. Resolve full dependency closure
    print("Resolving complete package dependency tree...")
    resolved_packages = resolve_dependencies(pkg_map, TOP_LEVEL_PACKAGES)
    print(f"Resolved {len(resolved_packages)} total packages for GNOME & Utilities stack.")

    # 2. Download missing packages in parallel
    download_packages_parallel(resolved_packages, pkg_map)

    # 3. Extract all deb packages into rootfs
    print("\nExtracting packages into target rootfs...")
    for idx, pkg in enumerate(resolved_packages, 1):
        meta = pkg_map.get(pkg)
        if not meta:
            continue
        filename = meta.get("Filename")
        if not filename:
            continue
        deb_file = BUILD_CACHE / Path(filename).name
        if deb_file.exists():
            extract_deb(deb_file, ROOTFS_DIR)
        if idx % 75 == 0 or idx == len(resolved_packages):
            print(f"  [{idx}/{len(resolved_packages)}] packages staged...")
    print("  ✓ All packages extracted into rootfs.")

    # 4. Extract Kernel and Modules
    kernel_deb = BUILD_CACHE / "linux-image-6.1.0-50-amd64.deb"
    if not kernel_deb.exists():
        k_meta = pkg_map.get("linux-image-6.1.0-50-amd64")
        if not k_meta:
            raise RuntimeError("linux-image-6.1.0-50-amd64 metadata not found")
        kernel_deb = download_file(f"{DEBIAN_MIRROR}/{k_meta['Filename']}", BUILD_CACHE / Path(k_meta['Filename']).name)
    
    print("Staging Linux kernel and drivers...")
    extract_deb(kernel_deb, ROOTFS_DIR)
    print("  ✓ Linux kernel 6.1.0-50-amd64 staged.")

    # 5. Extract Live-Boot
    for lb_pkg in ["live-boot.deb", "live-boot-initramfs-tools.deb"]:
        lb_deb = BUILD_CACHE / lb_pkg
        if lb_deb.exists():
            extract_deb(lb_deb, ROOTFS_DIR)
    print("  ✓ live-boot tools integrated.")

    # 6. Inject Pulse identity, themes, wallpapers & GNOME autologin
    print("Injecting Pulse Linux configurations, GNOME themes, 4K wallpapers and autologin...")
    setup_users_and_groups()
    inject_pulse_system_files()

    # Create standard mount points
    for mnt in ["proc", "sys", "dev", "run", "tmp", "root", "media", "mnt"]:
        (ROOTFS_DIR / mnt).mkdir(exist_ok=True)

    print("\n[SUCCESS] Pulse Linux GNOME root filesystem assembled at:")
    print(f"  {ROOTFS_DIR}\n")

if __name__ == "__main__":
    build_rootfs()
