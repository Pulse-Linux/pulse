#!/usr/bin/env bash
# Pulse Linux - Boot Installed System from Virtual Disk
# Boots directly from the installed QCOW2 virtual disk image without the ISO.

set -euo pipefail

DISK_PATH="/tmp/pulse-test-disk.qcow2"

echo "=================================================================="
echo "      PULSE LINUX - BOOT INSTALLED VIRTUAL HARD DISK             "
echo "=================================================================="

if [ ! -f "${DISK_PATH}" ]; then
    echo "[ERROR] Virtual hard disk not found at ${DISK_PATH}!"
    echo "        Please run './scripts/test_pulse_qemu.sh' and install Pulse Linux first."
    exit 1
fi

KVM_FLAG=""
if [ -e /dev/kvm ] && [ -w /dev/kvm ]; then
    echo "[✓] Hardware KVM acceleration enabled."
    KVM_FLAG="-enable-kvm"
fi

if [ -z "${DISPLAY:-}" ]; then
    export DISPLAY=":0"
fi

echo "[*] Booting installed Pulse Linux from virtual disk: ${DISK_PATH}"

exec qemu-system-x86_64 \
    -name "Pulse Linux 1.0 (Vanguard) - Installed System" \
    ${KVM_FLAG} \
    -m 4096 \
    -smp 4 \
    -cpu host \
    -drive "file=${DISK_PATH},if=virtio,format=qcow2" \
    -boot "order=c" \
    -vga virtio \
    -display "gtk,zoom-to-fit=on" \
    -device virtio-net-pci,netdev=net0 \
    -netdev user,id=net0 \
    -device intel-hda -device hda-duplex
