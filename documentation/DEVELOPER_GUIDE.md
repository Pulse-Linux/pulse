# Pulse Linux Developer Guide

"One Operating System. Two Worlds. Unlimited Possibilities."

Pulse Linux provides one of the most comprehensive, productive, and modern software engineering environments available on Linux. This guide details language toolchains, container workflows, IDE integration, and development bundles.

---

## 1. Quick Profile Installation

Pulse Linux includes pre-configured developer bundles installable via the `pulse` CLI or Pulse Control Center:

```bash
# Systems programming (C, C++, Rust, Go, CMake, LLVM, GDB, Valgrind)
sudo pulse install systems

# Web engineering (Node.js, pnpm, Bun, Nginx, frameworks)
sudo pulse install web

# Cloud & DevOps (Docker, Podman, kubectl, Helm, Terraform, Ansible)
sudo pulse install cloud

# Mobile development (Android SDK, Flutter, ADB, Fastboot)
sudo pulse install mobile
```

---

## 2. Supported Programming Languages

### C and C++
- **Compilers**: GCC 12+ and Clang / LLVM 15+
- **Build Systems**: CMake, Ninja, Make, Meson
- **Debuggers & Profilers**: GDB, LLDB, Valgrind, perf, gprof
- **Libraries**: glibc, musl, libcurl, OpenSSL, boost

### Rust
- Installed via official toolchain (`rustup`, `rustc`, `cargo`).
- Fast compilation with `sccache` and `mold` linker options.

### Go
- Latest Go toolchain (`go`, `gofmt`, `gopls`).

### Python
- Python 3.11+ Debian base with `uv`, `pip`, `poetry`, and `venv` isolation.
- Scientific packages: NumPy, Pandas, SciPy, PyTorch.

### JavaScript & TypeScript
- Node.js LTS, `npm`, `pnpm`, `yarn`, and `bun`.
- Framework runtimes: React, Vue, Svelte, Next.js, Express, Fastify.

### Java & Kotlin
- OpenJDK 17 and OpenJDK 21 LTS.
- Build tools: Maven, Gradle.

---

## 3. Containerization & DevOps Workflows

Pulse Linux natively supports rootless containerization without daemon overhead:
- **Docker CE**: For standard container building and execution.
- **Podman**: OCI-compliant daemonless container engine.
- **Distrobox**: Seamless execution of other distribution environments (Ubuntu, Arch, Fedora) inside the Pulse terminal.
- **Kubernetes**: Pre-configured `kubectl`, `helm`, and `k3s`/`minikube` runners.

---

## 4. Database Engineering

Pulse Linux provides relational and key-value database engines with background management:
- **PostgreSQL**: `sudo systemctl start postgresql`
- **MariaDB / MySQL**: `sudo systemctl start mariadb`
- **SQLite**: Built-in CLI and GUI editors
- **Redis**: In-memory caching and message broker

*(Services are disabled by default to maintain fast boot times and conserve memory)*

---

## 5. Development Environments & Editors

- **Visual Studio Code / VSCodium**: Supported natively with official `.deb` and Flatpak integrations.
- **JetBrains IDEs**: Toolbox and standalone installations (IntelliJ IDEA, PyCharm, WebStorm, CLion, GoLand).
- **Neovim & Vim**: Pre-configured with LSP support, Treesitter syntax highlighting, and fuzzy search.
