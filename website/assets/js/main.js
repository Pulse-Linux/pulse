/**
 * Pulse Linux Official Website Interactive Scripts
 * Complies with modern web standards and accessibility guidelines.
 */

document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initMobileMenu();
  initDesktopShowcase();
  initTabs();
  initCopyButtons();
});

/* -------------------------------------------------------------
 * 1. Dark / Light Scheme Toggle (Modern Web Guidance Compliant)
 * ------------------------------------------------------------- */
function initThemeToggle() {
  const toggleBtn = document.getElementById('theme-toggle-btn');
  const metaColorScheme = document.querySelector('meta[name="color-scheme"]');
  if (!toggleBtn || !metaColorScheme) return;

  function updateToggleUI(currentScheme) {
    const isDark = currentScheme === 'dark' || 
      (currentScheme === 'light dark' && window.matchMedia('(prefers-color-scheme: dark)').matches);
    
    toggleBtn.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
    toggleBtn.innerHTML = isDark
      ? `<svg class="w-5 h-5 text-amber-300" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true"><path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"/></svg>`
      : `<svg class="w-5 h-5 text-violet-400" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true"><path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"/></svg>`;
  }

  // Initial UI state
  updateToggleUI(metaColorScheme.content);

  toggleBtn.addEventListener('click', () => {
    const isSystemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const currentExplicit = localStorage.getItem('color-scheme');
    let resolvedCurrent = currentExplicit ?? (isSystemDark ? 'dark' : 'light');
    let target = resolvedCurrent === 'dark' ? 'light' : 'dark';

    // If target equals system preference, remove stored value (return to system)
    if ((target === 'dark' && isSystemDark) || (target === 'light' && !isSystemDark)) {
      localStorage.removeItem('color-scheme');
      metaColorScheme.content = 'light dark';
    } else {
      localStorage.setItem('color-scheme', target);
      metaColorScheme.content = target;
    }

    updateToggleUI(metaColorScheme.content);
  });

  // Sync with other tabs
  window.addEventListener('storage', (e) => {
    if (e.key === 'color-scheme') {
      metaColorScheme.content = e.newValue ?? 'light dark';
      updateToggleUI(metaColorScheme.content);
    }
  });
}

/* -------------------------------------------------------------
 * 2. Mobile Menu Navigation Drawer
 * ------------------------------------------------------------- */
function initMobileMenu() {
  const toggle = document.getElementById('mobile-menu-toggle');
  const nav = document.getElementById('mobile-nav');
  if (!toggle || !nav) return;

  toggle.addEventListener('click', () => {
    const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', !isExpanded);
    if (isExpanded) {
      nav.classList.remove('open');
      nav.classList.add('closed');
    } else {
      nav.classList.remove('closed');
      nav.classList.add('open');
    }
  });

  // Close when clicking any nav link
  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      toggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('open');
      nav.classList.add('closed');
    });
  });
}

/* -------------------------------------------------------------
 * 3. Interactive Desktop Showcase & Live Wallpaper Switcher
 * ------------------------------------------------------------- */
function initDesktopShowcase() {
  const mockScreen = document.getElementById('mockup-screen-bg');
  const themePills = document.querySelectorAll('.theme-selector-btn');
  const screenTabBtns = document.querySelectorAll('.mockup-tab-btn');
  const screenViews = document.querySelectorAll('.mockup-screen-view');

  // Theme previews mapping
  const wallpapers = {
    'dark': 'assets/wallpapers/pulse-dark-4k.svg',
    'light': 'assets/wallpapers/pulse-light-4k.svg',
    'cyber-neon': 'assets/wallpapers/pulse-cyber-neon-4k.svg',
    'midnight': 'assets/wallpapers/pulse-midnight-minimal-4k.svg',
    'security-slate': 'assets/wallpapers/pulse-security-slate-4k.svg'
  };

  themePills.forEach(btn => {
    btn.addEventListener('click', () => {
      const themeKey = btn.getAttribute('data-theme');
      if (wallpapers[themeKey] && mockScreen) {
        mockScreen.style.backgroundImage = `url('${wallpapers[themeKey]}')`;
        
        themePills.forEach(p => p.classList.remove('ring-2', 'ring-cyan-400', 'active'));
        btn.classList.add('ring-2', 'ring-cyan-400', 'active');
        
        showToast(`Switched active preview to: Pulse ${btn.innerText.trim()}`);
      }
    });
  });

  // Screen View Switcher (Desktop vs CLI Terminal vs Cybersecurity Tools)
  screenTabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetView = btn.getAttribute('data-view');
      screenTabBtns.forEach(b => {
        b.classList.remove('bg-violet-600', 'text-white');
        b.classList.add('bg-white/10', 'text-slate-300');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('bg-violet-600', 'text-white');
      btn.classList.remove('bg-white/10', 'text-slate-300');
      btn.setAttribute('aria-selected', 'true');

      screenViews.forEach(view => {
        if (view.id === `view-${targetView}`) {
          view.classList.remove('hidden');
        } else {
          view.classList.add('hidden');
        }
      });
    });
  });

  // Interactive Terminal Command Triggers
  const termCmds = document.querySelectorAll('.term-interactive-btn');
  const termOutput = document.getElementById('interactive-term-output');

  const cmdOutputs = {
    'pulse info': `<span class="text-violet-400 font-bold">pulse@vanguard:~$ pulse info</span>
<span class="text-cyan-400">───────────────────────────────────────────────────</span>
<span class="text-white font-semibold">Pulse Linux 1.0 (Vanguard) x86_64</span>
<span class="text-slate-400">Base System:</span>     Debian GNU/Linux 12 (Bookworm)
<span class="text-slate-400">Desktop:</span>         GNOME 43.9 (Wayland & X11)
<span class="text-slate-400">Kernel:</span>          6.1.0-28-amd64 #1 SMP PREEMPT_DYNAMIC
<span class="text-slate-400">Developer Stack:</span> Git, Python 3.11, Rust, Go, Node.js
<span class="text-slate-400">Security Suite:</span>  Modular Kali Isolation Engine (Active)
<span class="text-slate-400">Installed Apps:</span>  Nautilus, Terminal, Gedit, Eye of GNOME,
                 File Roller, Calculator, System Monitor
<span class="text-cyan-400">───────────────────────────────────────────────────</span>
<span class="text-emerald-400">✔ System Status: All modules verified healthy</span>`,

    'pulse doctor': `<span class="text-violet-400 font-bold">pulse@vanguard:~$ pulse doctor</span>
<span class="text-slate-400">Running Pulse Linux Diagnostics Engine...</span>
<span class="text-emerald-400">[PASS]</span> APT Package Repositories: Official Debian Bookworm verified
<span class="text-emerald-400">[PASS]</span> Linux Kernel integrity and DKMS modules healthy
<span class="text-emerald-400">[PASS]</span> GNOME Desktop Shell and Wayland compositor responsive
<span class="text-emerald-400">[PASS]</span> Pulse Theme Engine: 5 themes & wallpapers synchronized
<span class="text-emerald-400">[PASS]</span> Security Sandboxing Subsystem ready (AppArmor enabled)
<span class="text-cyan-400">Result: 0 errors, 0 warnings. System optimal.</span>`,

    'pulse theme': `<span class="text-violet-400 font-bold">pulse@vanguard:~$ pulse theme --list</span>
Available Pulse Linux Built-in Themes:
  * <span class="text-violet-400">pulse-dark</span>             (Active: Deep Void Charcoal & Electric Violet)
    <span class="text-slate-300">pulse-light</span>            (Clean Pure Slate & Cyan Accents)
    <span class="text-pink-400">pulse-cyber-neon</span>       (Hacker Synthwave & Matrix Neon)
    <span class="text-slate-500">pulse-midnight</span>         (OLED Pure Pitch Black Minimalist)
    <span class="text-emerald-400">pulse-security-slate</span>   (Distraction-Free Tactical Grey)

Run 'pulse theme set &lt;name&gt;' to apply instantly across Shell, GTK4 & Icons.`,

    'pulse install': `<span class="text-violet-400 font-bold">pulse@vanguard:~$ pulse install --help</span>
<span class="text-cyan-400">Pulse Linux Guided Bare-Metal & VM Installer v1.0</span>
Usage: pulse-install [OPTIONS]

Options:
  --target &lt;DISK&gt;     Target installation disk (e.g. /dev/sda, /dev/nvme0n1)
  --edition &lt;TYPE&gt;    'workstation' (GNOME Desktop) or 'core' (CLI Minimal)
  --encrypt           Enable LUKS2 full-disk encryption with Argon2id
  --swap &lt;SIZE&gt;       Auto-configure ZRAM swap space (Default: 4G)
  --gui               Launch GNOME graphical installation wizard`
  };

  termCmds.forEach(btn => {
    btn.addEventListener('click', () => {
      const cmd = btn.getAttribute('data-cmd');
      if (cmdOutputs[cmd] && termOutput) {
        termOutput.innerHTML = cmdOutputs[cmd];
        termCmds.forEach(b => b.classList.remove('bg-cyan-500/20', 'border-cyan-400'));
        btn.classList.add('bg-cyan-500/20', 'border-cyan-400');
      }
    });
  });
}

/* -------------------------------------------------------------
 * 4. Tabbed Interfaces (Modern Web Guidance Compliant)
 * ------------------------------------------------------------- */
function initTabs() {
  const tabContainers = document.querySelectorAll('[data-tabs-container]');

  tabContainers.forEach(container => {
    const tabs = container.querySelectorAll('[role="tab"]');
    const panels = container.querySelectorAll('[role="tabpanel"]');

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const targetPanelId = tab.getAttribute('aria-controls');

        // Update tabs
        tabs.forEach(t => {
          const isSelected = t === tab;
          t.setAttribute('aria-selected', isSelected ? 'true' : 'false');
          t.toggleAttribute('focusgroupstart', isSelected);
        });

        // Update panels
        panels.forEach(p => {
          if (p.id === targetPanelId) {
            p.removeAttribute('hidden');
            p.setAttribute('tabindex', '0');
          } else {
            p.setAttribute('hidden', 'until-found');
            p.removeAttribute('tabindex');
          }
        });
      });
    });
  });
}

/* -------------------------------------------------------------
 * 5. Copy-to-Clipboard with Floating Toast Notification
 * ------------------------------------------------------------- */
function initCopyButtons() {
  const copyButtons = document.querySelectorAll('.copy-btn');

  copyButtons.forEach(btn => {
    btn.addEventListener('click', async () => {
      const textToCopy = btn.getAttribute('data-copy');
      const label = btn.getAttribute('data-label') || 'Text';

      try {
        await navigator.clipboard.writeText(textToCopy);
        showToast(`Copied ${label} to clipboard!`);
        
        // Brief button visual feedback
        const originalContent = btn.innerHTML;
        btn.innerHTML = `<svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg> Copied!`;
        setTimeout(() => {
          btn.innerHTML = originalContent;
        }, 2000);
      } catch (err) {
        showToast('Failed to copy. Please copy manually.');
      }
    });
  });
}

/* -------------------------------------------------------------
 * 6. Global Toast Notification System
 * ------------------------------------------------------------- */
function showToast(message) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `
    <span class="text-cyan-400 font-bold" aria-hidden="true">✔</span>
    <span>${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => {
      toast.remove();
    }, 300);
  }, 3200);
}
