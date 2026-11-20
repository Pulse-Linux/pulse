# Pulse Linux

**"One Operating System. Two Worlds. Unlimited Possibilities."**

Pulse Linux is a modern, production-grade Linux distribution engineered for software developers, systems engineers, cybersecurity professionals, and researchers. Built upon the rock-solid foundation of Debian Stable, Pulse seamlessly bridges the gap between productive development environments and cutting-edge security testing capabilities without compromising system integrity.

---

## Key Highlights

- **Debian Stable Foundation**: Maximum reliability, binary package compatibility (`.deb`, APT), and long-term security maintenance.
- **Dual Workstation Capabilities**:
  - **Developer Environment**: Toolchains for C/C++, Rust, Go, Python, Java, JavaScript/TypeScript, cloud orchestration (Docker, Podman, Kubernetes), and web development.
  - **Cybersecurity Environment**: Rigorously curated penetration testing, digital forensics, reverse engineering, and network auditing toolkits organized by workflow categories with safe isolation.
- **Multi-Format Compatibility**:
  - Native Debian packages (`.deb`) and APT repositories
  - Sandboxed Flatpak and AppImage applications
  - Android application support via Waydroid
  - Windows application compatibility via Wine, Bottles, and Proton
- **Professional Desktop Experience**:
  - Desktop Environment: GNOME Workstation (`gnome-shell`, `gnome-session`, GDM3 autologin, Wayland & X11)
  - Full Basic Utility Suite: Nautilus, GNOME Terminal, Gedit, Nano, Vim Tiny, GNOME Calculator, Eye of GNOME (`eog`), GNOME System Monitor, `htop`, File Roller, 7z, Unzip, Zip, NetworkManager
  - 5 Distinct Visual Themes: Pulse Dark (default), Pulse Light, Pulse Cyber Neon, Pulse Midnight Minimal, Pulse Security Slate
  - 5 4K Vector Wallpapers & native GNOME Settings integration
  - Interactive Theme Switcher: CLI (`pulse theme`) and GUI (`pulse-theme-gui`)
  - Terminal-first workflow powered by modern Pulse CLI tooling (`pulse info`, `pulse doctor`, `pulse theme`)
- **Security-First Architecture**:
  - Full-disk encryption with LUKS and Secure Boot compatibility
  - AppArmor security enforcement and nftables/UFW firewall active by default
  - Verified repository signing and package provenance
  - Controlled security tool isolation to prevent upstream dependency collisions

---

## Repository Structure

```
pulse-linux/
├── branding/         # Logos, wallpapers, icons, SDDM theme, Plymouth splash
├── build/            # Toolchains, rootfs generators, SquashFS and ISO pipelines
├── iso/              # Bootloader configurations (GRUB2, EFI, loopback)
├── installer/        # Calamares installer configurations and first-boot setup
├── packages/         # Native Pulse .deb package definitions and meta-packages
├── repositories/     # APT repository configurations and signing keys
├── kernel/           # Kernel tuning parameters and hardware rules
├── desktop/          # KDE Plasma configurations, color schemes, and applets
├── applications/     # Pulse Control Center, Software Center, Doctor, Hubs
├── configurations/   # /etc configs, os-release, PAM, sudoers, network
├── security/         # Security profiles, AppArmor profiles, audit policies
├── developer/        # Developer bundles and language SDK profiles
├── compatibility/    # Waydroid APK and Wine EXE installer helpers
├── scripts/          # Pulse CLI command-line suite (`pulse`)
├── tests/            # Automated smoke tests and QEMU boot test suites
├── documentation/    # Comprehensive technical guides and architecture manuals
└── release/          # Verified ISO images, SHA256 checksums, and signatures
```

---

## Quick Start & Building From Source

Pulse Linux builds reproducibly using rootless container staging and Debian package mirrors.

```bash
# 1. Setup build toolchain
python3 build/scripts/00_setup_toolchain.py

# 2. Build rootfs (GNOME desktop, full utilities, themes, wallpapers)
python3 build/scripts/01_build_rootfs.py

# 3. Build live initial ramdisk
python3 build/scripts/02_build_initramfs.py

# 4. Assemble bootable hybrid ISO
python3 build/scripts/03_build_iso.py

# 5. Test in QEMU with KVM acceleration
./build/scripts/04_test_qemu.sh
```

---

## Documentation

- [Roadmap & Acceptance Criteria](ROADMAP.md)
- [Development Status](DEVELOPMENT_STATUS.md)
- [Specification](PROJECT%20PULSE%20LINUX%20Complete.md)
- [Build Instructions](documentation/BUILD.md)
- [Installation Guide](documentation/INSTALL.md)

---

## License & Upstream Attribution

Pulse Linux is developed in accordance with open-source software licensing. Debian is a registered trademark of Software in the Public Interest, Inc. Ubuntu is a registered trademark of Canonical Ltd. Kali Linux is a registered trademark of OffSec. Pulse Linux is an independent distribution and is not affiliated with or endorsed by Canonical, OffSec, or SPI.
