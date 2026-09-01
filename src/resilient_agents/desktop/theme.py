"""Qt stylesheet and presentation tokens for the final desktop application.

The visual language intentionally tracks the accepted historical T-528 reference
screens: white chrome, a quiet blue accent, a pale workspace and restrained
borders. Scientific state is communicated semantically rather than by turning
the whole application into a status color.
"""

COLORS = {
    "background": "#F4F7FB",
    "surface": "#FFFFFF",
    "surface_subtle": "#F8FAFD",
    "sidebar": "#FFFFFF",
    "text": "#101828",
    "muted": "#5F718F",
    "border": "#DDE3EC",
    "accent": "#245DE8",
    "accent_hover": "#184BC7",
    "accent_soft": "#EDF3FF",
    "locked": "#9A5B00",
    "locked_bg": "#FFF8EE",
    "locked_border": "#F3C47A",
    "development": "#1F5A7A",
    "development_bg": "#EEF8FC",
    "development_border": "#A9D7E8",
    "success": "#067647",
    "success_bg": "#ECFDF3",
    "danger": "#B42318",
    "danger_bg": "#FEF3F2",
}


def application_stylesheet() -> str:
    return f"""
    * {{ font-family: "Segoe UI", "Inter", sans-serif; font-size: 13px; color: {COLORS['text']}; }}
    QMainWindow, QWidget#AppRoot {{ background: {COLORS['background']}; }}

    QWidget#TopHeader {{ background: #FFFFFF; border-bottom: 1px solid {COLORS['border']}; }}
    QLabel#HeaderBrand {{ color: {COLORS['text']}; font-size: 16px; font-weight: 700; }}
    QLabel#HeaderSubtitle {{ color: {COLORS['muted']}; font-size: 11px; }}
    QLabel#HeaderPage {{ color: {COLORS['muted']}; font-size: 12px; font-weight: 600; }}
    QPushButton#HeaderHelp {{ color: {COLORS['accent']}; background: transparent; border: 0; padding: 7px 9px; font-weight: 650; }}
    QPushButton#HeaderHelp:hover {{ color: {COLORS['accent_hover']}; background: {COLORS['accent_soft']}; border-radius: 6px; }}
    QPushButton#HeaderHelp:focus {{ color: {COLORS['accent_hover']}; background: {COLORS['accent_soft']}; border: 2px solid {COLORS['accent']}; border-radius: 6px; }}
    QLabel#HeaderLock {{ color: #8A4B00; background: #FFF1DB; border: 1px solid #F4C27A; border-radius: 9px; padding: 3px 8px; font-size: 11px; font-weight: 700; }}

    QWidget#Sidebar {{ background: {COLORS['sidebar']}; border-right: 1px solid {COLORS['border']}; }}
    QLabel#SidebarSection {{ color: {COLORS['accent']}; font-size: 11px; font-weight: 750; letter-spacing: 0.5px; }}
    QPushButton#NavButton {{ border: 0; border-radius: 7px; padding: 10px 12px; text-align: left; color: #24405F; background: transparent; font-weight: 600; }}
    QPushButton#NavButton:hover {{ background: #F4F7FC; color: {COLORS['accent']}; }}
    QPushButton#NavButton:checked {{ background: {COLORS['accent_soft']}; color: {COLORS['accent']}; font-weight: 700; }}
    QPushButton#NavButton:focus {{ border: 2px solid {COLORS['accent']}; }}
    QLabel#SidebarUtility {{ color: {COLORS['muted']}; font-size: 11px; }}
    QLabel#SidebarState {{ color: #344054; font-size: 12px; padding: 2px 0; }}

    QScrollArea {{ border: 0; background: transparent; }}
    QWidget#Page {{ background: transparent; }}
    QLabel#PageEyebrow {{ color: {COLORS['accent']}; font-size: 11px; font-weight: 750; letter-spacing: 0.5px; }}
    QLabel#PageTitle {{ font-size: 28px; font-weight: 700; color: {COLORS['text']}; }}
    QLabel#PageLead {{ font-size: 14px; color: {COLORS['muted']}; }}
    QLabel#SectionTitle {{ font-size: 16px; font-weight: 700; }}
    QLabel#SectionHint {{ color: {COLORS['muted']}; font-size: 12px; }}
    QLabel#GridLegend {{ color: #3F526B; background: #F7F9FC; border: 1px solid {COLORS['border']}; border-radius: 6px; padding: 5px 8px; font-size: 11px; }}
    QPushButton#ChartToggleActive {{ color: #174EA6; background: {COLORS['accent_soft']}; border: 1px solid #B9CDF7; border-radius: 6px; padding: 5px 9px; font-weight: 650; }}
    QPushButton#ChartToggleInactive {{ color: #344054; background: {COLORS['surface']}; border: 1px solid #D0D5DD; border-radius: 6px; padding: 5px 9px; font-weight: 600; }}
    QPushButton#ChartToggleActive:focus, QPushButton#ChartToggleInactive:focus {{ border: 2px solid {COLORS['accent']}; }}

    QFrame#HeroSurface {{ background: {COLORS['surface']}; border: 1px solid {COLORS['border']}; border-radius: 16px; }}
    QFrame#Surface {{ background: {COLORS['surface']}; border: 1px solid {COLORS['border']}; border-radius: 11px; }}
    QFrame#SubtleSurface {{ background: {COLORS['surface_subtle']}; border: 1px solid {COLORS['border']}; border-radius: 8px; }}
    QFrame#ChoiceCard {{ background: {COLORS['surface']}; border: 1px solid {COLORS['border']}; border-radius: 14px; min-height: 248px; }}
    QFrame#ChoiceCard:hover {{ border-color: #B8C9E7; }}
    QFrame#ChoiceFacts {{ background: {COLORS['surface_subtle']}; border: 1px solid #E7ECF3; border-radius: 8px; }}
    QLabel#ChoiceTitle {{ color: {COLORS['text']}; font-size: 18px; font-weight: 700; }}
    QLabel#ChoiceBody {{ color: {COLORS['muted']}; font-size: 12px; }}
    QLabel#ChoiceFact {{ color: #344054; font-size: 12px; }}

    QFrame#LockedBanner {{ background: {COLORS['locked_bg']}; border: 1px solid {COLORS['locked_border']}; border-radius: 9px; }}
    QLabel#LockedTitle {{ color: #704300; font-weight: 700; }}
    QLabel#LockedText {{ color: #7A5A24; }}
    QLabel#StatusLocked {{ color: {COLORS['locked']}; background: {COLORS['locked_bg']}; border: 1px solid {COLORS['locked_border']}; border-radius: 9px; padding: 3px 8px; font-size: 11px; font-weight: 700; }}
    QLabel#StatusFrozen {{ color: #174EA6; background: {COLORS['accent_soft']}; border: 1px solid #B9CDF7; border-radius: 9px; padding: 3px 8px; font-size: 11px; font-weight: 700; }}
    QLabel#StatusDevelopment {{ color: {COLORS['development']}; background: {COLORS['development_bg']}; border: 1px solid {COLORS['development_border']}; border-radius: 9px; padding: 3px 8px; font-size: 11px; font-weight: 700; }}
    QFrame#DevelopmentBanner {{ background: {COLORS['development_bg']}; border: 1px solid {COLORS['development_border']}; border-radius: 9px; }}
    QLabel#DevelopmentTitle {{ color: #234E63; font-size: 13px; font-weight: 700; }}
    QLabel#DevelopmentText {{ color: #315B70; }}

    QPushButton#HelpDisclosure {{ color: #24405F; background: transparent; border: 0; padding: 4px 2px; text-align: left; font-weight: 650; }}
    QPushButton#HelpDisclosure:hover {{ color: {COLORS['accent']}; }}
    QPushButton#HelpDisclosure:checked {{ color: {COLORS['accent']}; }}
    QPushButton#HelpDisclosure:focus {{ color: {COLORS['accent_hover']}; border: 2px solid {COLORS['accent']}; border-radius: 5px; }}
    QLabel#HelpDetail {{ color: #3F526B; background: #F7F9FC; border: 1px solid {COLORS['border']}; border-radius: 8px; padding: 10px 12px; }}

    QLabel#StepComplete {{ color: #2F6A50; background: #EFF8F3; border: 1px solid #B8DCC7; border-radius: 8px; padding: 6px 11px; font-size: 11px; font-weight: 700; }}
    QLabel#StepCurrent {{ color: {COLORS['accent']}; background: {COLORS['accent_soft']}; border: 1px solid #B9CDF7; border-radius: 8px; padding: 6px 11px; font-size: 11px; font-weight: 750; }}
    QLabel#StepUpcoming {{ color: #667085; background: #FFFFFF; border: 1px solid {COLORS['border']}; border-radius: 8px; padding: 6px 11px; font-size: 11px; font-weight: 650; }}
    QLabel#StepArrow {{ color: #98A2B3; font-size: 13px; }}

    QFrame#ModelChoiceCard {{ background: {COLORS['surface']}; border: 1px solid {COLORS['border']}; border-radius: 11px; min-height: 124px; }}
    QFrame#ModelChoiceCard:hover {{ border-color: #B8C9E7; }}
    QCheckBox#ModelChoiceCheck {{ color: {COLORS['text']}; font-size: 14px; font-weight: 700; spacing: 8px; }}
    QCheckBox#ModelChoiceCheck::indicator {{ width: 16px; height: 16px; }}
    QCheckBox#ModelChoiceCheck:focus {{ background: {COLORS['accent_soft']}; border: 2px solid {COLORS['accent']}; border-radius: 5px; }}
    QLabel#ModelChoiceConfig {{ color: {COLORS['accent']}; font-size: 11px; font-weight: 600; }}

    QLabel#ReviewLabel {{ color: {COLORS['muted']}; font-size: 11px; font-weight: 650; }}
    QLabel#ReviewValue {{ color: #1D2939; font-size: 13px; font-weight: 650; }}

    QLabel#MetricValue {{ font-size: 20px; font-weight: 700; }}
    QLabel#MetricLabel {{ color: {COLORS['muted']}; font-size: 11px; }}
    QLabel#MethodName {{ font-weight: 650; font-size: 13px; }}
    QLabel#MethodConfig {{ color: {COLORS['muted']}; font-size: 11px; }}
    QLabel#MethodDescription {{ color: {COLORS['muted']}; font-size: 12px; }}
    QLabel#StageLabel {{ font-weight: 600; }}
    QLabel#StageArrow {{ color: #8FA2BA; font-size: 15px; }}
    QLabel#ErrorText {{ color: {COLORS['danger']}; background: {COLORS['danger_bg']}; border: 1px solid #FECDCA; border-radius: 7px; padding: 9px 11px; }}

    QPushButton#PrimaryButton {{ background: {COLORS['accent']}; color: #FFFFFF; border: 0; border-radius: 7px; padding: 9px 14px; font-weight: 650; }}
    QPushButton#PrimaryButton:hover {{ background: {COLORS['accent_hover']}; }}
    QPushButton#PrimaryButton:focus {{ border: 2px solid {COLORS['text']}; }}
    QPushButton#PrimaryButton:disabled {{ background: #D7DFED; color: #FFFFFF; }}
    QPushButton#SecondaryButton {{ background: {COLORS['surface']}; color: #263B56; border: 1px solid #C8D2E1; border-radius: 7px; padding: 9px 14px; font-weight: 600; }}
    QPushButton#SecondaryButton:hover {{ color: {COLORS['accent']}; border-color: #AFC3EE; background: #F8FAFF; }}
    QPushButton#SecondaryButton:focus {{ color: {COLORS['accent_hover']}; border: 2px solid {COLORS['accent']}; background: #F8FAFF; }}
    QPushButton#LockedButton {{ background: #F5F7FA; color: #98A2B3; border: 1px solid #E1E6ED; border-radius: 7px; padding: 9px 14px; font-weight: 600; }}
    QPushButton#TextButton {{ color: {COLORS['accent']}; background: transparent; border: 0; padding: 5px 0; font-weight: 600; text-align: left; }}
    QPushButton#TextButton:hover {{ color: {COLORS['accent_hover']}; }}
    QPushButton#TextButton:focus {{ color: {COLORS['accent_hover']}; border: 2px solid {COLORS['accent']}; border-radius: 5px; }}

    QLineEdit#StudyLabelInput, QComboBox#ScopeCombo {{ background: {COLORS['surface']}; border: 1px solid #C8D2E1; border-radius: 7px; padding: 8px 10px; min-height: 18px; }}
    QLineEdit#StudyLabelInput:focus, QComboBox#ScopeCombo:focus {{ border: 2px solid {COLORS['accent']}; }}

    QFrame#Divider {{ background: {COLORS['border']}; min-width: 1px; max-width: 1px; }}
    QTableWidget#StudyTable, QTableWidget#ArtifactTable {{ background: {COLORS['surface']}; border: 1px solid {COLORS['border']}; border-radius: 9px; selection-background-color: {COLORS['accent_soft']}; selection-color: {COLORS['text']}; outline: 0; }}
    QTableWidget#StudyTable:focus, QTableWidget#ArtifactTable:focus, QTableWidget#ResultsTable:focus {{ border: 2px solid {COLORS['accent']}; }}
    QTableWidget#StudyTable::item, QTableWidget#ArtifactTable::item {{ border-bottom: 1px solid #F0F2F5; padding: 7px 6px; }}
    QHeaderView::section {{ background: #F8FAFC; color: {COLORS['muted']}; border: 0; border-bottom: 1px solid {COLORS['border']}; padding: 8px 6px; font-size: 11px; font-weight: 650; }}
    QProgressBar {{ border: 1px solid #D0D5DD; border-radius: 6px; background: #F2F4F7; text-align: center; min-height: 18px; color: {COLORS['text']}; }}
    QProgressBar::chunk {{ background: #84ADFF; border-radius: 5px; }}
    QComboBox {{ background: {COLORS['surface']}; border: 1px solid #D0D5DD; border-radius: 7px; padding: 7px 10px; }}
    QComboBox:focus {{ border: 2px solid {COLORS['accent']}; }}
    QToolTip {{ background: #253247; color: #FFFFFF; border: 0; padding: 7px 9px; }}
    """
