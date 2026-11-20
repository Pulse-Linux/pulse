#!/usr/bin/env bash
# Pulse Linux - One-Click QEMU Live & Install Test Launcher
# Launches Pulse Linux GNOME ISO in QEMU with a 20GB virtual hard drive attached.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
ISO_PATH="${REPO_ROOT}/release/pulse-linux-1.0-gnome-amd64.iso"
DISK_PATH="/tmp/pulse-test-disk.qcow2"

echo "=================================================================="
echo "      PULSE LINUX - QEMU LIVE & INSTALLATION TEST LAUNCHER        "
echo "=================================================================="

# Check if ISO exists
if [ ! -f "${ISO_PATH}" ]; then
    echo "[!] ISO not found at ${ISO_PATH}"
    echo "    Looking for alias..."
    if [ -f "${REPO_ROOT}/release/pulse-linux-gnome-amd64.iso" ]; then
        ISO_PATH="${REPO_ROOT}/release/pulse-linux-gnome-amd64.iso"
    else
        echo "[ERROR] ISO file not found! Please run build scripts first."
        exit 1
    fi
fi

# Create virtual disk if not already existing
if [ ! -f "${DISK_PATH}" ]; then
    echo "[*] Creating 20 GB QCOW2 virtual test disk at ${DISK_PATH}..."
    qemu-img create -f qcow2 "${DISK_PATH}" 20G
else
    echo "[*] Using existing virtual disk: ${DISK_PATH}"
fi

# Detect KVM acceleration
KVM_FLAG=""
if [ -e /dev/kvm ] && [ -w /dev/kvm ]; then
    echo "[✓] Hardware KVM acceleration enabled."
    KVM_FLAG="-enable-kvm"
else
    echo "[!] /dev/kvm not writable or missing; running in emulation mode."
fi

# Detect display environment
DISPLAY_OPT="gtk,zoom-to-fit=on"
if [ -z "${DISPLAY:-}" ]; then
    export DISPLAY=":0"
fi

echo "[*] Launching QEMU..."
echo "    - ISO: ${ISO_PATH}"
echo "    - Disk: ${DISK_PATH} (presented as /dev/vda inside VM)"
echo "    - RAM: 4096 MB | Cores: 4"
echo ""
echo "Inside the VM:"
echo "  1. Click 'Install Pulse Linux' on the desktop, or open Terminal and run:"
echo "     sudo pulse-install /dev/vda"
echo "  2. Once installed, close this window and run './scripts/boot_installed_pulse.sh'"
echo "=================================================================="

exec qemu-system-x86_64 \
    -name "Pulse Linux 1.0 (Vanguard) - Installation Test" \
    ${KVM_FLAG} \
    -m 4096 \
    -smp 4 \
    -cpu host \
    -cdrom "${ISO_PATH}" \
    -drive "file=${DISK_PATH},if=virtio,format=qcow2" \
    -boot "menu=on,order=d" \
    -vga std \
    -display "${DISPLAY_OPT}" \
    -device virtio-net-pci,netdev=net0 \
    -netdev user,id=net0 \
    -device intel-hda -device hda-duplex
