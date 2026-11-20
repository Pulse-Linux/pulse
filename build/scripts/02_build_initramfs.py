#!/usr/bin/env python3
"""
Pulse Linux Live Initramfs Builder
Constructs the boot initial ramdisk (initrd.img) containing kernel modules,
statically linked busybox utilities, display/DRM drivers, and the Pulse Linux live medium discovery & overlayfs orchestrator.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BUILD_CACHE = REPO_ROOT / "build" / "cache"
WORK_DIR = REPO_ROOT / "build" / "work"
ROOTFS_DIR = WORK_DIR / "rootfs"
INITRD_DIR = WORK_DIR / "initrd_tree"
OUTPUT_INITRD = WORK_DIR / "initrd.img"

TARGET_MODULE_NAMES = [
    # Filesystem & overlay
    "squashfs.ko", "overlay.ko", "isofs.ko", "ext4.ko", "vfat.ko",
    # Block & loop
    "loop.ko", "sr_mod.ko", "cdrom.ko", "sd_mod.ko", "scsi_mod.ko",
    "libahci.ko", "ahci.ko", "libata.ko", "ata_generic.ko", "ata_piix.ko",
    "nvme-core.ko", "nvme.ko", "uas.ko", "usb-storage.ko", "usbcore.ko",
    # Virtualization (QEMU, KVM, VirtualBox)
    "virtio.ko", "virtio_pci.ko", "virtio_pci_modern_dev.ko", "virtio_pci_legacy_dev.ko",
    "virtio_blk.ko", "virtio_ring.ko", "virtio_scsi.ko",
    # Display & DRM graphics drivers (QEMU std, virtio, VirtualBox, QXL)
    "bochs.ko", "virtio-gpu.ko", "vboxvideo.ko", "qxl.ko", "drm.ko", "drm_kms_helper.ko",
    # CRC & Crypto
    "crc32c_generic.ko", "crc32c-intel.ko", "crc32_generic.ko", "crc32-pclmul.ko",
    "crc-t10dif.ko", "crct10dif_common.ko"
]

INIT_SCRIPT = """#!/bin/sh
# Pulse Linux 1.0 (Vanguard) Live Bootloader Init
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

# 1. Mount essential pseudo-filesystems
mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t devtmpfs devtmpfs /dev 2>/dev/null || mount -t tmpfs dev /dev

echo ""
echo " \033[38;2;120;82;255m\033[1m================================================================\033[0m"
echo " \033[38;2;0;210;255m\033[1m   PULSE LINUX 1.0 (VANGUARD) - INITIALIZING LIVE ENVIRONMENT   \033[0m"
echo " \033[38;2;120;82;255m\033[1m================================================================\033[0m"
echo ""

# Populate dev nodes via mdev
mdev -s 2>/dev/null || true

# 2. Load storage, virtualization, and display drivers
echo "[+] Loading storage, virtualization, and display drivers..."
for mod in bochs virtio-gpu vboxvideo qxl isofs squashfs overlay loop cdrom scsi_mod scsi_common sr_mod sd_mod virtio virtio_ring virtio_pci virtio_blk virtio_scsi ahci libahci libata ata_piix nvme; do
    modprobe "$mod" 2>/dev/null || true
done

# Fallback: insmod any remaining staged drivers
for f in $(find /lib/modules -name "*.ko" 2>/dev/null); do
    insmod "$f" 2>/dev/null || true
done

# Re-scan hardware devices
mdev -s 2>/dev/null || true
sleep 1

# 3. Locate live filesystem on CD, USB, or virtual block device
mkdir -p /mnt/medium /mnt/squashfs /mnt/overlay /mnt/work /mnt/root

FOUND=0
echo "[+] Searching for Pulse Linux live medium..."
for attempt in 1 2 3 4 5 6 7 8 9 10; do
    for dev in /dev/sr* /dev/vd* /dev/sd* /dev/nvme*n* /dev/loop*; do
        [ -b "$dev" ] || continue
        if mount -t iso9660 -o ro "$dev" /mnt/medium 2>/dev/null || mount -t ext4 -o ro "$dev" /mnt/medium 2>/dev/null || mount -o ro "$dev" /mnt/medium 2>/dev/null; then
            if [ -f /mnt/medium/live/filesystem.squashfs ]; then
                echo "\033[38;2;46;204;113m[+] Located Pulse Linux live medium on $dev\033[0m"
                FOUND=1
                break 2
            fi
            umount /mnt/medium 2>/dev/null
        fi
    done
    echo "  Waiting for storage devices (attempt $attempt/10)..."
    sleep 1
done

if [ $FOUND -eq 0 ]; then
    echo "\033[38;2;231;76;60m[-] ERROR: Pulse Linux live medium not found!\033[0m"
    echo "Starting emergency maintenance shell..."
    exec /bin/sh
fi

echo "[+] Mounting compressed SquashFS..."
mount -t squashfs -o loop,ro /mnt/medium/live/filesystem.squashfs /mnt/squashfs

echo "[+] Setting up writable tmpfs overlay..."
mount -t tmpfs -o mode=0755 tmpfs /mnt/overlay
mkdir -p /mnt/overlay/upper /mnt/overlay/work
mount -t overlay -o lowerdir=/mnt/squashfs,upperdir=/mnt/overlay/upper,workdir=/mnt/overlay/work overlay /mnt/root

# Retain live medium mount inside target root
mkdir -p /mnt/root/lib/live/mount/medium
mount -n -o move /mnt/medium /mnt/root/lib/live/mount/medium 2>/dev/null || true

# Prepare essential pseudo mounts in target root
mount -t proc /proc /mnt/root/proc 2>/dev/null || true
mount -t sysfs /sys /mnt/root/sys 2>/dev/null || true
mount --bind /dev /mnt/root/dev 2>/dev/null || true

# Unmount initramfs pseudo-filesystems
umount -l /proc 2>/dev/null || true
umount -l /sys 2>/dev/null || true
umount -l /dev 2>/dev/null || true

echo "\033[38;2;0;210;255m[+] Launching Pulse Linux system initialization (systemd)...\033[0m"
exec switch_root /mnt/root /sbin/init
"""

def build_initramfs():
    print(f"\n{'-'*60}")
    print("  Phase 1: Generating Pulse Linux Live Initramfs")
    print(f"{'-'*60}\n")

    if INITRD_DIR.exists():
        shutil.rmtree(INITRD_DIR)
    INITRD_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Create standard directory layout
    for d in ["bin", "sbin", "usr/bin", "usr/sbin", "dev", "proc", "sys", "mnt", "lib/modules/6.1.0-50-amd64", "etc"]:
        (INITRD_DIR / d).mkdir(parents=True, exist_ok=True)

    # 2. Stage Statically-Linked BusyBox
    busybox_src = ROOTFS_DIR / "bin" / "busybox"
    if not busybox_src.exists():
        bb_deb = next(BUILD_CACHE.glob("busybox-static_*.deb"), None)
        if bb_deb:
            tmp_bb = WORK_DIR / "tmp_bb"
            subprocess.run(f"dpkg-deb -x '{bb_deb}' '{tmp_bb}'", shell=True, check=True)
            busybox_src = tmp_bb / "bin" / "busybox"
    
    if not busybox_src or not busybox_src.exists():
        raise RuntimeError("busybox-static binary not found")

    busybox_dest = INITRD_DIR / "bin" / "busybox"
    shutil.copy2(busybox_src, busybox_dest)
    busybox_dest.chmod(0o755)

    # Install RELATIVE applet symlinks to avoid host absolute path leakage
    applets = subprocess.check_output([str(busybox_dest), "--list"]).decode().split()
    for app in applets:
        # Link in /bin/
        link_bin = INITRD_DIR / "bin" / app
        if not link_bin.exists() and not link_bin.is_symlink():
            link_bin.symlink_to("busybox")
        
        # Link in /sbin/
        link_sbin = INITRD_DIR / "sbin" / app
        if not link_sbin.exists() and not link_sbin.is_symlink():
            link_sbin.symlink_to("../bin/busybox")

    # Symlink /usr/bin and /usr/sbin to bin
    shutil.rmtree(INITRD_DIR / "usr" / "bin")
    shutil.rmtree(INITRD_DIR / "usr" / "sbin")
    (INITRD_DIR / "usr" / "bin").symlink_to("../bin")
    (INITRD_DIR / "usr" / "sbin").symlink_to("../bin")

    print(f"  ✓ Staged BusyBox and created {len(applets)} relative applet symlinks.")

    # 3. Stage Kernel Modules & Compute Dependencies
    kmodules_src = ROOTFS_DIR / "lib" / "modules" / "6.1.0-50-amd64"
    if not kmodules_src.exists():
        raise RuntimeError(f"Kernel modules directory missing: {kmodules_src}")

    # Build modules.dep on rootfs if not already present
    dep_file = kmodules_src / "modules.dep"
    if not dep_file.exists():
        subprocess.run(["depmod", "-b", str(ROOTFS_DIR), "6.1.0-50-amd64"], check=True)

    deps = {}
    with open(dep_file) as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            mod, mod_deps = line.split(":", 1)
            mod_name = Path(mod.strip()).name
            dep_list = [Path(d.strip()).name for d in mod_deps.strip().split() if d.strip()]
            deps[mod_name] = dep_list

    resolved_modules = set()
    def resolve(mod_name):
        if mod_name not in resolved_modules:
            resolved_modules.add(mod_name)
            for d in deps.get(mod_name, []):
                resolve(d)

    for m in TARGET_MODULE_NAMES:
        resolve(m)

    kmodules_dest = INITRD_DIR / "lib" / "modules" / "6.1.0-50-amd64"
    copied_count = 0
    for mod_file in kmodules_src.rglob("*.ko"):
        if mod_file.name in resolved_modules:
            rel_dir = mod_file.parent.relative_to(kmodules_src)
            target_dir = kmodules_dest / rel_dir
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(mod_file, target_dir / mod_file.name)
            copied_count += 1

    # Run depmod on the initramfs tree
    subprocess.run(["depmod", "-b", str(INITRD_DIR), "6.1.0-50-amd64"], check=True)
    print(f"  ✓ Staged {copied_count} boot-critical drivers with resolved dependencies.")

    # 4. Write /init orchestrator
    init_file = INITRD_DIR / "init"
    init_file.write_text(INIT_SCRIPT)
    init_file.chmod(0o755)
    print("  ✓ Live overlayfs /init orchestrator written.")

    # 5. Package cpio.gz archive
    print("Compressing initial ramdisk (cpio.gz)...")
    cmd = f"cd '{INITRD_DIR}' && find . | cpio -H newc -o 2>/dev/null | gzip -9 > '{OUTPUT_INITRD}'"
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        raise RuntimeError("Failed packaging initramfs archive")

    initrd_size_mb = OUTPUT_INITRD.stat().st_size / (1024 * 1024)
    print(f"\n[SUCCESS] Pulse Linux live initrd created: {OUTPUT_INITRD} ({initrd_size_mb:.2f} MB)\n")

if __name__ == "__main__":
    build_initramfs()
