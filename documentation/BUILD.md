# Building Pulse Linux From Source

"One Operating System. Two Worlds. Unlimited Possibilities."

This document provides complete instructions for reproducibly building Pulse Linux from source.

---

## 1. Prerequisites & Host Requirements

Pulse Linux build scripts execute unprivileged in user space without requiring root or modifying the host operating system.

- **Architecture**: `x86_64` (AMD64)
- **RAM**: Minimum 4 GiB (8 GiB+ recommended)
- **Free Disk Space**: Minimum 10 GiB free space
- **Operating System**: Any modern Linux distribution (Ubuntu 22.04+, Debian 12+, Arch, Fedora)
- **Required Host Binaries**:
  - `xorriso` (ISO 9660 filesystem creation)
  - `mksquashfs` (SquashFS compression utility)
  - `qemu-system-x86_64` (Virtualization testing)
  - `bwrap` (Bubblewrap container isolation)
  - `python3` (Python 3.10+)

---

## 2. Repository Layout

```
pulse-linux/
├── build/
│   ├── Makefile          # Build automation entry point
│   ├── scripts/          # Staging, rootfs, initramfs, and ISO generation scripts
│   ├── tools/bin/        # Staged unprivileged helper binaries (mtools, etc.)
│   ├── cache/            # Cached .deb packages and package indices
│   └── work/             # Intermediate assembly directories (rootfs, iso_tree)
├── release/              # Generated bootable ISO images and SHA256 checksums
└── scripts/pulse-cli/    # Native Pulse Linux CLI utility
```

---

## 3. Quick Build Commands

```bash
cd "/home/kali/pulse linux"

# Step 1: Verify and stage build dependencies
python3 build/scripts/00_setup_toolchain.py

# Step 2: Download base packages and assemble root filesystem
python3 build/scripts/01_build_rootfs.py

# Step 3: Construct live boot initial ramdisk
python3 build/scripts/02_build_initramfs.py

# Step 4: Compress SquashFS and generate hybrid UEFI/BIOS ISO
python3 build/scripts/03_build_iso.py

# Step 5: Test boot in QEMU
./build/scripts/04_test_qemu.sh
```

Or execute via Makefile:
```bash
make all
make test
```

---

## 4. Build Artifacts

Upon build completion, the following artifacts are generated:
- `release/pulse-linux-core-amd64.iso`: Bootable hybrid ISO (UEFI and Legacy BIOS El Torito).
- `release/SHA256SUMS`: Cryptographic SHA256 verification checksum.

---

## 5. Verification & Testing

To test the generated ISO with hardware KVM acceleration:
```bash
qemu-system-x86_64 \
    -enable-kvm \
    -m 2048 \
    -cdrom release/pulse-linux-core-amd64.iso \
    -boot d \
    -vga virtio \
    -serial stdio
```

The system will boot to GRUB, load the Linux kernel and initramfs, mount the live rootfs via overlayfs, and start the interactive Pulse session on `tty1`.
