import pandas as pd
import streamlit as st

ALTERNATIVES = ["Candidat A", "Candidat B", "Candidat C", "Candidat D", "Candidat E"]
CRITERES = [
    "Expérience (années)",
    "Entretien (/10)",
    "Compétences requises (%)",
    "Disponibilité (jours)",
    "Prétentions salariales (€ / an)",
]
TYPES = ["max", "min", "max", "min", "min"]

DATA = [
    [6, 8.5, 92, 14, 52000],
    [3, 9.0, 88, 7, 48000],
    [8, 7.5, 95, 30, 61000],
    [5, 8.0, 83, 3, 45000],
    [2, 8.7, 90, 10, 50000],
]

ANCIENNES_ALTERNATIVES = ["Actions", "Obligations", "Mixte", "Immobilier", "Tech"]
ANCIENS_CRITERES = [
    "Rendement (%)", "Volatilité (%)", "Sharpe", "Drawdown max (%)", "Frais (%)",
]
ANCIENNES_DONNEES = [
    [12.5, 18.0, 0.58, 35, 0.8],
    [4.2, 5.5, 0.40, 12, 0.3],
    [8.1, 10.2, 0.60, 20, 0.6],
    [6.8, 8.5, 0.56, 18, 1.2],
    [16.0, 25.0, 0.56, 45, 1.0],
]


def appliquer_style():
    """Applique le thème visuel commun à toutes les pages Streamlit."""
    st.markdown(
        """
        <style>
        :root {
            --mcdm-ink: #172c3c;
            --mcdm-muted: #647987;
            --mcdm-accent: #087f75;
            --mcdm-accent-dark: #06665f;
            --mcdm-surface: #ffffff;
            --mcdm-canvas: #f5f8f8;
            --mcdm-border: #dce7e8;
            --mcdm-sidebar: #132d3b;
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(ellipse at 92% 0%, rgba(8, 127, 117, 0.09), transparent 38rem),
                linear-gradient(180deg, #f8fbfb 0%, var(--mcdm-canvas) 52rem);
            color: var(--mcdm-ink);
        }

        [data-testid="stHeader"] {
            background: rgba(248, 251, 251, 0.82);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(165deg, var(--mcdm-sidebar), #1b4549);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        [data-testid="stSidebar"] * {
            color: #eef7f5;
        }

        [data-testid="stSidebar"] [data-baseweb="radio"] > div {
            gap: 0.55rem;
        }

        [data-testid="stSidebar"] [data-baseweb="radio"] label {
            padding: 0.5rem 0.65rem;
            border-radius: 8px;
        }

        [data-testid="stSidebar"] [data-baseweb="radio"] label:hover {
            background: rgba(255, 255, 255, 0.08);
        }

        [data-testid="stMain"] .block-container {
            max-width: 1440px;
            padding-top: 2.4rem;
            padding-bottom: 3.5rem;
        }

        h1, h2, h3 {
            color: var(--mcdm-ink);
            letter-spacing: -0.035em;
        }

        h1 {
            font-weight: 760;
            line-height: 1.15;
            padding-bottom: 0.75rem;
            border-bottom: 3px solid var(--mcdm-accent);
        }

        h2, h3 {
            font-weight: 680;
        }

        h2 {
            margin-top: 1.6rem;
            padding-left: 0.75rem;
            border-left: 3px solid var(--mcdm-accent);
        }

        [data-testid="stMain"] [data-testid="stCaptionContainer"],
        [data-testid="stMain"] [data-testid="stMarkdownContainer"] p {
            color: var(--mcdm-muted);
        }

        [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stDataFrame"],
        [data-testid="stTable"] {
            border: 1px solid var(--mcdm-border);
            border-radius: 14px;
            overflow: hidden;
            background: var(--mcdm-surface);
            box-shadow: 0 8px 24px rgba(23, 44, 60, 0.055);
        }

        [data-testid="stDataEditor"] {
            border: 1px solid var(--mcdm-border);
            border-radius: 12px;
            overflow: hidden;
            background: var(--mcdm-surface);
        }

        [data-testid="stButton"] > button,
        [data-testid="stFormSubmitButton"] > button {
            min-height: 2.65rem;
            border-radius: 9px;
            font-weight: 650;
            transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease;
        }

        [data-testid="stButton"] > button[kind="primary"],
        [data-testid="stFormSubmitButton"] > button[kind="primary"] {
            background: var(--mcdm-accent);
            border-color: var(--mcdm-accent);
            color: white;
        }

        [data-testid="stButton"] > button[kind="primary"]:hover,
        [data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
            background: var(--mcdm-accent-dark);
            border-color: var(--mcdm-accent-dark);
            box-shadow: 0 6px 16px rgba(8, 127, 117, 0.22);
            transform: translateY(-1px);
        }

        [data-testid="stButton"] > button:focus-visible,
        [data-testid="stFormSubmitButton"] > button:focus-visible {
            outline: 3px solid rgba(8, 127, 117, 0.35);
            outline-offset: 2px;
        }

        [data-testid="stAlert"] {
            border-radius: 11px;
        }

        [data-testid="stSlider"] [role="slider"],
        [data-testid="stCheckbox"] [role="checkbox"] {
            accent-color: var(--mcdm-accent);
        }

        [data-testid="stRadio"] label,
        [data-testid="stSelectbox"] label,
        [data-testid="stTextInput"] label,
        [data-testid="stNumberInput"] label {
            font-weight: 560;
            color: var(--mcdm-ink);
        }

        hr {
            border-color: var(--mcdm-border);
        }

        @media (max-width: 700px) {
            [data-testid="stMain"] .block-container {
                padding: 1.4rem 1rem 2rem;
            }

            h1 {
                font-size: 1.8rem;
            }

            h2 {
                font-size: 1.25rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state():
    """Initialise la matrice et les types au premier chargement.
    À appeler au début de chaque page."""
    appliquer_style()
    if "matrice" not in st.session_state:
        m = pd.DataFrame(DATA, index=ALTERNATIVES, columns=CRITERES)
        m.index.name = "Alternative"
        st.session_state.matrice = m
        st.session_state.types = pd.Series(TYPES, index=CRITERES, name="Type")
    else:
        ancienne_matrice = pd.DataFrame(
            ANCIENNES_DONNEES,
            index=ANCIENNES_ALTERNATIVES,
            columns=ANCIENS_CRITERES,
        )
        if st.session_state.matrice.equals(ancienne_matrice):
            m = pd.DataFrame(DATA, index=ALTERNATIVES, columns=CRITERES)
            m.index.name = "Alternative"
            st.session_state.matrice = m
            st.session_state.types = pd.Series(TYPES, index=CRITERES, name="Type")
            for key in ("poids", "poids_source", "res_pond", "res_class"):
                st.session_state.pop(key, None)


def afficher_steps(res):
    for i, (titre, obj) in enumerate(res["steps"], 1):
        st.markdown(f"**Étape {i} : {titre}**")
        if isinstance(obj, (pd.DataFrame, pd.Series)):
            df = pd.DataFrame(obj)
            st.dataframe(df.style.format("{:.4f}", subset=df.select_dtypes("number").columns),
                         use_container_width=True)
        else:
            st.write(obj)