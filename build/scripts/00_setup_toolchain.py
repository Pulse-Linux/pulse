#!/usr/bin/env python3
"""
Pulse Linux Toolchain Setup
Ensures all required build dependencies and unprivileged tools are staged.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BUILD_TOOLS_BIN = REPO_ROOT / "build" / "tools" / "bin"
BUILD_CACHE = REPO_ROOT / "build" / "cache"

def run(cmd, check=True):
    print(f"[CMD] {cmd}")
    res = subprocess.run(cmd, shell=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed with code {res.returncode}: {cmd}")
    return res.returncode

def ensure_toolchain():
    BUILD_TOOLS_BIN.mkdir(parents=True, exist_ok=True)
    BUILD_CACHE.mkdir(parents=True, exist_ok=True)

    print("Checking build environment dependencies...")
    required_host_tools = ["xorriso", "mksquashfs", "qemu-system-x86_64", "bwrap", "dpkg-deb"]
    for tool in required_host_tools:
        if not shutil.which(tool):
            raise RuntimeError(f"Missing required host tool: {tool}")
        print(f"  ✓ {tool:<20} found at {shutil.which(tool)}")

    # Check mformat / mcopy (needed for grub-mkrescue UEFI FAT images)
    if not shutil.which("mformat") and not (BUILD_TOOLS_BIN / "mformat").exists():
        print("  Staging unprivileged mtools into build/tools/bin...")
        mtools_deb = BUILD_CACHE / "mtools.deb"
        if not mtools_deb.exists():
            run(f"cd '{BUILD_CACHE}' && apt-get download mtools && mv mtools_*.deb mtools.deb")
        run(f"dpkg-deb -x '{mtools_deb}' '{BUILD_CACHE}/mtools-tmp'")
        for bin_file in (BUILD_CACHE / "mtools-tmp" / "usr" / "bin").glob("*"):
            dest = BUILD_TOOLS_BIN / bin_file.name
            shutil.copy2(bin_file, dest)
            dest.chmod(0o755)
        shutil.rmtree(BUILD_CACHE / "mtools-tmp", ignore_errors=True)
        print("  ✓ Staged mtools binaries into build/tools/bin")
    else:
        print("  ✓ mformat/mtools available")

    # Verify grub-mkrescue
    env = os.environ.copy()
    env["PATH"] = f"{BUILD_TOOLS_BIN}:{env.get('PATH', '')}"
    res = subprocess.run("grub-mkrescue --help", shell=True, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode == 0:
        print("  ✓ grub-mkrescue verified and functional")
    else:
        raise RuntimeError("grub-mkrescue verification failed")

    print("\n[SUCCESS] Build toolchain ready.")

if __name__ == "__main__":
    ensure_toolchain()
