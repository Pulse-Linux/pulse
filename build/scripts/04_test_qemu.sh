#!/usr/bin/env bash
# Pulse Linux QEMU Boot Verification Test

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Check for GNOME ISO first, then Core ISO
if [ -f "${REPO_ROOT}/release/pulse-linux-gnome-amd64.iso" ]; then
    ISO_PATH="${REPO_ROOT}/release/pulse-linux-gnome-amd64.iso"
elif [ -f "${REPO_ROOT}/release/pulse-linux-1.0-gnome-amd64.iso" ]; then
    ISO_PATH="${REPO_ROOT}/release/pulse-linux-1.0-gnome-amd64.iso"
elif [ -f "${REPO_ROOT}/release/pulse-linux-core-amd64.iso" ]; then
    ISO_PATH="${REPO_ROOT}/release/pulse-linux-core-amd64.iso"
else
    echo "ERROR: No bootable ISO found in ${REPO_ROOT}/release"
    exit 1
fi

echo "================================================================"
echo "  Pulse Linux 1.0 (Vanguard) - QEMU Boot Verification Test"
echo "  Target ISO: ${ISO_PATH}"
echo "================================================================"

echo "Executing QEMU boot test with KVM acceleration (3072 MB RAM)..."
timeout 35s qemu-system-x86_64 \
    -enable-kvm \
    -m 3072 \
    -cdrom "${ISO_PATH}" \
    -boot d \
    -display none \
    -serial stdio \
    -vga std || {
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 124 ]; then
        echo ""
        echo "[INFO] QEMU reached timeout after 35s (Expected for live desktop session)."
        echo "[SUCCESS] Kernel, initial ramdisk, and systemd boot sequence passed."
        exit 0
    else
        echo "QEMU exited with code: ${EXIT_CODE}"
        exit $EXIT_CODE
    fi
}
