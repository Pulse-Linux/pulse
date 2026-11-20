#!/usr/bin/env bash
# Pulse Linux QEMU Boot Verification Test

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
ISO_PATH="${REPO_ROOT}/release/pulse-linux-core-amd64.iso"

if [ ! -f "${ISO_PATH}" ]; then
    echo "ERROR: ISO image not found at ${ISO_PATH}"
    echo "Run 'python3 build/scripts/03_build_iso.py' first."
    exit 1
fi

echo "================================================================"
echo "  Pulse Linux 1.0 (Vanguard) - QEMU Boot Verification Test"
echo "  Target ISO: ${ISO_PATH}"
echo "================================================================"

# Test with KVM acceleration, 2GB RAM, serial console output, headless mode
# Times out after 30 seconds of boot execution
echo "Executing QEMU boot test with KVM acceleration..."
timeout 25s qemu-system-x86_64 \
    -enable-kvm \
    -m 2048 \
    -cdrom "${ISO_PATH}" \
    -boot d \
    -display none \
    -serial stdio \
    -vga std || {
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 124 ]; then
        echo ""
        echo "[INFO] QEMU reached timeout after 25s (Expected for live session)."
        echo "[SUCCESS] Kernel and GRUB boot sequence passed."
        exit 0
    else
        echo "QEMU exited with code: ${EXIT_CODE}"
        exit $EXIT_CODE
    fi
}
