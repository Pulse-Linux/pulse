#!/usr/bin/env python3
"""
Pulse Linux Live Initramfs Builder
Constructs the boot initial ramdisk (initrd.img) containing kernel modules,
busybox utilities, and the Pulse Linux live medium discovery & overlayfs orchestrator.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BUILD_CACHE = REPO_ROOT / "build" / "cache"
WORK_DIR = REPO_ROOT / "build" / "work"
INITRD_DIR = WORK_DIR / "initrd_tree"
OUTPUT_INITRD = WORK_DIR / "initrd.img"

MODULES_TO_COPY = [
    # Filesystem & overlay
    "squashfs.ko", "overlay.ko", "isofs.ko", "ext4.ko", "vfat.ko",
    # Block & loop
    "loop.ko", "sr_mod.ko", "cdrom.ko", "libahci.ko", "ahci.ko",
    "nvme-core.ko", "nvme.ko", "uas.ko", "usb-storage.ko",
    # Virtualization
    "virtio.ko", "virtio_pci.ko", "virtio_blk.ko", "virtio_ring.ko",
    # Crypto / crc helpers
    "crc32c_generic.ko", "crc32c-intel.ko", "crc32_generic.ko", "crc32-pclmul.ko"
]

INIT_SCRIPT = """#!/bin/sh
# Pulse Linux 1.0 (Vanguard) Live Bootloader Init

# Mount essential kernel filesystems
mount -t proc none /proc
mount -t sysfs none /sys
mount -t devtmpfs none /dev

echo ""
echo " \033[38;2;120;82;255m\033[1m================================================================\033[0m"
echo " \033[38;2;0;210;255m\033[1m   PULSE LINUX 1.0 (VANGUARD) - INITIALIZING LIVE ENVIRONMENT   \033[0m"
echo " \033[38;2;120;82;255m\033[1m================================================================\033[0m"
echo ""

mkdir -p /mnt/medium /mnt/squashfs /mnt/overlay /mnt/work /mnt/root

# Insert hardware and filesystem modules
for mod in /lib/modules/*/*.ko /lib/modules/*/*/*.ko /lib/modules/*/*/*/*.ko /lib/modules/*/*/*/*/*.ko; do
    [ -f "$mod" ] && insmod "$mod" 2>/dev/null
done

# Wait for storage devices
sleep 1

# Locate live filesystem on CD, USB, or virtual block device
FOUND=0
for attempt in 1 2 3 4 5 6 7 8 9 10; do
    for dev in /dev/sr* /dev/sd* /dev/vd* /dev/nvme*n* /dev/loop*; do
        [ -e "$dev" ] || continue
        if mount -t iso9660 -o ro "$dev" /mnt/medium 2>/dev/null || mount -o ro "$dev" /mnt/medium 2>/dev/null; then
            if [ -f /mnt/medium/live/filesystem.squashfs ]; then
                echo "\033[38;2;46;204;113m[+] Located Pulse Linux live medium on $dev\033[0m"
                FOUND=1
                break 2
            fi
            umount /mnt/medium 2>/dev/null
        fi
    done
    echo "Waiting for storage devices (attempt $attempt/10)..."
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
mount -t tmpfs -o mode=0755 none /mnt/overlay
mkdir -p /mnt/overlay/upper /mnt/overlay/work
mount -t overlay -o lowerdir=/mnt/squashfs,upperdir=/mnt/overlay/upper,workdir=/mnt/overlay/work overlay /mnt/root

# Retain live medium mount inside target root
mkdir -p /mnt/root/lib/live/mount/medium
mount -n -o move /mnt/medium /mnt/root/lib/live/mount/medium

# Unmount pseudo-filesystems before pivot
umount /proc
umount /sys
umount /dev

echo "\033[38;2;0;210;255m[+] Launching Pulse Linux system initialization...\033[0m"
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
    for d in ["bin", "sbin", "dev", "proc", "sys", "mnt", "lib/modules", "etc"]:
        (INITRD_DIR / d).mkdir(parents=True, exist_ok=True)

    # 2. Stage BusyBox
    rootfs_dir = WORK_DIR / "rootfs"
    busybox_src = rootfs_dir / "bin" / "busybox"
    if not busybox_src.exists():
        # Try finding busybox in cache
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

    # Install busybox symlinks
    subprocess.run(f"cd '{INITRD_DIR}/bin' && ./busybox --install -s .", shell=True, check=True)

    # 3. Stage Kernel Modules
    kmodules_src = rootfs_dir / "lib" / "modules" / "6.1.0-50-amd64"
    if not kmodules_src.exists():
        raise RuntimeError(f"Kernel modules directory missing: {kmodules_src}")

    kmodules_dest = INITRD_DIR / "lib" / "modules" / "6.1.0-50-amd64"
    kmodules_dest.mkdir(parents=True, exist_ok=True)

    copied_count = 0
    for mod_file in kmodules_src.rglob("*.ko"):
        if any(mod_file.name.startswith(t.replace(".ko", "")) for t in MODULES_TO_COPY):
            rel_dir = mod_file.parent.relative_to(kmodules_src)
            target_dir = kmodules_dest / rel_dir
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(mod_file, target_dir / mod_file.name)
            copied_count += 1
    print(f"  ✓ Staged {copied_count} boot-critical kernel drivers.")

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
