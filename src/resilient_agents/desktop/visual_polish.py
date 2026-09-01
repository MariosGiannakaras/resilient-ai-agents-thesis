"""Final bounded visual-polish overrides for the experiment-first desktop UI.

These rules refine spacing, typography and hierarchy only. They intentionally
reuse the accepted palette and do not encode scientific state or behavior.
"""


def visual_polish_stylesheet() -> str:
    return """
    QLabel#PageTitle { font-size: 30px; font-weight: 720; }
    QLabel#PageLead { color: #52647D; font-size: 14px; line-height: 1.25; }
    QLabel#SectionTitle { color: #101828; font-size: 17px; font-weight: 720; }
    QLabel#SectionHint { color: #536781; font-size: 13px; }
    QLabel#ReviewLabel { color: #536781; font-size: 12px; font-weight: 650; }
    QLabel#ReviewValue { color: #1D2939; font-size: 14px; font-weight: 680; }
    QLabel#MethodDescription { color: #536781; font-size: 13px; }
    QLabel#MethodConfig { color: #536781; font-size: 12px; }
    QLabel#HeaderSubtitle { color: #536781; font-size: 12px; }
    QLabel#SidebarState { color: #344054; font-size: 12px; line-height: 1.2; }

    QFrame#HeroSurface { border-color: #D7E0EB; }
    QFrame#Surface { border-color: #D7E0EB; }
    QFrame#SubtleSurface { background: #F7F9FC; border-color: #E0E6EF; }

    QLabel#CurrentMethod {
        color: #173F98;
        background: #EDF3FF;
        border: 1px solid #B9CDF7;
        border-radius: 7px;
        padding: 6px 9px;
        font-size: 13px;
        font-weight: 720;
    }
    QLabel#MethodStatus {
        color: #344054;
        background: #F7F9FC;
        border: 1px solid #DDE3EC;
        border-radius: 7px;
        padding: 4px 7px;
        font-size: 12px;
        font-weight: 620;
    }
    QLabel#CurrentMethodStatus {
        color: #174EA6;
        background: #EDF3FF;
        border: 1px solid #B9CDF7;
        border-radius: 7px;
        padding: 4px 7px;
        font-size: 12px;
        font-weight: 720;
    }

    QTableWidget#ResultsTable {
        background: #FFFFFF;
        border: 1px solid #D7E0EB;
        border-radius: 9px;
        selection-background-color: #EDF3FF;
        selection-color: #101828;
        outline: 0;
    }
    QTableWidget#ResultsTable::item { border-bottom: 1px solid #F0F2F5; padding: 7px 6px; }
    """
