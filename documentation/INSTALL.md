# Pulse Linux Installation Guide

"One Operating System. Two Worlds. Unlimited Possibilities."

This guide explains how to write the Pulse Linux ISO image to a USB installation drive and install it on physical or virtual hardware.

---

## 1. System Requirements

### Minimum Requirements (Pulse Core)
- **CPU**: 64-bit x86 dual-core processor (1.6 GHz+)
- **RAM**: 2 GB RAM
- **Storage**: 20 GB free disk space
- **Display**: 1024x768 resolution

### Recommended Requirements (Developer & Security Workstations)
- **CPU**: 64-bit quad-core processor (Intel Core i5/i7/i9 or AMD Ryzen 5/7/9)
- **RAM**: 8 GB to 16 GB+ RAM
- **Storage**: 64 GB+ NVMe or SATA SSD
- **Virtualization**: Hardware VT-x / AMD-V enabled in BIOS/UEFI
- **Display**: 1920x1080 (Full HD) or 4K with HiDPI support

---

## 2. Preparing the Installation Media

### Writing to USB on Linux
Insert a USB drive (minimum 4 GB) and verify its device identifier (`lsblk`):
```bash
sudo dd if=release/pulse-linux-core-amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync
```
*(Replace `/dev/sdX` with your target USB drive, NOT a partition like `/dev/sdX1`)*

### Writing to USB on Windows / macOS
- **BalenaEtcher**: Open the ISO, select target USB drive, and flash.
- **Rufus (Windows)**: Select the ISO in "DD Image mode".

---

## 3. Booting the Live Environment

1. Insert the installation USB into the computer.
2. Power on the machine and access the boot menu (commonly `F12`, `F11`, `F10`, or `Esc`).
3. Select your USB drive under **UEFI Boot** or **Legacy Boot**.
4. The GRUB2 bootloader will display:
   - **Pulse Linux 1.0 (Live AMD64 - Default)**: Standard live workstation mode.
   - **Pulse Linux 1.0 (Live AMD64 - Safe Graphics)**: For machines requiring `nomodeset` (older Nvidia/AMD GPUs).
   - **Pulse Linux 1.0 (Live AMD64 - Debug Mode)**: Verbose kernel logging.

---

## 4. Live Session & First Steps

The live session automatically logs into the `pulse` user account:
- **Default Username**: `pulse`
- **Default Password**: `pulse`
- **Root Password**: `pulse`

To run diagnostic checks:
```bash
pulse info
pulse doctor
pulse security status
```

---

## 5. Installing to Disk

Pulse Linux includes Calamares for graphical installation and CLI partition utilities for manual configuration.

Features supported during installation:
- **Automatic Partitioning**: Automatically sizes EFI System Partition, root (`/`), and swap.
- **Full-Disk Encryption**: LUKS2 AES-XTS-256 with user passphrase protection.
- **Filesystem Options**: Btrfs (with automated snapshots) or ext4 (maximum compatibility).
- **Profile Bundles**: Core, Developer, Security, or Professional Workstation.
