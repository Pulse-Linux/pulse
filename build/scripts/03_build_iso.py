#!/usr/bin/env python3
"""
Pulse Linux ISO Image Builder
Compresses the rootfs into SquashFS, configures GRUB2 bootloader,
and generates the bootable hybrid UEFI/BIOS ISO image using grub-mkrescue.
"""

import os
import sys
import shutil
import hashlib
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BUILD_TOOLS_BIN = REPO_ROOT / "build" / "tools" / "bin"
WORK_DIR = REPO_ROOT / "build" / "work"
ROOTFS_DIR = WORK_DIR / "rootfs"
ISO_TREE = WORK_DIR / "iso_tree"
INITRD_IMG = WORK_DIR / "initrd.img"
RELEASE_DIR = REPO_ROOT / "release"
OUTPUT_ISO = RELEASE_DIR / "pulse-linux-core-amd64.iso"

GRUB_CFG_CONTENT = """set default="0"
set timeout=2

# Serial and Console Terminal configuration
insmod serial
serial --speed=115200 --unit=0 --word=8 --parity=no --stop=1
terminal_input console serial
terminal_output console serial

# Pulse Linux Color Palette: Electric Violet (#7852FF) & Pulse Blue (#00D2FF)
set color_normal=light-gray/black
set color_highlight=white/magenta
set menu_color_normal=cyan/black
set menu_color_highlight=white/blue

echo "Booting Pulse Linux 1.0 (Vanguard)..."

menuentry "Pulse Linux 1.0 (Live AMD64 - Default)" --class pulse --class gnu-linux --class gnu --class os {
    echo "Loading Pulse Linux kernel..."
    linux /live/vmlinuz boot=live console=tty0 console=ttyS0,115200
    echo "Loading Pulse Linux initial ramdisk..."
    initrd /live/initrd.img
}

menuentry "Pulse Linux 1.0 (Live AMD64 - Safe Graphics / Nomodeset)" --class pulse --class gnu-linux {
    echo "Loading Pulse Linux in Safe Graphics Mode..."
    linux /live/vmlinuz boot=live nomodeset console=tty0 console=ttyS0,115200
    initrd /live/initrd.img
}

menuentry "Pulse Linux 1.0 (Live AMD64 - Debug & Verbose Boot)" --class pulse --class gnu-linux {
    echo "Loading Pulse Linux in Verbose Diagnostic Mode..."
    linux /live/vmlinuz boot=live debug verbose console=tty0 console=ttyS0,115200
    initrd /live/initrd.img
}

submenu "Advanced System Options" {
    menuentry "Reboot System" {
        reboot
    }
    menuentry "Power Off System" {
        halt
    }
}
"""

def build_iso():
    print(f"\n{'-'*60}")
    print("  Phase 1: Assembling Pulse Linux Bootable Hybrid ISO")
    print(f"{'-'*60}\n")

    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    live_dir = ISO_TREE / "live"
    live_dir.mkdir(parents=True, exist_ok=True)
    grub_dir = ISO_TREE / "boot" / "grub"
    grub_dir.mkdir(parents=True, exist_ok=True)

    # 1. Compress Rootfs into SquashFS if not already existing
    squashfs_dest = live_dir / "filesystem.squashfs"
    if not squashfs_dest.exists():
        print(f"Compressing rootfs into SquashFS ({squashfs_dest})...")
        cmd = f"mksquashfs '{ROOTFS_DIR}' '{squashfs_dest}' -comp gzip -noappend -all-root -e boot"
        res = subprocess.run(cmd, shell=True)
        if res.returncode != 0:
            raise RuntimeError("Failed generating SquashFS")
        sq_size_mb = squashfs_dest.stat().st_size / (1024 * 1024)
        print(f"  ✓ SquashFS compressed successfully ({sq_size_mb:.2f} MB)")
    else:
        sq_size_mb = squashfs_dest.stat().st_size / (1024 * 1024)
        print(f"  ✓ Reusing existing SquashFS ({sq_size_mb:.2f} MB)")

    # 2. Copy Kernel and Initrd
    vmlinuz_src = next((ROOTFS_DIR / "boot").glob("vmlinuz-*"), None)
    if not vmlinuz_src or not vmlinuz_src.exists():
        raise RuntimeError("vmlinuz kernel binary missing in rootfs/boot")
    
    shutil.copy2(vmlinuz_src, live_dir / "vmlinuz")
    shutil.copy2(INITRD_IMG, live_dir / "initrd.img")
    print(f"  ✓ Kernel ({vmlinuz_src.name}) and Initrd staged into ISO tree.")

    # 3. Write GRUB configuration
    (grub_dir / "grub.cfg").write_text(GRUB_CFG_CONTENT)
    print("  ✓ GRUB2 bootloader menu configuration generated.")

    # 4. Invoke grub-mkrescue to produce Hybrid ISO
    print("Generating hybrid UEFI/BIOS ISO with grub-mkrescue...")
    env = os.environ.copy()
    env["PATH"] = f"{BUILD_TOOLS_BIN}:{env.get('PATH', '')}"

    if OUTPUT_ISO.exists():
        OUTPUT_ISO.unlink()

    i386_pc_dir = REPO_ROOT / "build" / "tools" / "lib" / "grub" / "i386-pc"
    d_flag = f"-d '{i386_pc_dir}'" if i386_pc_dir.exists() else ""
    mkrescue_cmd = (
        f"grub-mkrescue {d_flag} -o '{OUTPUT_ISO}' '{ISO_TREE}' "
        f"-- -volid 'PULSE_CORE'"
    )
    res = subprocess.run(mkrescue_cmd, shell=True, env=env)
    if res.returncode != 0:
        raise RuntimeError("grub-mkrescue failed generating ISO image")

    iso_size_mb = OUTPUT_ISO.stat().st_size / (1024 * 1024)
    print(f"\n[SUCCESS] Bootable ISO produced: {OUTPUT_ISO} ({iso_size_mb:.2f} MB)")

    # 5. Compute SHA256 Checksum
    print("Calculating SHA256 release checksum...")
    h = hashlib.sha256()
    with open(OUTPUT_ISO, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    sha256_val = h.hexdigest()
    
    sha_file = RELEASE_DIR / "SHA256SUMS"
    sha_file.write_text(f"{sha256_val}  {OUTPUT_ISO.name}\n")
    print(f"  SHA256: {sha256_val}")
    print(f"  Checksum written to: {sha_file}\n")

if __name__ == "__main__":
    build_iso()
