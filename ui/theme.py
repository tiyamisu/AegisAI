"""
AegisAI — UI Theme
====================
Single source of truth for all design tokens: colors, fonts, spacing.
Import this module in every UI file instead of hard-coding values.

Palette: Warm Amber / Orange professional NGO/Government platform theme.

Usage
-----
from ui.theme import Theme
frame = CTkFrame(parent, fg_color=Theme.BG_CARD)
"""


class Theme:
    """Design tokens for the AegisAI warm-mode interface."""

    # ── Background Colors ──────────────────────────────────────────────
    BG_DARK    = "#1A1A2E"    # App root — very dark navy (keeps contrast)
    BG_SIDEBAR = "#16213E"    # Left sidebar — deep navy
    BG_CARD    = "#1F2B47"    # Cards, panels — slightly lighter navy
    BG_INPUT   = "#253354"    # Input fields — medium navy
    BG_HOVER   = "#2A3A5C"    # Hover state backgrounds
    BG_ACTIVE  = "#1E2F50"    # Active/selected nav item
    BG_HEADER  = "#0F1930"    # Top header bar — darkest navy

    # ── Accent & Semantic Colors (Warm Orange / Amber palette) ────────
    ACCENT        = "#F59E0B"   # Primary amber/orange
    ACCENT_HOVER  = "#FBBF24"   # Hover on accent — lighter amber
    ACCENT_MUTED  = "#D97706"   # Darker amber for active indicator

    SUCCESS       = "#10B981"   # Emerald green — low risk, positive
    SUCCESS_BG    = "#064E3B"   # Success background tint
    WARNING       = "#F59E0B"   # Amber — medium risk (same as accent)
    WARNING_BG    = "#451A03"   # Warning background tint
    DANGER        = "#EF4444"   # Red — high risk, error
    DANGER_BG     = "#450A0A"   # Danger background tint
    CRITICAL      = "#FF2D55"   # Critical emergency — vivid red-pink
    CRITICAL_BG   = "#3B0014"   # Critical background tint

    # ── Text Colors ───────────────────────────────────────────────────
    TEXT_PRIMARY   = "#F1F5F9"   # Main body text — near-white
    TEXT_SECONDARY = "#94A3B8"   # Labels, secondary info — soft gray-blue
    TEXT_MUTED     = "#64748B"   # Timestamps, placeholder text
    TEXT_ACCENT    = "#FBBF24"   # Highlighted / link text — amber
    TEXT_DANGER    = "#FCA5A5"   # Error text — soft red

    # ── Border Colors ─────────────────────────────────────────────────
    BORDER        = "#2D3F6B"   # Card and panel borders
    BORDER_ACCENT = "#D97706"   # Active state borders — amber
    BORDER_DANGER = "#EF4444"   # Emergency / error borders

    # ── Risk Level Colors (matches models/assessment.py RiskLevel) ────
    RISK_COLORS = {
        "UNKNOWN":  "#64748B",
        "LOW":      "#10B981",
        "MEDIUM":   "#F59E0B",
        "HIGH":     "#EF4444",
        "CRITICAL": "#FF2D55",
    }

    # ── Fonts ─────────────────────────────────────────────────────────
    # Prefer "Segoe UI" (Windows) then fallback to system sans-serif
    FONT_FAMILY   = "Segoe UI"

    FONT_HERO     = ("Segoe UI", 24, "bold")
    FONT_TITLE    = ("Segoe UI", 17, "bold")
    FONT_SUBTITLE = ("Segoe UI", 13, "bold")
    FONT_BODY     = ("Segoe UI", 12)
    FONT_SMALL    = ("Segoe UI", 11)
    FONT_TINY     = ("Segoe UI", 10)
    FONT_MONO     = ("Consolas", 11)

    # Chat-specific fonts
    FONT_CHAT_MSG  = ("Segoe UI", 12)
    FONT_CHAT_TIME = ("Segoe UI", 10)
    FONT_CHIP      = ("Segoe UI", 11)

    # ── Spacing & Geometry ────────────────────────────────────────────
    SIDEBAR_W   = 190       # Sidebar width px (reduced ~20%)
    HEADER_H    = 52        # Header height px
    RADIUS      = 8         # Default corner radius
    RADIUS_SM   = 5         # Small corner radius (chips, badges)
    RADIUS_LG   = 12        # Large corner radius (cards)
    PAD         = 14        # Standard padding
    PAD_SM      = 7         # Small padding
    PAD_LG      = 20        # Large padding
    CARD_PAD    = 16        # Inner card padding

    # ── Icon Map ─────────────────────────────────────────────────────
    # Emoji icons for sidebar navigation items
    NAV_ICONS = {
        "dashboard":     "🏠",
        "awareness":     "📚",
        "assessment":    "🛡️",
        "scam_analyzer": "🔍",
        "emergency":     "🆘",
        "resources":     "📁",
    }

    NAV_LABELS = {
        "dashboard":     "Dashboard",
        "awareness":     "Awareness",
        "assessment":    "Risk Assessment",
        "scam_analyzer": "Scam Analyzer",
        "emergency":     "Emergency Help",
        "resources":     "Resources",
    }

    # ── Sidebar Nav Order ─────────────────────────────────────────────
    NAV_ORDER = [
        "dashboard",
        "awareness",
        "assessment",
        "scam_analyzer",
        "emergency",
        "resources",
    ]
