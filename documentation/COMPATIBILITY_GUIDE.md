# Pulse Linux Compatibility Guide: Android & Windows

"One Operating System. Two Worlds. Unlimited Possibilities."

Pulse Linux bridges mobile, desktop, and cross-platform ecosystems by integrating high-performance compatibility subsystems for Android (APK) and Windows (EXE/MSI) applications.

---

## 1. Android Application Compatibility (Waydroid)

Pulse Linux integrates Waydroid, allowing Android applications to run natively at bare-metal performance through Linux kernel namespaces and LXC containerization.

### Requirements & Hardware Pre-checks
- **Graphics Session**: Wayland (default in KDE Plasma session).
- **Kernel Features**: Linux binder and ashmem driver nodes (`/dev/binder`, `/dev/ashmem`).
- **Architecture**: x86_64. For ARM-based APKs, an ARM translation layer (such as `libndk` or `libhoudini`) is required.

### Initializing Waydroid
```bash
# Initialize Waydroid Android subsystem
sudo waydroid init -s GAPPS -c https://ota.waydroid.net/system -v https://ota.waydroid.net/vendor

# Start container session
waydroid session start
```

### Installing Android Applications
- **Graphical Installer**: Double-click any `.apk` file in the Pulse file manager to launch the **Pulse APK Installer**.
- **CLI Installer**:
  ```bash
  waydroid app install sample-app.apk
  ```

### Limitations & Known Constraints
- Hardware-dependent features (Bluetooth low-energy peripherals, NFC, cellular hardware) may not be exposed to the Android container.
- Applications with strict hardware-backed DRM or Google SafetyNet/Play Integrity requirements (e.g. certain banking apps) may not function.

---

## 2. Windows Application Compatibility (Wine & Proton)

Pulse Linux supports Windows software execution through Wine, Bottles, and Valve's Proton compatibility layers.

### Supported Frameworks
- **Wine (Wine-GE / Wine Staging)**: Core translation of Windows API calls to POSIX/Linux.
- **Bottles**: Sandboxed Wine prefix manager for clean dependency isolation.
- **Proton**: High-performance DirectX-to-Vulkan (DXVK/VKD3D) translation layer optimized for gaming and 3D graphics.

### Installing Windows Applications
- **Graphical Execution**: Double-click any `.exe` or `.msi` file. The **Pulse Windows Compatibility Manager** prompts you to select a targeted compatibility profile.
- **CLI Execution**:
  ```bash
  # Execute in default Wine prefix
  wine application.exe

  # Configure Windows runtime dependencies
  winetricks dotnet48 vcrun2022
  ```

### Compatibility Profiles
1. **General Applications**: Office suites, utilities, and lightweight productivity tools.
2. **Developer & Engineering**: Microcontroller IDEs, CAD/EDA tools, and proprietary hardware flashers.
3. **Gaming & Graphics**: Proton DXVK integration with Vulkan acceleration.
4. **Legacy Windows**: 32-bit Windows XP/7 compatibility modes.

### Limitations
- Applications requiring proprietary Windows kernel-mode drivers (such as kernel-level anti-cheat engines like Vanguard or Easy Anti-Cheat in non-Proton modes) cannot run under Wine.
