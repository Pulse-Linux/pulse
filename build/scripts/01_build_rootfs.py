#!/usr/bin/env python3
"""
Pulse Linux Root Filesystem Builder
Downloads and stages base Debian Bookworm packages, injects Pulse Linux OS identity,
configures users, PAM, systemd autologin, kernel, and Pulse CLI utilities.
"""

import os
import sys
import gzip
import shutil
import tarfile
import urllib.request
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BUILD_CACHE = REPO_ROOT / "build" / "cache"
WORK_DIR = REPO_ROOT / "build" / "work"
ROOTFS_DIR = WORK_DIR / "rootfs"
PACKAGES_INDEX = BUILD_CACHE / "Packages.gz"

DEBIAN_MIRROR = "http://deb.debian.org/debian"

ESSENTIAL_PACKAGES = [
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
    # Python 3 minimal stack for Pulse CLI
    "python3-minimal", "python3", "libpython3.11-minimal", "libpython3.11-stdlib",
    "libexpat1", "libffi8", "libssl3", "libsqlite3-0",
    # Hardware & networking
    "pciutils", "usbutils", "kmod", "iputils-ping", "net-tools", "curl"
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

def download_package(pkg_name, metadata):
    filename = metadata.get("Filename")
    if not filename:
        raise RuntimeError(f"Missing Filename for package: {pkg_name}")
    dest_path = BUILD_CACHE / Path(filename).name
    if not dest_path.exists():
        url = f"{DEBIAN_MIRROR}/{filename}"
        print(f"  Downloading {pkg_name} ({dest_path.name})...")
        urllib.request.urlretrieve(url, dest_path)
    return dest_path

def extract_deb(deb_path, target_dir):
    # Extract data archive from deb
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
    (etc_dir / "shadow").write_text(shadow_content)
    os.chmod(etc_dir / "shadow", 0o600)

    # Sudoers configuration
    sudoers_d = etc_dir / "sudoers.d"
    sudoers_d.mkdir(parents=True, exist_ok=True)
    (sudoers_d / "pulse").write_text("pulse ALL=(ALL:ALL) NOPASSWD: ALL\n")
    os.chmod(sudoers_d / "pulse", 0o440)

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

    # Symlink /bin/pulse
    usr_bin = ROOTFS_DIR / "usr" / "bin"
    usr_bin.mkdir(parents=True, exist_ok=True)
    if not (usr_bin / "pulse").exists():
        (usr_bin / "pulse").symlink_to("/usr/local/bin/pulse")

    # 3. Systemd autologin on tty1
    systemd_getty_dir = etc_dir / "systemd" / "system" / "getty@tty1.service.d"
    systemd_getty_dir.mkdir(parents=True, exist_ok=True)
    autologin_conf = """[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin pulse --noclear %I $TERM
Type=idle
"""
    (systemd_getty_dir / "override.conf").write_text(autologin_conf)

    # 4. User profile & .bashrc
    home_pulse = ROOTFS_DIR / "home" / "pulse"
    home_pulse.mkdir(parents=True, exist_ok=True)
    bashrc_content = """# Pulse Linux User Session
if [ -f /etc/bash.bashrc ]; then
    . /etc/bash.bashrc
fi

# Print Pulse System Welcome
pulse info
echo -e "\\033[1;36mType \\033[1;35mpulse doctor\\033[1;36m to run diagnostics or \\033[1;35mpulse --help\\033[1;36m for options.\\033[0m\\n"

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
    print("  Phase 1: Generating Pulse Linux Root Filesystem")
    print(f"{'-'*60}\n")

    ROOTFS_DIR.mkdir(parents=True, exist_ok=True)
    pkg_map = load_package_metadata()

    # 1. Download and extract essential base packages
    print("Staging essential base packages...")
    for pkg in ESSENTIAL_PACKAGES:
        if pkg not in pkg_map:
            print(f"  [WARN] Package not in repository index: {pkg}")
            continue
        meta = pkg_map[pkg]
        deb_file = download_package(pkg, meta)
        extract_deb(deb_file, ROOTFS_DIR)
    print("  ✓ Base system packages extracted.")

    # 2. Extract Kernel and Modules
    kernel_deb = BUILD_CACHE / "linux-image-6.1.0-50-amd64.deb"
    if not kernel_deb.exists():
        print("Kernel deb not found in cache. Downloading...")
        k_meta = pkg_map.get("linux-image-6.1.0-50-amd64")
        if not k_meta:
            raise RuntimeError("linux-image-6.1.0-50-amd64 metadata not found")
        kernel_deb = download_package("linux-image-6.1.0-50-amd64", k_meta)
    
    print("Staging Linux kernel and hardware drivers...")
    extract_deb(kernel_deb, ROOTFS_DIR)
    print("  ✓ Linux kernel 6.1.0-50-amd64 staged.")

    # 3. Extract Live-Boot
    for lb_pkg in ["live-boot.deb", "live-boot-initramfs-tools.deb"]:
        lb_deb = BUILD_CACHE / lb_pkg
        if lb_deb.exists():
            extract_deb(lb_deb, ROOTFS_DIR)
    print("  ✓ live-boot tools integrated.")

    # 4. Inject Pulse identity & configurations
    print("Injecting Pulse Linux identity and user profiles...")
    setup_users_and_groups()
    inject_pulse_system_files()

    # Create standard mount points
    for mnt in ["proc", "sys", "dev", "run", "tmp", "root", "media", "mnt"]:
        (ROOTFS_DIR / mnt).mkdir(exist_ok=True)

    print("\n[SUCCESS] Pulse Linux root filesystem assembled at:")
    print(f"  {ROOTFS_DIR}\n")

if __name__ == "__main__":
    build_rootfs()
