# Pulse Linux System Architecture

"One Operating System. Two Worlds. Unlimited Possibilities."

This document details the architectural design, software layers, package management strategy, and security model of **Pulse Linux**.

---

## 1. Architectural Philosophy

Pulse Linux is designed to solve a fundamental trade-off in modern technical operating systems:
- **Developer Workstations** (e.g. Ubuntu) offer high stability, comprehensive programming toolchains, and container integration, but lack curated security auditing tools.
- **Security Workstations** (e.g. Kali Linux) provide hundreds of penetration testing tools, but using Rolling repositories for everyday software engineering frequently causes dependency breakage (`glibc`, Python ABI changes, broken graphics drivers).

**Pulse Linux unites both worlds** upon the rock-solid, long-term foundation of **Debian Stable**, utilizing modular isolation so that security tools and developer toolchains coexist without destabilizing the operating system.

---

## 2. System Layer Stack

```
+--------------------------------------------------------------------------+
|                  PULSE CONTROL CENTER & HUB APPLICATIONS                 |
|  Control Center | Software Center | Security Hub | Developer Hub | Doctor|
+--------------------------------------------------------------------------+
|                       DESKTOP ENVIRONMENT (KDE PLASMA)                   |
|     Wayland Session | Pulse Dark Theme | KWin Window Tiling | SDDM       |
+--------------------+--------------------------------+--------------------+
|  DEVELOPER STACK   |        COMPATIBILITY LAYERS    |   SECURITY SUITE   |
|  GCC / Clang / Rust|  Waydroid (Android APK)        |  Nmap / Wireshark  |
|  Go / Python / Java|  Wine / Proton (Windows EXE)   |  Burp / OWASP ZAP  |
|  Docker / Podman   |  Flatpak / AppImage Sandboxes  |  Ghidra / Radare2  |
+--------------------+--------------------------------+--------------------+
|                   PULSE PACKAGE MANAGEMENT & APT CHANNELS                |
|  pulse-stable | pulse-security | pulse-extras | Debian Bookworm Base     |
+--------------------------------------------------------------------------+
|                    CORE OS & SYSTEMD SERVICE SUPERVISOR                  |
|    systemd | udev | NetworkManager | AppArmor | UFW/nftables | Pulse CLI |
+--------------------------------------------------------------------------+
|                         LINUX KERNEL & DRIVER LAYER                      |
|      Linux Kernel (x86_64) | Hardware Drivers (DRM, Wi-Fi, Storage)      |
+--------------------------------------------------------------------------+
|                          FIRMWARE & HARDWARE                             |
|          UEFI / BIOS | Secure Boot | NVMe / SSD | Intel / AMD / NVIDIA   |
+--------------------------------------------------------------------------+
```

---

## 3. Package Management & Repository Channels

Pulse Linux natively adheres to Debian packaging standards (`.deb`, APT, dpkg) and introduces dedicated Pulse channels:

1. **pulse-stable**: Production-ready packages, core Pulse applications, branding, and tuned desktop configurations.
2. **pulse-testing**: Staging channel for packages undergoing automated regression testing.
3. **pulse-development**: Nightly builds and bleeding-edge developer packages.
4. **pulse-security**: Rapid security patches verified against the Debian Stable foundation.
5. **pulse-extras**: Optional applications, proprietary hardware firmware, and compatibility runtimes.

### Security Tooling Isolation Strategy
To prevent upstream package conflicts (e.g. tools requiring legacy Python 2, distinct Ruby gems, or specific glibc versions), Pulse Linux employs **modular container sandboxes** (via Distrobox/Podman) and standalone binaries. Upstream security repositories are never blindly added to `/etc/apt/sources.list`, ensuring zero risk of dependency collapse.

---

## 4. Multi-Runtime Compatibility Architecture

- **Android Subsystem**: Powered by Waydroid, integrating an LXC-based Android container that directly shares the Linux kernel and Wayland compositor. Double-clicking an `.apk` invokes the Pulse APK Installer.
- **Windows Subsystem**: Powered by Wine, Bottles, and Proton, creating isolated per-application prefixes with runtime dependencies automatically provisioned. Double-clicking an `.exe` or `.msi` triggers the Pulse Windows Compatibility Manager.
- **Sandboxed Universal Packages**: Full integration of Flatpak (Flathub) and AppImage runtimes with permission enforcement.

---

## 5. Security Architecture

1. **Kernel Enforcement**: AppArmor active by default, enforcing profiles on network services and user applications.
2. **Network Perimeter**: UFW and nftables active by default, with incoming connections blocked and stateful outgoing inspection.
3. **Cryptographic Protection**: Full-disk encryption via LUKS2 (AES-XTS-256) with Secure Boot support.
4. **Auditing**: Active system audit framework (`auditd`) logging critical permission changes and authentication failures.
5. **Pulse Doctor**: Continuous automated diagnostics monitoring memory pressure, package database consistency, and exposed ports.
