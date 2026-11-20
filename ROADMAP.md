# Pulse Linux Engineering Roadmap

"One Operating System. Two Worlds. Unlimited Possibilities."

This roadmap defines the 10 engineering phases required to design, develop, build, test, and release **Pulse Linux**, a Debian-based developer and cybersecurity workstation distribution.

---

## Phase 1: Foundation & Bootable Core ISO (Target: Completed)
- [x] **Host System Diagnostics**: Identify CPU, RAM, Disk, KVM acceleration, and network connectivity.
- [x] **Source Repository Architecture**: Establish modular repository layout, version control, and build structure.
- [ ] **Debian Base & Rootfs Pipeline**: Build an unprivileged rootfs generator pinning Debian Bookworm with signed repositories.
- [ ] **Kernel & Live-Boot Configuration**: Package Linux kernel, initramfs with `live-boot` support, and systemd init.
- [ ] **GRUB2 Hybrid Bootloader**: Support UEFI and BIOS El Torito boot with signed EFI and GRUB menu configurations.
- [ ] **First Bootable ISO Generation**: Produce `pulse-linux-core-amd64.iso` and verify boot in QEMU/KVM.
- **Acceptance Criteria**:
  - Live ISO boots in QEMU/KVM to an interactive root/pulse prompt.
  - Filesystem mounts overlayfs over SquashFS root.
  - Hardware detection (udev) initializes successfully.
  - `pulse` command-line utility executes and reports correct OS identity.

---

## Phase 2: Desktop Environment & Visual Identity
- [ ] **KDE Plasma 5/6 Integration**: Configure modern, lightweight, professional KDE Plasma session.
- [ ] **Pulse Visual Identity**:
  - Electric violet (`#7852FF`), deep navy (`#0B1021`), pulse blue (`#00D2FF`), dark charcoal (`#12141A`).
  - Vector SVG logo, wordmark, and application icon sets.
  - Wallpapers (dark and light modes).
- [ ] **Display Manager**: Configure SDDM with custom Pulse theme and autologin capability for live media.
- [ ] **Boot Splash**: Configure Plymouth theme with Pulse animated pulse wave.
- [ ] **Desktop Defaults**: Configure virtual desktops, window tiling shortcuts, system tray widgets, and terminal hotkeys.
- **Acceptance Criteria**:
  - Graphical desktop loads cleanly upon boot without manual intervention.
  - Look-and-feel theme applied across Qt and GTK applications.

---

## Phase 3: Core System Engineering & Pulse CLI
- [ ] **Network Stack**: NetworkManager with systemd-resolved and iwd/wpa_supplicant.
- [ ] **Security Defaults**: AppArmor enabled by default, UFW firewall active, auditd configured, unprivileged hardening.
- [ ] **Power & Performance Profiles**: Configure `power-profiles-daemon`, zram swap compressed with zstd, and CPU governor tuning.
- [ ] **Pulse CLI (`pulse`)**:
  - `pulse info`: System diagnostics, kernel version, edition, architecture.
  - `pulse doctor`: Automated health check (disk, repos, memory, systemd failed units).
  - `pulse update`: Safe atomic package updates with rollback protection.
  - `pulse security status`: Real-time firewall, AppArmor, LUKS, and listening ports report.
  - `pulse install <profile>`: Modular installer for developer and security profiles.
  - `pulse repair`: Automated package and bootloader repair routines.
  - `pulse system clean`: Safe cache, old kernel, and orphaned package cleaner.
- **Acceptance Criteria**:
  - All `pulse` commands execute real operations with exit code 0 and structured JSON/colored terminal outputs.

---

## Phase 4: Developer Toolkit & Environment Profiles
- [ ] **Core Toolchains**: GCC, Clang/LLVM, Make, CMake, Ninja, Git, Python 3, Rust (cargo), Go, OpenJDK.
- [ ] **Modern Developer CLI Tools**: fzf, ripgrep, bat, eza, jq, yq, tmux, zsh, Starship prompt.
- [ ] **Containerization & Sandboxing**: Docker CE, Podman, Distrobox for non-native dependencies.
- [ ] **Modular Developer Profiles**:
  - `profile-web`: Node.js, pnpm, Bun, frontend & backend frameworks.
  - `profile-systems`: C/C++, Rust, Go, assembly, GDB, LLDB, Valgrind, perf.
  - `profile-cloud`: kubectl, Helm, Terraform, Ansible, AWS/Azure/GCP CLIs.
  - `profile-mobile`: Android SDK tools, Flutter, udev rules for debugging.
  - `profile-data-ai`: Python scientific stack, Jupyter, PyTorch/ONNX runtime tooling.
- **Acceptance Criteria**:
  - Developer profiles can be installed cleanly without breaking base system dependencies.

---

## Phase 5: Cybersecurity & Penetration Testing Environment
- [ ] **Repository Isolation Strategy**: Strict decoupling of base Debian packages and security tooling.
- [ ] **Modular Security Profiles**:
  - `security-essentials`: Nmap, Wireshark, tcpdump, Netcat, John, Aircrack-ng, SQLmap.
  - `security-professional`: Burp Suite CE, OWASP ZAP, Ghidra, Radare2/Cutter, Metasploit, Nuclei.
  - `security-research`: Volatility 3, Autopsy, Binwalk, Frida, GDB-gef, TestDisk, Plaso.
- [ ] **Pulse Security Hub**: Desktop and CLI hub organizing tools by workflow categories with safety warnings.
- **Acceptance Criteria**:
  - Security tools execute in isolated sandboxes or native packages without pulling conflicting glibc or libc6 libraries.

---

## Phase 6: Android & Windows Compatibility Subsystems
- [ ] **Android Compatibility (Waydroid)**:
  - Waydroid container initialization scripts.
  - Graphic APK installer (`pulse-apk-installer`).
  - Desktop integration for Android apps with launcher icons.
- [ ] **Windows Compatibility (Wine / Bottles / Proton)**:
  - Automated Wine prefix management (`pulse-wine-init`).
  - Graphical EXE/MSI runner (`pulse-exe-installer`).
  - Pre-configured profiles for developer utilities, engineering tools, and games.
- **Acceptance Criteria**:
  - Double-clicking `.apk` launches the Pulse APK installer.
  - Double-clicking `.exe` opens the Pulse Windows Compatibility Manager.

---

## Phase 7: Pulse Native Application Ecosystem
- [ ] **Pulse Control Center**: Central management GUI (Qt/QML/PySide6) for settings, updates, hardware, and profiles.
- [ ] **Pulse Software Center**: Unified package manager supporting Debian APT, Flatpak, AppImage, and Pulse repos.
- [ ] **Pulse Security Hub**: Interactive tool launcher, category browser, and vulnerability scanner.
- [ ] **Pulse Developer Hub**: SDK switcher, runtime environment manager, and project initializer.
- [ ] **Pulse System Monitor**: Lightweight real-time hardware, process, and network monitor.
- **Acceptance Criteria**:
  - Native applications launch cleanly with consistent Pulse dark theme and responsive UI.

---

## Phase 8: System Installer & First-Boot Setup
- [ ] **Calamares Installer Integration**:
  - Pulse branded slideshow and design.
  - Partitioning with Btrfs (snapshots) and ext4.
  - LUKS full-disk encryption with secure key derivation.
  - EFI and legacy bootloader installation.
  - Profile selection during installation (Core, Developer, Security, Professional).
- [ ] **First-Boot Setup Assistant**:
  - Hardware driver detection (NVIDIA, Wi-Fi, audio).
  - Power profile and telemetry configuration.
  - Initial developer and security bundle selection.
- **Acceptance Criteria**:
  - Installer successfully partitions a virtual drive, installs the OS, and boots into the installed system.

---

## Phase 9: Testing, Verification & Quality Assurance
- [ ] **Automated Smoke Tests**: Verification test suite for ISO boot, network, packaging, and tools.
- [ ] **QEMU / KVM Integration Matrix**: Boot tests under UEFI, BIOS, virtio-gpu, and software rasterizer.
- [ ] **Security Audits**: Lynis compliance audit, open port verification, AppArmor profile enforcement.
- **Acceptance Criteria**:
  - 100% pass on all 21 mandatory test categories specified in Section 21 of the specification.

---

## Phase 10: Production Release Infrastructure
- [ ] **Reproducible Build Pipeline**: Single-command build script producing verified ISO artifacts.
- [ ] **Release Metadata**: Signed checksums (SHA256), GPG signature verification, and release notes.
- [ ] **Documentation**: Full operator manual, installation guide, developer handbook, and security handbook.
- **Acceptance Criteria**:
  - Complete, verifiable release files published in `/release` with SHA256SUMS.
