# PROJECT: PULSE LINUX
## Complete Operating System Engineering, Development and Production Specification

You are acting as a senior Linux distribution architect, Linux kernel engineer, Debian package maintainer, cybersecurity engineer, desktop environment developer, DevOps engineer, UI/UX designer and operating system release engineer.

Your assignment is to design, develop, build, test and deliver a complete, installable, production-quality Linux operating system named **Pulse Linux**.

This is a real operating system development project, not a website, desktop simulation, application mockup or simple Linux theme.

You must create the actual source code, system configurations, package definitions, installation infrastructure, desktop environment configuration, security tooling integration, build scripts, ISO generation system and release documentation.

Do not stop after creating a proposal or architectural document. Progressively implement the system until a bootable and installable operating system is produced.

---

# 1. PRODUCT IDENTITY

Product name: Pulse Linux

Short name: Pulse

Operating system family: Debian-based Linux distribution.

Primary architecture: x86_64 (AMD64).

Secondary architecture: ARM64 (aarch64), designed as a future supported build target.

Operating system category:
- Developer operating system.
- Cybersecurity workstation.
- Software engineering workstation.
- Systems engineering workstation.
- Research and innovation workstation.
- Digital forensics workstation.
- Penetration testing workstation.
- General-purpose desktop operating system.

Brand positioning:

"One Operating System. Two Worlds. Unlimited Possibilities."

Pulse Linux combines the development experience of Ubuntu, the security specialization of Kali Linux and the flexibility of Debian into one integrated operating system.

The operating system must be independently branded as Pulse Linux while properly respecting and complying with the licenses, trademarks, copyrights and redistribution requirements of its upstream projects.

Do not claim that Pulse Linux is an official Ubuntu, Debian or Kali Linux product.

---

# 2. CORE PHILOSOPHY

Pulse Linux must provide two equally important computing environments.

A. DEVELOPMENT ENVIRONMENT

Inspired by the productivity, stability and developer experience of Ubuntu.

It must provide:
- Complete software development infrastructure.
- Programming language toolchains.
- Database systems.
- Development IDEs.
- Containerization.
- Virtualization.
- Cloud development tools.
- Web development tools.
- Mobile development tools.
- Embedded development tools.
- AI and machine learning development.
- Networking and systems engineering.

B. SECURITY ENVIRONMENT

Inspired by Kali Linux.

It must provide:
- Penetration testing.
- Network security analysis.
- Vulnerability assessment.
- Digital forensics.
- Reverse engineering.
- Malware analysis in isolated environments.
- Wireless security auditing.
- Application security testing.
- Incident response.
- Cryptographic analysis.
- Security research.

The two environments must coexist without compromising system stability.

Users must be able to switch between developer and security workflows without reinstalling the operating system.

---

# 3. LINUX BASE AND PACKAGE MANAGEMENT

Use Debian Stable as the primary distribution foundation.

Select the appropriate Debian release at implementation time and pin the distribution to a tested release.

Use:
- Linux kernel with supported hardware drivers.
- Debian APT package management.
- dpkg.
- systemd.
- GRUB2.
- UEFI boot support.
- initramfs-tools or an appropriately supported alternative.
- NetworkManager.
- systemd-resolved where appropriate.

The operating system must natively support:

1. Debian packages (.deb).
2. APT repositories.
3. Flatpak applications.
4. AppImage applications.
5. Android APK applications through Waydroid.
6. Windows EXE and MSI applications through Wine.
7. Windows gaming applications through Proton.
8. Optional Snap package support.

Do not replace native Debian package management with a proprietary package system.

Create Pulse Linux's own package repository infrastructure.

Repository channels:

- pulse-stable: production packages.
- pulse-testing: packages undergoing testing.
- pulse-development: development builds.
- pulse-security: verified security updates.
- pulse-extras: optional applications and integrations.

Implement signed repository metadata, package signing, reproducible build practices and package provenance.

Do not blindly add Kali Rolling repositories to the primary Debian installation.

Instead, integrate selected Kali tools through carefully maintained packages, official upstream sources or isolated environments.

Provide a controlled mechanism for installing additional security tools without allowing their dependencies to break the base operating system.

---

# 4. DESKTOP ENVIRONMENT

Build Pulse Linux around KDE Plasma as the primary desktop environment.

Use a modern, professional, elegant interface.

The desktop must feel like an operating system built for technical professionals.

Design requirements:

- Modern dark theme by default.
- Light theme available.
- Pulse-branded wallpapers.
- Professional icon theme.
- Custom login screen.
- Custom boot splash.
- Custom system sounds with an option to disable them.
- Consistent application styling.
- Responsive desktop layouts.
- Multiple virtual desktops.
- Window tiling support.
- Multi-monitor support.
- Touchpad gestures.
- Keyboard shortcuts.
- HiDPI support.
- Accessibility support.

Brand colors:
- Primary: electric violet.
- Secondary: deep navy.
- Accent: pulse blue.
- Background: professional dark charcoal.
- Optional light theme: clean white and soft gray.

Avoid excessive gradients, unnecessary animations and visual clutter.

Create a distinctive Pulse Linux identity rather than copying Ubuntu or Kali Linux artwork.

## Desktop applications and panels

Include:

- Application launcher.
- Task manager.
- System tray.
- Notification center.
- Network manager.
- Bluetooth controls.
- Audio controls.
- Battery controls.
- Quick settings.
- System monitor.
- Clipboard manager.
- Screenshot utility.
- Screen recorder.
- File manager.
- Terminal launcher.
- Workspace switcher.

Create a custom Pulse Control Center that provides access to important operating system settings and tools.

---

# 5. PULSE CONTROL CENTER

Develop a native Pulse Control Center application.

It must provide centralized management of the operating system.

Main sections:

1. Overview
2. System Information
3. Updates
4. Drivers
5. Hardware
6. Network
7. Security Center
8. Developer Environment
9. Security Tools
10. Virtualization
11. Containers
12. Android Compatibility
13. Windows Compatibility
14. Package Management
15. Repository Management
16. Backup and Recovery
17. Firewall
18. Users and Permissions
19. Appearance
20. Performance
21. Troubleshooting

The interface must allow users to manage their operating system without always needing the terminal.

However, do not hide advanced Linux functionality.

Provide an advanced mode for experienced users.

Use an appropriate native technology, preferably Qt/PySide6 or another maintainable desktop framework.

---

# 6. DEVELOPER TOOLKIT

Pulse Linux must be one of the best operating systems for software developers.

Include a comprehensive developer environment.

## Programming languages

Provide installation profiles for:

- C.
- C++.
- Rust.
- Go.
- Python.
- Java.
- Kotlin.
- JavaScript.
- TypeScript.
- PHP.
- Ruby.
- Dart.
- Swift where officially supported.
- C#.
- .NET.
- R.
- Lua.
- Perl.
- Shell scripting.
- Assembly language.

Include the appropriate compilers, interpreters, build systems, package managers and debugging tools.

Examples:

- GCC.
- Clang.
- LLVM.
- GDB.
- LLDB.
- CMake.
- Ninja.
- Make.
- Cargo.
- Go toolchain.
- OpenJDK.
- Maven.
- Gradle.
- Node.js.
- npm.
- pnpm.
- Yarn.
- Composer.
- pip.
- uv.
- Poetry.
- RubyGems.
- Dart SDK.
- Flutter SDK.
- .NET SDK.

Do not install every possible SDK in the minimal edition. Offer installation profiles and curated developer bundles.

## IDEs and editors

Provide easy installation and integration for:

- Visual Studio Code.
- VSCodium.
- JetBrains IDEs.
- IntelliJ IDEA.
- PyCharm.
- WebStorm.
- Android Studio.
- Neovim.
- Vim.
- Emacs.
- Eclipse.
- Qt Creator.
- Code::Blocks.
- Zed where officially supported.

Respect each application's redistribution and licensing requirements.

## Web development

Provide tools for:

- React.
- Vue.
- Angular.
- Next.js.
- Nuxt.
- Svelte.
- Vite.
- Tailwind CSS.
- Laravel.
- Symfony.
- Django.
- Flask.
- FastAPI.
- Express.
- NestJS.
- WordPress development.

Include local development server support, browser developer tools and debugging integrations.

## Database engineering

Provide:

- MySQL.
- MariaDB.
- PostgreSQL.
- SQLite.
- Redis.
- MongoDB tools.
- Database clients.
- SQL editors.
- Database backup utilities.

Do not automatically run every database server on startup.

## Mobile development

Support:

- Android Studio.
- Android SDK.
- Android Emulator.
- ADB.
- Fastboot.
- Flutter.
- React Native.
- Expo.
- Kotlin Multiplatform where supported.
- Cross-platform application development.

Include udev rules and appropriate USB debugging support.

## Cloud and DevOps

Include installation profiles for:

- Docker.
- Podman.
- Kubernetes.
- kubectl.
- Helm.
- Minikube.
- Kind.
- Terraform.
- OpenTofu.
- Ansible.
- Vagrant.
- Packer.
- Git.
- GitHub CLI.
- GitLab CLI.
- OpenSSH.
- rsync.
- tmux.
- screen.

Provide cloud CLI installation options for AWS, Azure and Google Cloud.

---

# 7. CYBERSECURITY AND PENETRATION TESTING ENVIRONMENT

Build a professional security workstation.

Integrate well-maintained, legitimate security tools.

Organize tools into categories.

## Network discovery and analysis

Examples:

- Nmap.
- Masscan.
- Netcat.
- Wireshark.
- Tshark.
- tcpdump.
- Netdiscover.
- traceroute.
- mtr.
- iperf3.

## Web application security

Examples:

- Burp Suite Community Edition.
- OWASP ZAP.
- Nikto.
- Gobuster.
- Feroxbuster.
- ffuf.
- SQLmap.
- WhatWeb.
- SSLyze.
- testssl.sh.

## Vulnerability assessment

Examples:

- OpenVAS / Greenbone Community Edition where compatible.
- Lynis.
- Nuclei.
- Trivy.
- Grype.
- Semgrep.
- OWASP Dependency-Check.

## Digital forensics

Examples:

- Autopsy.
- The Sleuth Kit.
- Volatility.
- Foremost.
- Binwalk.
- ExifTool.
- TestDisk.
- PhotoRec.
- Plaso.

## Reverse engineering

Examples:

- Ghidra.
- Radare2.
- Cutter.
- JADX.
- Apktool.
- Frida.
- GDB.
- strace.
- ltrace.

## Wireless security

Examples:

- Aircrack-ng.
- Kismet.
- Bettercap.
- hcxtools.
- Wi-Fi diagnostic utilities.

Clearly identify hardware requirements for wireless monitor mode and packet injection.

## Password auditing

Examples:

- John the Ripper.
- Hashcat.
- Hydra.
- Hashcat utilities.

## Security infrastructure

Examples:

- OpenSSL.
- GnuPG.
- age.
- WireGuard.
- OpenVPN.
- nftables.
- UFW.
- Fail2ban.
- auditd.
- AppArmor.

## Security application launcher

Create a custom Pulse Security Hub.

It must organize security tools by category.

Provide:
- Tool descriptions.
- Installation status.
- Version information.
- Official documentation.
- Hardware requirements.
- Launch functionality.
- Update status.
- Dependency checking.

Do not install every large security tool by default.

Create three security installation profiles:

1. Security Essentials.
2. Professional Security Lab.
3. Complete Security Research Lab.

The complete profile should be modular and install only compatible tools.

Include clear authorization warnings and safe-use documentation.

Never execute security scans, exploitation tools or other intrusive operations automatically.

---

# 8. ANDROID APPLICATION COMPATIBILITY

Pulse Linux must support Android applications through Waydroid.

Implement:

- Waydroid installation.
- Android container initialization.
- Android application launcher integration.
- APK installation support.
- APK removal.
- Android application management.
- Clipboard integration.
- File sharing.
- Appropriate audio integration.
- Input integration.
- Hardware acceleration where supported.
- Network connectivity.
- Android application shortcuts in the desktop.

Provide a graphical APK installer.

When a user double-clicks an APK file, the system should offer to install it through the Android compatibility environment.

The installer must explain that Waydroid requires compatible kernel features and a suitable graphical session.

Support ARM translation where feasible, while clearly communicating its limitations and licensing requirements.

Do not promise that every Android application will work.

Document hardware, graphics, Google Play Services and application compatibility limitations.

---

# 9. WINDOWS APPLICATION COMPATIBILITY

Implement a Windows compatibility layer using:

- Wine.
- Winetricks.
- Bottles.
- Proton.
- Lutris.

Provide:

- EXE application launcher integration.
- MSI installer integration.
- Windows application management.
- Per-application Wine prefixes.
- Dependency management.
- Windows runtime installation.
- Application uninstall functionality.
- Desktop shortcuts.
- File associations.

Create a Pulse Windows Compatibility Manager.

When users open an EXE or MSI file, provide an option to install or run it using Wine or Bottles.

Provide compatibility profiles:

- General Windows Applications.
- Developer Applications.
- Engineering Applications.
- Windows Games.
- Legacy Applications.

Do not claim universal Windows application compatibility.

Explain that applications requiring unsupported kernel drivers, specific hardware or Windows-only services may not work.

---

# 10. VIRTUALIZATION AND SANDBOXING

Make Pulse Linux a strong operating system for running isolated technical environments.

Include:

- KVM.
- QEMU.
- libvirt.
- Virt-Manager.
- GNOME Boxes as an optional application.
- VirtualBox as an optional compatible installation.
- Docker.
- Podman.
- Distrobox.
- Toolbox where appropriate.
- LXC/LXD alternatives where supported.

Provide easy creation of:

- Ubuntu virtual machines.
- Debian virtual machines.
- Kali Linux virtual machines.
- Windows virtual machines.
- Security testing environments.
- Development containers.
- Isolated malware analysis environments.

Integrate snapshots, virtual networks and shared-folder management.

Use virtualization and isolation as the preferred way to test risky software.

---

# 11. SECURITY-FIRST OPERATING SYSTEM DESIGN

Security must be a fundamental part of Pulse Linux.

Implement:

- Secure Boot compatibility.
- Full-disk encryption using LUKS.
- Encrypted home directory options where supported.
- AppArmor.
- nftables firewall.
- UFW graphical management.
- Automatic security updates as an opt-in or clearly configurable policy.
- Signed package repositories.
- Kernel security updates.
- Secure password handling.
- sudo access control.
- SSH security configuration.
- Audit logging.
- Fail2ban.
- USB device management.
- Application sandboxing.
- Flatpak permissions management.
- Browser security recommendations.

Configure sensible defaults.

Do not disable essential Linux security features simply to make applications work.

Create a Pulse Security Center that displays:

- Firewall status.
- Disk encryption status.
- Secure Boot status.
- Security update status.
- Failed login events.
- AppArmor status.
- Suspicious service warnings.
- Exposed network services.
- Pending system updates.

Never present a simple green status indicator as proof that a system is completely secure.

Provide explanations and remediation recommendations.

---

# 12. PERFORMANCE AND SYSTEM ENGINEERING

Pulse Linux must work on both modern and reasonably modest computers.

Optimize for:

- Fast boot.
- Low idle RAM usage.
- Efficient CPU utilization.
- SSD performance.
- Laptop battery life.
- Thermal management.
- Graphics acceleration.
- Multi-core workloads.
- Development workloads.
- Large compilation tasks.

Include:

- systemd-boot diagnostics or GRUB2 diagnostics.
- zram configuration.
- Appropriate swap management.
- CPU frequency management.
- power-profiles-daemon.
- thermald where applicable.
- smartmontools.
- lm-sensors.
- nvme-cli.
- iotop.
- htop.
- btop.
- glances.
- sysstat.

Provide selectable power profiles:

1. Balanced.
2. Performance.
3. Power Saver.
4. Developer Workload.

Never apply aggressive performance tweaks that compromise hardware reliability.

---

# 13. HARDWARE AND DRIVER SUPPORT

Provide reliable hardware detection and configuration.

Support:

- Intel processors.
- AMD processors.
- NVIDIA GPUs.
- AMD GPUs.
- Intel graphics.
- Wi-Fi adapters.
- Bluetooth devices.
- Ethernet.
- USB devices.
- Audio devices.
- Webcams.
- Printers.
- Scanners.
- Touchscreens.
- External monitors.
- Thunderbolt where supported.

Implement an optional driver management interface.

Handle proprietary drivers and firmware according to their licensing requirements.

Provide NVIDIA driver installation and verification tools.

Include diagnostics for missing firmware, GPU acceleration and hardware incompatibilities.

Do not bundle proprietary drivers into the default ISO unless redistribution rights permit it.

---

# 14. PULSE APPLICATION ECOSYSTEM

Develop a native Pulse Software Center.

It should provide:

- Application discovery.
- Application installation.
- Application removal.
- Updates.
- Package details.
- Version history.
- Screenshots and descriptions.
- Source repository information.
- Permission information.
- Package verification.
- Search and category filters.

Support available application sources:

- Debian APT.
- Pulse repositories.
- Flatpak.
- AppImage.
- Windows compatibility applications.
- Android applications.

Clearly distinguish native applications from compatibility-layer applications.

Do not present unverified downloads as trusted software.

Provide repository trust information and package provenance.

---

# 15. TERMINAL EXPERIENCE

Create Pulse Terminal as the default terminal experience.

Use a modern terminal emulator with:

- Tabs.
- Split panes.
- Multiple sessions.
- Search.
- Copy and paste.
- Custom themes.
- Font management.
- SSH profiles.
- Keyboard shortcuts.
- Command history.

Provide an optional Zsh environment with Oh My Zsh or a lightweight alternative.

Include:

- Bash.
- Zsh.
- Fish.
- Starship prompt.
- tmux.
- fzf.
- ripgrep.
- fd.
- bat.
- eza.
- jq.
- yq.

Create Pulse command-line utilities.

Examples:

pulse info
pulse update
pulse doctor
pulse install developer
pulse install security
pulse install android
pulse install windows
pulse security status
pulse hardware
pulse repair
pulse system clean

All commands must perform actual documented operations.

Do not create fake commands or placeholder success responses.

---

# 16. PULSE SYSTEM UTILITIES

Develop a set of native system tools.

Pulse Doctor:
Diagnoses operating system problems, missing dependencies, repository errors, disk issues, network issues and hardware problems.

Pulse Update:
Provides a controlled system update interface.

Pulse Backup:
Provides backup and restoration support using established Linux backup technologies.

Pulse Monitor:
Displays CPU, RAM, disk, network, GPU and process statistics.

Pulse Network:
Provides network diagnostics and configuration.

Pulse Package Manager:
Provides a unified interface to supported package sources.

Pulse Security Hub:
Provides access to security tools and security status.

Pulse Developer Hub:
Provides programming environments, development toolchains and project shortcuts.

Pulse Compatibility Manager:
Manages Android and Windows application environments.

Pulse Recovery:
Provides system recovery, boot repair and rescue utilities.

---

# 17. INSTALLATION SYSTEM

Build a complete operating system installer.

Prefer Calamares or another proven Linux distribution installer.

The installer must support:

- Live boot.
- UEFI.
- Legacy BIOS where practical.
- GPT.
- EFI system partitions.
- Automatic partitioning.
- Manual partitioning.
- LUKS disk encryption.
- Btrfs.
- ext4.
- Swap configuration.
- User creation.
- Hostname configuration.
- Timezone selection.
- Keyboard layouts.
- Language selection.
- Bootloader installation.
- Offline installation of essential components.
- Online installation of optional components.

Provide installation profiles:

1. Pulse Linux Desktop.
2. Pulse Linux Developer.
3. Pulse Linux Security.
4. Pulse Linux Professional.

The user must be able to select additional tool bundles during installation.

Create a first-boot setup assistant.

It should help users:

- Configure their system.
- Check hardware.
- Install additional drivers.
- Select a developer environment.
- Select security tools.
- Configure Android support.
- Configure Windows support.
- Set update preferences.

---

# 18. EDITIONS

Produce the following official editions using a shared base system.

## Pulse Linux Core

Minimal, fast and stable desktop operating system.

For users who want a clean Linux experience.

## Pulse Linux Developer

Optimized for programmers, software engineers, researchers and application developers.

Includes the curated developer toolkit.

## Pulse Linux Security

Optimized for cybersecurity professionals, penetration testers, security researchers and digital forensic specialists.

Includes the curated security toolkit.

## Pulse Linux Professional

The complete workstation experience combining development, security, engineering and compatibility features.

Do not duplicate the entire operating system for each edition. Use shared base packages and profile-based installation.

---

# 19. SOFTWARE ENGINEERING AND CODE QUALITY

Organize the source code into maintainable repositories or clearly separated modules.

Suggested structure:

pulse-linux/
    branding/
    build/
    iso/
    installer/
    packages/
    repositories/
    kernel/
    desktop/
    applications/
        pulse-control-center/
        pulse-software-center/
        pulse-terminal/
        pulse-security-hub/
        pulse-developer-hub/
        pulse-system-monitor/
        pulse-compatibility-manager/
        pulse-doctor/
        pulse-backup/
        pulse-recovery/
    configurations/
    security/
    developer/
    compatibility/
    scripts/
    tests/
    documentation/
    release/

Use established upstream projects wherever possible.

Do not rewrite working Linux infrastructure without a compelling technical reason.

Write maintainable, documented code.

Use Git for version control.

Provide automated testing.

Provide package build scripts.

Provide CI/CD pipelines.

Use automated checks for:

- Package dependency resolution.
- Package signing.
- ISO integrity.
- Bootability.
- Installer functionality.
- Hardware detection.
- Security defaults.
- Desktop startup.
- Application launching.
- Upgrade compatibility.

---

# 20. RELEASE AND UPDATE INFRASTRUCTURE

Create a professional operating system release process.

Implement:

- Semantic versioning.
- Release channels.
- Signed ISO images.
- SHA256 checksums.
- Package repository signing.
- Security advisories.
- Changelogs.
- Upgrade procedures.
- Rollback strategy where supported.
- Installation documentation.
- Release notes.

Provide a predictable update policy.

Separate security updates, ordinary updates and major distribution upgrades.

Do not automatically migrate users between major Debian releases without appropriate testing and a supported upgrade path.

---

# 21. TESTING AND QUALITY ASSURANCE

The project is not complete merely because an ISO file exists.

Test the system in QEMU/KVM and on representative physical hardware.

Mandatory tests:

1. ISO boots successfully.
2. Live desktop works.
3. Installer launches.
4. Installation completes.
5. Installed system boots.
6. User account works.
7. Network connectivity works.
8. APT works.
9. Debian packages install successfully.
10. Flatpak works.
11. Developer tools work.
12. Security tools launch.
13. Firewall works.
14. AppArmor works.
15. Windows compatibility layer works.
16. Android compatibility layer initializes where hardware supports it.
17. Graphics drivers function.
18. Audio works.
19. Suspend and resume work.
20. System update works.
21. Recovery environment works.

Document hardware-dependent test failures rather than pretending every feature works on every machine.

Create automated smoke tests and a release acceptance checklist.

---

# 22. DOCUMENTATION

Produce comprehensive documentation:

- Installation guide.
- First boot guide.
- Desktop guide.
- Developer guide.
- Security guide.
- Package management guide.
- Windows compatibility guide.
- Android compatibility guide.
- Hardware compatibility guide.
- System administration guide.
- Troubleshooting guide.
- Recovery guide.
- Building Pulse Linux from source.
- Creating custom editions.
- Maintaining repositories.
- Security policy.
- Release policy.
- Contribution guidelines.

Include clear technical explanations and runnable examples.

---

# 23. DESIGN AND BRANDING

Develop a complete Pulse Linux visual identity.

Create:

- Official logo.
- Icon.
- Wordmark.
- Boot splash.
- Login background.
- Desktop wallpaper.
- Installer branding.
- Application icons.
- Control Center branding.
- System icons.
- Documentation theme.

The design should be professional, futuristic, minimal and recognizable.

The visual identity should communicate technology, engineering, innovation, performance and security.

Do not imitate Kali Linux's dragon, Ubuntu's logo or Debian's swirl.

Use the name Pulse Linux consistently.

---

# 24. BUILD AND DELIVERY REQUIREMENTS

The final deliverable must include:

1. Complete source repository.
2. Linux distribution build configuration.
3. Package definitions.
4. ISO generation scripts.
5. Desktop environment configuration.
6. Installer configuration.
7. Repository configuration.
8. Custom Pulse applications.
9. Developer tool profiles.
10. Security tool profiles.
11. Android compatibility integration.
12. Windows compatibility integration.
13. Automated tests.
14. CI/CD configuration.
15. Complete documentation.
16. Release notes.
17. Bootable ISO image.

Produce at least one working x86_64 bootable ISO.

Suggested ISO outputs:

pulse-linux-core-amd64.iso
pulse-linux-developer-amd64.iso
pulse-linux-security-amd64.iso
pulse-linux-professional-amd64.iso

If all editions cannot be produced immediately, prioritize the Core edition and make the other editions reproducible from the same source and build infrastructure.

Provide SHA256 checksums for release artifacts.

---

# 25. DEVELOPMENT EXECUTION STRATEGY

Do not attempt to build everything simultaneously.

Execute the project in carefully managed phases.

PHASE 1: FOUNDATION
- Establish Debian base.
- Configure repositories.
- Configure kernel and bootloader.
- Establish the build environment.
- Generate the first bootable ISO.

PHASE 2: DESKTOP
- Integrate KDE Plasma.
- Apply Pulse branding.
- Configure login and boot splash.
- Build desktop defaults.

PHASE 3: CORE SYSTEM
- Integrate networking.
- Configure security defaults.
- Configure drivers.
- Implement updates.
- Implement Pulse command-line utilities.

PHASE 4: DEVELOPER ENVIRONMENT
- Integrate development toolchains.
- Create developer installation profiles.
- Integrate databases and DevOps tools.

PHASE 5: SECURITY ENVIRONMENT
- Integrate security tools.
- Create Pulse Security Hub.
- Implement security profiles.
- Validate isolation and system stability.

PHASE 6: COMPATIBILITY
- Integrate Waydroid.
- Integrate Wine and Bottles.
- Integrate Proton and Lutris.
- Develop compatibility management interfaces.

PHASE 7: PULSE APPLICATIONS
- Build Control Center.
- Build Software Center.
- Build Developer Hub.
- Build Security Hub.
- Build system utilities.

PHASE 8: INSTALLER
- Build and customize the installer.
- Implement partitioning and encryption.
- Implement first-boot configuration.

PHASE 9: TESTING
- Run automated tests.
- Test virtual machines.
- Test physical hardware.
- Fix boot, package, driver and compatibility issues.

PHASE 10: RELEASE
- Generate final ISO images.
- Generate checksums.
- Sign artifacts.
- Publish documentation.
- Prepare the first official release.

---

# 26. IMPORTANT RULES FOR THE AI DEVELOPMENT AGENT

1. Build an actual operating system, not a website representing an OS.
2. Never claim a feature has been implemented unless working code and configuration exist.
3. Never create fake installation scripts.
4. Never use placeholder commands that return fabricated success messages.
5. Never silently skip failed build stages.
6. Do not mix incompatible Debian and Kali repositories.
7. Do not compromise the operating system's security to improve compatibility.
8. Respect upstream software licenses.
9. Prefer official upstream packages and well-maintained projects.
10. Document proprietary software requirements.
11. Avoid unnecessarily bloating the base installation.
12. Make advanced functionality modular.
13. Preserve the ability to upgrade the operating system.
14. Make the system reproducibly buildable.
15. Never overwrite the host operating system while building.
16. Build and test inside isolated environments or virtual machines.
17. Maintain a clear record of completed, incomplete and blocked features.
18. Use real integration tests.
19. Do not declare the project production-ready until release acceptance tests pass.
20. If a requested feature is technically impossible or unsupported, explain why and provide the best available alternative.

If you encounter a missing dependency, build error or incompatible upstream component, investigate and resolve it before moving forward.

Do not abandon the project after producing the initial ISO.

---

# 27. FIRST TASK

Start by examining the available development machine and identifying:

- CPU architecture.
- CPU cores.
- Available RAM.
- Available disk space.
- Virtualization support.
- Existing Linux distribution.
- Available build dependencies.
- Network connectivity.

Then create the Pulse Linux source repository.

Before building the full distribution, implement Phase 1 and produce the first bootable Pulse Linux ISO.

Create a project roadmap with measurable acceptance criteria.

Maintain a DEVELOPMENT_STATUS.md file that tracks:

- Completed features.
- Features currently being developed.
- Pending features.
- Failed tests.
- Known compatibility limitations.
- Build instructions.
- Next implementation tasks.

After Phase 1, continue through the remaining phases systematically.

Your ultimate objective is to deliver a complete, independently branded, Debian-based operating system called PULSE LINUX, suitable for professional developers, software engineers, systems engineers, cybersecurity experts and technical researchers.

**Build Pulse Linux as a real operating system that people can install on physical computers and use as their primary workstation.**
