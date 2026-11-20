#!/usr/bin/env python3
"""
Pulse Linux Theme Generator
Generates GTK 3.0, GTK 4.0, and GNOME Shell themes for all 5 Pulse Linux color schemes.
"""

from pathlib import Path

THEMES_DIR = Path(__file__).resolve().parent

THEMES = {
    "Pulse-Dark": {
        "name": "Pulse Dark",
        "comment": "Default Pulse Linux dark theme with Electric Violet and Pulse Blue accents",
        "is_dark": True,
        "accent": "#7852ff",
        "accent_secondary": "#00d2ff",
        "bg": "#12141a",
        "bg_elevated": "#1a1d26",
        "header_bg": "#161922",
        "fg": "#f1f5f9",
        "fg_muted": "#94a3b8",
        "border": "#282c37",
        "selection": "#7852ff",
        "selection_fg": "#ffffff",
        "panel_bg": "rgba(18, 20, 26, 0.88)",
        "wallpaper": "pulse-dark-4k.svg"
    },
    "Pulse-Light": {
        "name": "Pulse Light",
        "comment": "Crisp and modern light theme with Ice Blue and Indigo accents",
        "is_dark": False,
        "accent": "#6366f1",
        "accent_secondary": "#0284c7",
        "bg": "#f8fafc",
        "bg_elevated": "#ffffff",
        "header_bg": "#f1f5f9",
        "fg": "#0f172a",
        "fg_muted": "#64748b",
        "border": "#e2e8f0",
        "selection": "#6366f1",
        "selection_fg": "#ffffff",
        "panel_bg": "rgba(248, 250, 252, 0.90)",
        "wallpaper": "pulse-light-4k.svg"
    },
    "Pulse-Cyber-Neon": {
        "name": "Pulse Cyber Neon",
        "comment": "Vibrant cyberpunk synthwave theme with high-voltage Cyan and Magenta",
        "is_dark": True,
        "accent": "#00f5ff",
        "accent_secondary": "#ff007f",
        "bg": "#05070e",
        "bg_elevated": "#0d111e",
        "header_bg": "#080b15",
        "fg": "#f8fafc",
        "fg_muted": "#7dd3fc",
        "border": "#1e293b",
        "selection": "#00f5ff",
        "selection_fg": "#05070e",
        "panel_bg": "rgba(5, 7, 14, 0.92)",
        "wallpaper": "pulse-cyber-neon-4k.svg"
    },
    "Pulse-Midnight": {
        "name": "Pulse Midnight Minimal",
        "comment": "Deep stealth obsidian minimalist theme for focused development",
        "is_dark": True,
        "accent": "#8b5cf6",
        "accent_secondary": "#3b82f6",
        "bg": "#07080b",
        "bg_elevated": "#0d0e14",
        "header_bg": "#090b10",
        "fg": "#e2e8f0",
        "fg_muted": "#64748b",
        "border": "#1a1c23",
        "selection": "#8b5cf6",
        "selection_fg": "#ffffff",
        "panel_bg": "rgba(7, 8, 11, 0.94)",
        "wallpaper": "pulse-midnight-minimal-4k.svg"
    },
    "Pulse-Security-Slate": {
        "name": "Pulse Security Slate",
        "comment": "Tactical cybersecurity carbon theme with Matrix Green indicators",
        "is_dark": True,
        "accent": "#00e676",
        "accent_secondary": "#00b0ff",
        "bg": "#0f141c",
        "bg_elevated": "#161d27",
        "header_bg": "#121822",
        "fg": "#f1f5f9",
        "fg_muted": "#86efac",
        "border": "#243042",
        "selection": "#00e676",
        "selection_fg": "#0f141c",
        "panel_bg": "rgba(15, 20, 28, 0.92)",
        "wallpaper": "pulse-security-slate-4k.svg"
    }
}

def generate_index_theme(cfg):
    return f"""[Desktop Entry]
Type=X-GNOME-Metatheme
Name={cfg['name']}
Comment={cfg['comment']}
Encoding=UTF-8

[X-GNOME-Metatheme]
GtkTheme={cfg['name']}
MetacityTheme={cfg['name']}
IconTheme=Adwaita
CursorTheme=Adwaita
ButtonLayout=:minimize,maximize,close
"""

def generate_gtk_css(cfg):
    return f"""/* Pulse Linux {cfg['name']} - GTK Style Definitions */
@define-color accent_color {cfg['accent']};
@define-color accent_bg_color {cfg['accent']};
@define-color accent_fg_color {cfg['selection_fg']};
@define-color window_bg_color {cfg['bg']};
@define-color window_fg_color {cfg['fg']};
@define-color view_bg_color {cfg['bg_elevated']};
@define-color view_fg_color {cfg['fg']};
@define-color headerbar_bg_color {cfg['header_bg']};
@define-color headerbar_fg_color {cfg['fg']};
@define-color headerbar_border_color {cfg['border']};
@define-color card_bg_color {cfg['bg_elevated']};
@define-color card_fg_color {cfg['fg']};
@define-color dialog_bg_color {cfg['bg_elevated']};
@define-color dialog_fg_color {cfg['fg']};
@define-color popover_bg_color {cfg['bg_elevated']};
@define-color popover_fg_color {cfg['fg']};
@define-color destructive_color #ef4444;
@define-color destructive_bg_color #ef4444;
@define-color destructive_fg_color #ffffff;
@define-color success_color #10b981;
@define-color warning_color #f59e0b;
@define-color error_color #ef4444;

window {{
    background-color: @window_bg_color;
    color: @window_fg_color;
}}

headerbar {{
    background-color: @headerbar_bg_color;
    border-bottom: 1px solid @headerbar_border_color;
    box-shadow: none;
}}

button {{
    border-radius: 8px;
    padding: 6px 14px;
    background-color: @card_bg_color;
    color: @window_fg_color;
    border: 1px solid @headerbar_border_color;
    transition: all 150ms ease;
}}

button:hover {{
    background-color: alpha(@accent_color, 0.15);
    border-color: @accent_color;
}}

button:active {{
    background-color: @accent_color;
    color: @accent_fg_color;
}}

button.suggested-action {{
    background-color: @accent_color;
    color: @accent_fg_color;
    border: none;
}}

entry {{
    border-radius: 8px;
    background-color: @view_bg_color;
    color: @view_fg_color;
    border: 1px solid @headerbar_border_color;
    padding: 6px 10px;
}}

entry:focus {{
    border-color: @accent_color;
    box-shadow: 0 0 0 2px alpha(@accent_color, 0.35);
}}

/* Scrollbar refinement */
scrollbar slider {{
    min-width: 6px;
    min-height: 6px;
    border-radius: 4px;
    background-color: alpha(@window_fg_color, 0.25);
}}

scrollbar slider:hover {{
    background-color: @accent_color;
}}
"""

def generate_gnome_shell_css(cfg):
    return f"""/* Pulse Linux {cfg['name']} - GNOME Shell Stylesheet */

#panel {{
    background-color: {cfg['panel_bg']};
    font-weight: 500;
    font-size: 11pt;
    height: 34px;
    border-bottom: 1px solid {cfg['border']};
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
}}

#panel .panel-button {{
    color: {cfg['fg']};
    border-radius: 6px;
    margin: 2px 4px;
    padding: 0 10px;
    transition: all 150ms ease-in-out;
}}

#panel .panel-button:hover {{
    background-color: {cfg['accent']}33;
    color: {cfg['accent']};
}}

#panel .panel-button:active,
#panel .panel-button:checked {{
    background-color: {cfg['accent']};
    color: {cfg['selection_fg']};
}}

/* Dash / Dock styling */
#dash .dash-background {{
    background-color: {cfg['panel_bg']};
    border-radius: 18px;
    border: 1px solid {cfg['border']};
    padding: 6px;
}}

.app-well-app:hover .overview-icon,
.show-apps:hover .overview-icon {{
    background-color: {cfg['accent']}33;
    border-radius: 12px;
}}

.app-well-app:active .overview-icon,
.app-well-app:checked .overview-icon {{
    background-color: {cfg['accent']}66;
    border-radius: 12px;
}}

/* Modal dialogs & popup menus */
.popup-menu-content {{
    background-color: {cfg['bg_elevated']};
    border: 1px solid {cfg['border']};
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
    color: {cfg['fg']};
    padding: 8px;
}}

.popup-menu-item:hover {{
    background-color: {cfg['accent']}33;
    color: {cfg['accent']};
    border-radius: 6px;
}}

.popup-menu-item:active {{
    background-color: {cfg['accent']};
    color: {cfg['selection_fg']};
    border-radius: 6px;
}}

/* Notifications */
.message-list {{
    background-color: {cfg['bg_elevated']};
    border: 1px solid {cfg['border']};
    border-radius: 14px;
    color: {cfg['fg']};
}}

.notification-banner {{
    background-color: {cfg['bg_elevated']};
    border: 1px solid {cfg['accent']};
    border-radius: 12px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
}}
"""

def main():
    print("Generating Pulse Linux Theme Bundles...")
    for theme_id, cfg in THEMES.items():
        t_dir = THEMES_DIR / theme_id
        t_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. index.theme
        (t_dir / "index.theme").write_text(generate_index_theme(cfg))
        
        # 2. GTK 3.0 & 4.0
        gtk_css = generate_gtk_css(cfg)
        (t_dir / "gtk-3.0").mkdir(exist_ok=True)
        (t_dir / "gtk-3.0" / "gtk.css").write_text(gtk_css)
        (t_dir / "gtk-4.0").mkdir(exist_ok=True)
        (t_dir / "gtk-4.0" / "gtk.css").write_text(gtk_css)
        
        # 3. GNOME Shell
        shell_css = generate_gnome_shell_css(cfg)
        (t_dir / "gnome-shell").mkdir(exist_ok=True)
        (t_dir / "gnome-shell" / "gnome-shell.css").write_text(shell_css)
        
        print(f"  ✓ {cfg['name']} created at {t_dir.name}")
    
    print("All 5 Pulse Linux themes generated successfully!")

if __name__ == "__main__":
    main()
