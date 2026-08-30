"""Qt stylesheet and presentation tokens for the final desktop application."""

COLORS = {
    "background": "#F5F7FA",
    "surface": "#FFFFFF",
    "surface_subtle": "#F9FAFB",
    "sidebar": "#111827",
    "sidebar_muted": "#9CA3AF",
    "text": "#172033",
    "muted": "#667085",
    "border": "#E4E7EC",
    "accent": "#2563EB",
    "accent_hover": "#1D4ED8",
    "accent_soft": "#EFF6FF",
    "locked": "#9A6700",
    "locked_bg": "#FFFAEB",
    "locked_border": "#FEDF89",
    "success": "#067647",
    "success_bg": "#ECFDF3",
    "danger": "#B42318",
    "danger_bg": "#FEF3F2",
}


def application_stylesheet() -> str:
    return f"""
    * {{
        font-family: "Segoe UI", "Inter", sans-serif;
        font-size: 13px;
        color: {COLORS['text']};
    }}
    QMainWindow, QWidget#AppRoot {{ background: {COLORS['background']}; }}
    QWidget#Sidebar {{ background: {COLORS['sidebar']}; }}
    QLabel#Brand {{ color: #FFFFFF; font-size: 17px; font-weight: 700; }}
    QLabel#BrandSubtitle {{ color: {COLORS['sidebar_muted']}; font-size: 11px; }}
    QPushButton#NavButton {{
        border: 0; border-radius: 7px; padding: 10px 12px;
        text-align: left; color: #D1D5DB; background: transparent;
        font-weight: 500;
    }}
    QPushButton#NavButton:hover {{ background: #1F2937; color: #FFFFFF; }}
    QPushButton#NavButton:checked {{ background: #263449; color: #FFFFFF; font-weight: 650; }}
    QLabel#SidebarUtility {{ color: {COLORS['sidebar_muted']}; font-size: 11px; }}
    QScrollArea {{ border: 0; background: transparent; }}
    QWidget#Page {{ background: transparent; }}
    QLabel#PageTitle {{ font-size: 28px; font-weight: 700; color: {COLORS['text']}; }}
    QLabel#PageLead {{ font-size: 14px; color: {COLORS['muted']}; }}
    QLabel#SectionTitle {{ font-size: 16px; font-weight: 650; }}
    QLabel#SectionHint {{ color: {COLORS['muted']}; font-size: 12px; }}
    QFrame#Surface {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 10px;
    }}
    QFrame#SubtleSurface {{
        background: {COLORS['surface_subtle']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
    }}
    QFrame#LockedBanner {{
        background: {COLORS['locked_bg']};
        border: 1px solid {COLORS['locked_border']};
        border-radius: 9px;
    }}
    QLabel#LockedTitle {{ color: {COLORS['locked']}; font-weight: 700; }}
    QLabel#LockedText {{ color: #78590B; }}
    QLabel#StatusLocked {{
        color: {COLORS['locked']}; background: {COLORS['locked_bg']};
        border: 1px solid {COLORS['locked_border']}; border-radius: 9px;
        padding: 3px 8px; font-size: 11px; font-weight: 700;
    }}
    QLabel#StatusFrozen {{
        color: #175CD3; background: {COLORS['accent_soft']};
        border: 1px solid #B2DDFF; border-radius: 9px;
        padding: 3px 8px; font-size: 11px; font-weight: 700;
    }}
    QLabel#MetricValue {{ font-size: 20px; font-weight: 700; }}
    QLabel#MetricLabel {{ color: {COLORS['muted']}; font-size: 11px; }}
    QLabel#MethodName {{ font-weight: 650; font-size: 13px; }}
    QLabel#MethodConfig {{ color: {COLORS['muted']}; font-size: 11px; }}
    QLabel#MethodDescription {{ color: {COLORS['muted']}; font-size: 12px; }}
    QLabel#StageLabel {{ font-weight: 600; }}
    QLabel#StageArrow {{ color: #98A2B3; font-size: 15px; }}
    QPushButton#PrimaryButton {{
        background: {COLORS['accent']}; color: #FFFFFF; border: 0;
        border-radius: 7px; padding: 9px 14px; font-weight: 650;
    }}
    QPushButton#PrimaryButton:hover {{ background: {COLORS['accent_hover']}; }}
    QPushButton#SecondaryButton {{
        background: {COLORS['surface']}; color: {COLORS['text']};
        border: 1px solid #D0D5DD; border-radius: 7px; padding: 9px 14px;
        font-weight: 600;
    }}
    QPushButton#SecondaryButton:hover {{ background: #F9FAFB; }}
    QPushButton#LockedButton {{
        background: #F2F4F7; color: #98A2B3; border: 1px solid #EAECF0;
        border-radius: 7px; padding: 9px 14px; font-weight: 600;
    }}
    QPushButton#TextButton {{
        color: {COLORS['accent']}; background: transparent; border: 0;
        padding: 5px 0; font-weight: 600; text-align: left;
    }}
    QPushButton#TextButton:hover {{ color: {COLORS['accent_hover']}; }}
    QFrame#Divider {{ background: {COLORS['border']}; min-width: 1px; max-width: 1px; }}
    QToolTip {{
        background: #101828; color: #FFFFFF; border: 0; padding: 6px;
    }}
    """
