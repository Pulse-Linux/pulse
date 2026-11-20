# Pulse Linux 1.0 (Vanguard) — GNOME Desktop Workstation

> *"One Operating System. Two Worlds. Unlimited Possibilities."*

We are pleased to announce the inaugural public release of **Pulse Linux 1.0 (Vanguard)** — a modern, production-grade Linux distribution built on the rock-solid foundation of Debian 12 (Bookworm), uniting developer productivity, system reliability, and modular cybersecurity toolsets.

---

### 🌟 Key Highlights & Included Features

#### 1. Debian Stable (Bookworm) Foundation
* **Kernel**: Official Debian Linux Kernel `6.1.0-50-amd64` with 45+ essential boot and storage drivers.
* **Package Management**: Native `.deb` packaging with Debian Bookworm repositories and security updates.
* **Live System**: Robust Busybox-powered live initramfs orchestrator with overlayfs writable tmpfs layer.

#### 2. GNOME Desktop Experience
* **Compositor & Session**: Modern `gnome-shell` session running on Wayland with XWayland compatibility fallback.
* **Display Manager**: `gdm3` with passwordless automatic login for user `pulse`.
* **System Defaults**: Compiled GSettings overrides with dark mode, system fonts, and dock application pinouts.

#### 3. Complete Suite of Basic Applications & Utilities
* **File Manager**: Nautilus (GNOME Files)
* **Terminal Emulator**: GNOME Terminal
* **Text Editors**: Gedit (GUI), GNU Nano (CLI), Vim Tiny (CLI)
* **Calculator**: GNOME Calculator
* **Image Viewer**: Eye of GNOME (`eog`)
* **System Monitor**: GNOME System Monitor (GUI) & `htop` (CLI)
* **Archive Manager**: File Roller with 7-Zip (`7z`), Unzip, Zip, and tar support
* **Networking**: NetworkManager (`nmcli`, `nmtui`, `nm-applet`), `curl`, `wget`, `iproute2`, and `net-tools`

#### 4. Multiple Themes & 4K Vector Wallpapers
* **5 Distinct Visual Themes**:
  * **Pulse Dark** (Default): Electric Violet (`#7852FF`) & Pulse Blue (`#00D2FF`) on Dark Charcoal (`#12141A`).
  * **Pulse Light**: Clean Minimal Slate White (`#F8FAFC`) with Ice Blue (`#0284C7`) and Indigo (`#6366F1`).
  * **Pulse Cyber Neon**: High-voltage Synthwave Cyan (`#00F5FF`) & Neon Magenta (`#FF007F`) on Cyber Void (`#05070E`).
  * **Pulse Midnight Minimal**: Ultra-dark Stealth Obsidian (`#07080B`) for focused development.
  * **Pulse Security Slate**: Tactical Carbon Gray (`#0F141C`) with Terminal Matrix Green (`#00E676`) indicators.
* **5 4K Wallpapers**: High-definition vector SVGs natively integrated into GNOME Settings background selector.
* **Theme Switchers**: Dedicated CLI (`pulse theme`) and GUI (`pulse-theme-gui`) switcher tools.

#### 5. Pulse CLI Management Suite
Native system management tool (`/usr/local/bin/pulse`):
* `pulse info`: Comprehensive system hardware, kernel, and desktop overview.
* `pulse doctor`: Automated health, disk space, and subsystem diagnostic checks.
* `pulse theme`: Interactive CLI theme and wallpaper switcher.
* `pulse security status`: Audit firewall, AppArmor, disk encryption, and open network ports.
* `pulse update`: Safe rolling system updater.
* `pulse repair`: Automated network and package recovery.

---

### 💿 ISO Release & Verification

| Image | Size | Format | SHA256 Checksum |
| :--- | :--- | :--- | :--- |
| `pulse-linux-1.0-gnome-amd64.iso` | 615.50 MB | Hybrid ISO (UEFI + BIOS) | `a2be5dd1619f24747824a1ff4601dc5580ee1051d68354263a9b9d96b3f4967a` |
| `pulse-linux-core-amd64.iso` | 162.73 MB | Hybrid ISO (UEFI + BIOS) | `952a8b10b0f3f4bcda31147e917266ef61c9d95febcf57f4b85168cb04b26319` |

#### Checksum Verification
```bash
sha256sum -c SHA256SUMS
```

#### Live User Credentials
* **User**: `pulse` (UID 1000)
* **Password**: `pulse` (Full passwordless sudo access)
* **Root Password**: `pulse`
