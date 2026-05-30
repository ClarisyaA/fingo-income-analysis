"""
Fingo Dashboard — CC26-PSU217
Professional Income Predictor & Impulsive Detector
"""

import os, json, pickle, warnings
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
from scipy.stats import mannwhitneyu

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fingo — Financial Intelligence Platform",
    page_icon="assets/favicon.ico" if os.path.exists("assets/favicon.ico") else None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display:ital@0;1&display=swap');

/* ── Root Variables ── */
:root {
    --fingo-green:   #00C471;
    --fingo-dark:    #0B0F0E;
    --fingo-surface: #111714;
    --fingo-card:    #161D1A;
    --fingo-border:  #1E2B25;
    --fingo-text:    #E8EDE9;
    --fingo-muted:   #6B7E74;
    --fingo-accent:  #00E882;
    --fingo-warn:    #F5A623;
    --fingo-danger:  #E8504A;
}

/* ── Base Typography ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--fingo-text);
}

/* ── App Background ── */
.stApp {
    background-color: var(--fingo-dark);
}
.block-container {
    padding: 2rem 2.5rem 3rem;
    max-width: 1400px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--fingo-surface);
    border-right: 1px solid var(--fingo-border);
}
[data-testid="stSidebar"] * {
    color: var(--fingo-text) !important;
}
[data-testid="stSidebarContent"] {
    padding: 1.5rem 1.2rem;
}

/* ── Radio as Nav ── */
[data-testid="stSidebar"] .stRadio > label {
    display: none;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 4px;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    display: flex !important;
    align-items: center;
    padding: 10px 14px;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.15s ease;
    font-size: 0.9rem;
    font-weight: 500;
    border: 1px solid transparent;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: var(--fingo-border);
}
[data-testid="stSidebar"] .stRadio [aria-checked="true"] + label,
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: rgba(0, 196, 113, 0.12);
    border-color: rgba(0, 196, 113, 0.3);
    color: var(--fingo-accent) !important;
}

/* ── Page Title ── */
.page-header {
    border-bottom: 1px solid var(--fingo-border);
    padding-bottom: 1.2rem;
    margin-bottom: 2rem;
}
.page-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    font-weight: 400;
    color: var(--fingo-text);
    margin: 0 0 4px 0;
    line-height: 1.2;
}
.page-header p {
    color: var(--fingo-muted);
    font-size: 0.9rem;
    margin: 0;
}

/* ── Metric Cards ── */
.metric-grid {
    display: grid;
    gap: 1rem;
    margin-bottom: 2rem;
}
.metric-card {
    background: var(--fingo-card);
    border: 1px solid var(--fingo-border);
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
}
.metric-card .label {
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--fingo-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}
.metric-card .value {
    font-size: 1.6rem;
    font-weight: 600;
    color: var(--fingo-text);
    line-height: 1;
}
.metric-card .delta {
    font-size: 0.8rem;
    margin-top: 4px;
}
.delta-up   { color: var(--fingo-green); }
.delta-down { color: var(--fingo-danger); }
.delta-neutral { color: var(--fingo-muted); }

/* ── Section Headers ── */
.section-header {
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--fingo-muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 1.8rem 0 0.8rem;
}

/* ── Cards / Panels ── */
.panel {
    background: var(--fingo-card);
    border: 1px solid var(--fingo-border);
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.panel h3 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem;
    font-weight: 400;
    margin: 0 0 0.5rem 0;
    color: var(--fingo-text);
}
.panel p {
    color: var(--fingo-muted);
    font-size: 0.88rem;
    line-height: 1.6;
    margin: 0;
}

/* ── Status Badges ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 100px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.badge-green  { background: rgba(0,196,113,0.15); color: var(--fingo-green); border: 1px solid rgba(0,196,113,0.3); }
.badge-yellow { background: rgba(245,166,35,0.12); color: var(--fingo-warn);  border: 1px solid rgba(245,166,35,0.3); }
.badge-red    { background: rgba(232,80,74,0.12);  color: var(--fingo-danger);border: 1px solid rgba(232,80,74,0.3); }
.badge-gray   { background: rgba(107,126,116,0.15);color: var(--fingo-muted); border: 1px solid var(--fingo-border); }

/* ── Table overrides ── */
.stDataFrame {
    border-radius: 8px;
    overflow: hidden;
}
[data-testid="stDataFrame"] {
    border: 1px solid var(--fingo-border) !important;
    border-radius: 8px;
}

/* ── Form elements ── */
.stNumberInput input, .stSelectbox select, .stTextInput input {
    background: var(--fingo-card) !important;
    border: 1px solid var(--fingo-border) !important;
    border-radius: 7px !important;
    color: var(--fingo-text) !important;
}
.stButton button {
    border-radius: 8px !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
}
.stButton button[kind="primary"] {
    background: var(--fingo-green) !important;
    border: none !important;
    color: #000 !important;
}
.stButton button[kind="primary"]:hover {
    background: var(--fingo-accent) !important;
}

/* ── Streamlit default metric ── */
[data-testid="metric-container"] {
    background: var(--fingo-card);
    border: 1px solid var(--fingo-border);
    border-radius: 10px;
    padding: 1rem 1.2rem !important;
}
[data-testid="metric-container"] label {
    color: var(--fingo-muted) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--fingo-text) !important;
    font-size: 1.5rem !important;
}

/* ── Alerts ── */
.stAlert {
    border-radius: 8px !important;
    border: none !important;
}
.stSuccess { background: rgba(0,196,113,0.08) !important; border-left: 3px solid var(--fingo-green) !important; }
.stWarning { background: rgba(245,166,35,0.08) !important; border-left: 3px solid var(--fingo-warn) !important; }
.stInfo    { background: rgba(107,126,116,0.1) !important;  border-left: 3px solid var(--fingo-muted) !important; }
.stError   { background: rgba(232,80,74,0.08)  !important; border-left: 3px solid var(--fingo-danger) !important; }

/* ── Tab overrides ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: var(--fingo-card);
    border: 1px solid var(--fingo-border);
    border-radius: 8px;
    padding: 3px;
    width: fit-content;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px;
    padding: 6px 16px;
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--fingo-muted) !important;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    background: var(--fingo-border) !important;
    color: var(--fingo-text) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.5rem;
}

/* ── Dividers ── */
hr {
    border: none;
    border-top: 1px solid var(--fingo-border);
    margin: 1.5rem 0;
}

/* ── Matplotlib background ── */
.stImage img {
    border-radius: 8px;
    border: 1px solid var(--fingo-border);
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--fingo-card) !important;
    border: 1px solid var(--fingo-border) !important;
    border-radius: 8px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    color: var(--fingo-text) !important;
}
.streamlit-expanderContent {
    background: var(--fingo-card) !important;
    border: 1px solid var(--fingo-border) !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
}

/* ── Progress bar ── */
.stProgress > div > div {
    background: var(--fingo-green) !important;
}

/* ── Sidebar logo area ── */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 0 1.2rem 0;
    border-bottom: 1px solid var(--fingo-border);
    margin-bottom: 1.2rem;
}
.sidebar-brand .brand-icon {
    width: 36px;
    height: 36px;
    background: var(--fingo-green);
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    font-weight: 700;
    color: #000;
    flex-shrink: 0;
}
.sidebar-brand .brand-name {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: var(--fingo-text);
    font-weight: 400;
    line-height: 1;
}
.sidebar-brand .brand-sub {
    font-size: 0.7rem;
    color: var(--fingo-muted);
    margin-top: 2px;
}
.sidebar-nav-label {
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--fingo-muted);
    margin: 1rem 0 0.5rem 2px;
}
.sidebar-divider {
    border-top: 1px solid var(--fingo-border);
    margin: 1rem 0;
}
.sidebar-meta {
    font-size: 0.73rem;
    color: var(--fingo-muted);
    line-height: 1.7;
}
.sidebar-meta strong {
    color: var(--fingo-text);
}

/* ── Prediction result card ── */
.result-card {
    background: linear-gradient(135deg, rgba(0,196,113,0.08) 0%, rgba(0,196,113,0.03) 100%);
    border: 1px solid rgba(0,196,113,0.25);
    border-radius: 12px;
    padding: 1.6rem 2rem;
    margin: 1.5rem 0;
}
.result-card .result-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--fingo-green);
    margin-bottom: 0.5rem;
}
.result-card .result-value {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    color: var(--fingo-text);
    line-height: 1;
    margin-bottom: 0.4rem;
}
.result-card .result-sub {
    font-size: 0.85rem;
    color: var(--fingo-muted);
}

/* ── Budget allocation bars ── */
.budget-bar-wrap {
    margin: 0.6rem 0;
}
.budget-bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.83rem;
    margin-bottom: 4px;
    color: var(--fingo-text);
}
.budget-bar-track {
    height: 8px;
    background: var(--fingo-border);
    border-radius: 100px;
    overflow: hidden;
}
.budget-bar-fill {
    height: 100%;
    border-radius: 100px;
    transition: width 0.6s ease;
}

/* ── Coming soon ── */
.coming-soon-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 420px;
    text-align: center;
    padding: 3rem;
}
.coming-soon-badge {
    display: inline-block;
    background: rgba(245,166,35,0.1);
    border: 1px solid rgba(245,166,35,0.3);
    color: var(--fingo-warn);
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    padding: 4px 14px;
    border-radius: 100px;
    margin-bottom: 1.2rem;
}
.coming-soon-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    font-weight: 400;
    color: var(--fingo-text);
    margin-bottom: 1rem;
    line-height: 1.2;
}
.coming-soon-desc {
    color: var(--fingo-muted);
    font-size: 1rem;
    max-width: 480px;
    line-height: 1.7;
    margin-bottom: 2rem;
}

/* ── Overview pipeline step ── */
.pipeline-step {
    display: flex;
    gap: 14px;
    padding: 12px 0;
    border-bottom: 1px solid var(--fingo-border);
    align-items: flex-start;
}
.pipeline-step:last-child { border-bottom: none; }
.pipeline-num {
    flex-shrink: 0;
    width: 28px;
    height: 28px;
    background: var(--fingo-border);
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--fingo-muted);
}
.pipeline-info .pi-name {
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--fingo-text);
}
.pipeline-info .pi-out {
    font-size: 0.78rem;
    color: var(--fingo-muted);
    margin-top: 2px;
    font-family: 'Courier New', monospace;
}

/* ── KV info row ── */
.kv-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid var(--fingo-border);
    font-size: 0.85rem;
}
.kv-row:last-child { border-bottom: none; }
.kv-key { color: var(--fingo-muted); }
.kv-val { color: var(--fingo-text); font-weight: 500; font-family: 'Courier New', monospace; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MATPLOTLIB DARK THEME
# ─────────────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#161D1A",
    "axes.facecolor":   "#161D1A",
    "axes.edgecolor":   "#1E2B25",
    "axes.labelcolor":  "#6B7E74",
    "xtick.color":      "#6B7E74",
    "ytick.color":      "#6B7E74",
    "text.color":       "#E8EDE9",
    "grid.color":       "#1E2B25",
    "grid.alpha":       1.0,
    "axes.grid":        True,
    "grid.linewidth":   0.6,
    "figure.dpi":       120,
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "axes.titlepad":    12,
    "axes.titlesize":   11,
    "axes.titleweight": "bold",
    "axes.titlecolor":  "#E8EDE9",
    "axes.labelsize":   9,
    "font.family":      "sans-serif",
    "savefig.facecolor":"#161D1A",
    "savefig.edgecolor":"none",
})

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
FINGO_GREEN  = "#00C471"
FINGO_ACCENT = "#00E882"
FINGO_WARN   = "#F5A623"
FINGO_DANGER = "#E8504A"
FINGO_BLUE   = "#4A9EE8"
FINGO_MUTED  = "#6B7E74"

ORDERED_GIG_TYPES = [
    "ojek_online", "kurir", "jualan_online", "freelance_desain",
    "freelance_it", "content_creator", "tutor", "pekerja_harian",
]
GIG_LABELS = {
    "ojek_online":       "Ojek Online",
    "kurir":             "Kurir",
    "jualan_online":     "Jualan Online",
    "freelance_desain":  "Freelance Desain",
    "freelance_it":      "Freelance IT",
    "content_creator":   "Content Creator",
    "tutor":             "Tutor",
    "pekerja_harian":    "Pekerja Harian",
}

GIG_ICONS = {
    "ojek_online":       "Transportasi",
    "kurir":             "Logistik",
    "jualan_online":     "E-Commerce",
    "freelance_desain":  "Kreatif",
    "freelance_it":      "Teknologi",
    "content_creator":   "Media",
    "tutor":             "Pendidikan",
    "pekerja_harian":    "Harian",
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def fmt_idr(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "N/A"
    if val >= 1_000_000:
        return f"Rp {val/1_000_000:.2f} jt"
    if val >= 1_000:
        return f"Rp {val/1_000:.0f} rb"
    return f"Rp {val:.0f}"

def fmt_idr_short(val):
    if val >= 1_000_000:
        return f"Rp {val/1_000_000:.1f}jt"
    return f"Rp {val/1_000:.0f}rb"

BASE_DIR = os.path.dirname(__file__)

def fpath(*parts):
    return os.path.join(BASE_DIR, *parts)

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADERS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_survey():
    p = fpath("data", "processed", "survey_temporal_mapped.csv")
    if not os.path.exists(p):
        return None
    df = pd.read_csv(p)
    if "timestamp_parsed" in df.columns:
        df["timestamp_parsed"] = pd.to_datetime(df["timestamp_parsed"], errors="coerce")
    return df

@st.cache_data(show_spinner=False)
def load_survey_long():
    p = fpath("data", "processed", "survey_weekly_income_long.csv")
    if not os.path.exists(p):
        return None
    df = pd.read_csv(p)
    for c in ["period_start", "period_end"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return df

@st.cache_data(show_spinner=False)
def load_synthetic():
    p = fpath("data", "synthetic", "synthetic_52week_user_income.csv")
    if not os.path.exists(p):
        return None
    return pd.read_csv(p)

@st.cache_data(show_spinner=False)
def load_income_features():
    p = fpath("data", "processed", "income_features.csv")
    if not os.path.exists(p):
        return None
    return pd.read_csv(p)

@st.cache_data(show_spinner=False)
def load_predictions_test():
    p = fpath("outputs", "model_results", "predictions_test.csv")
    if not os.path.exists(p):
        return None
    return pd.read_csv(p)

@st.cache_data(show_spinner=False)
def load_regression_metrics():
    p = fpath("outputs", "model_results", "regression_metrics.csv")
    if not os.path.exists(p):
        return None
    return pd.read_csv(p)

@st.cache_data(show_spinner=False)
def load_classification_metrics():
    p = fpath("outputs", "model_results", "classification_metrics.csv")
    if not os.path.exists(p):
        return None
    return pd.read_csv(p)

@st.cache_data(show_spinner=False)
def load_model_contract():
    p = fpath("outputs", "model_contract", "model_contract.json")
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)

@st.cache_data(show_spinner=False)
def load_feature_columns():
    p = fpath("outputs", "model_contract", "feature_columns.json")
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)

@st.cache_data(show_spinner=False)
def load_data_dictionary():
    for p in [fpath("outputs", "dashboard", "data_dictionary.csv"),
               fpath("outputs", "reports", "data_dictionary.csv")]:
        if os.path.exists(p):
            return pd.read_csv(p)
    return None

@st.cache_resource(show_spinner=False)
def load_models():
    reg_path    = fpath("outputs", "model_results", "best_income_regressor.pkl")
    cls_path    = fpath("outputs", "model_results", "best_direction_classifier.pkl")
    scaler_path = fpath("outputs", "model_contract", "income_scalers.pkl")
    reg = cls = scalers = None
    if os.path.exists(reg_path):
        with open(reg_path, "rb") as f:   reg     = pickle.load(f)
    if os.path.exists(cls_path):
        with open(cls_path, "rb") as f:   cls     = pickle.load(f)
    if os.path.exists(scaler_path):
        with open(scaler_path, "rb") as f: scalers = pickle.load(f)
    return reg, cls, scalers

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-icon">F</div>
        <div>
            <div class="brand-name">Fingo</div>
            <div class="brand-sub">Financial Intelligence Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-nav-label">Module</div>', unsafe_allow_html=True)

    module = st.radio(
        "module",
        ["Income Predictor", "Impulsive Detector"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # Quick stats
    df_survey_sb = load_survey()
    df_synth_sb  = load_synthetic()
    mc_sb        = load_model_contract()

    n_resp  = len(df_survey_sb) if df_survey_sb is not None else 0
    n_users = df_synth_sb["synthetic_user_id"].nunique() if (df_synth_sb is not None and "synthetic_user_id" in df_synth_sb.columns) else 0

    st.markdown(f"""
    <div class="sidebar-meta">
        <div class="kv-row"><span class="kv-key">Responden Survey</span><span class="kv-val">{n_resp:,}</span></div>
        <div class="kv-row"><span class="kv-key">Synthetic Users</span><span class="kv-val">{n_users:,}</span></div>
        <div class="kv-row"><span class="kv-key">Tim</span><span class="kv-val">CC26-PSU217</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-meta" style="font-size:0.7rem">DS2: Clarisya Adeline<br>Coding Camp 2026 — DBS Foundation<br><br>© 2026 Fingo Team</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: render no-data placeholder
# ─────────────────────────────────────────────────────────────────────────────
def no_data_card(msg: str):
    st.markdown(f"""
    <div style="background:var(--fingo-card);border:1px dashed var(--fingo-border);border-radius:10px;
                padding:2rem;text-align:center;color:var(--fingo-muted);font-size:0.88rem;">
        {msg}
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE: INCOME PREDICTOR
# ══════════════════════════════════════════════════════════════════════════════
if module == "Income Predictor":

    sub_tabs = st.tabs([
        "Overview",
        "Data & Tren",
        "Prediksi Pendapatan",
        "Hasil A/B Testing",
        "Referensi Data",
    ])

    # ─────────────────────────────────────────────
    # TAB: OVERVIEW
    # ─────────────────────────────────────────────
    with sub_tabs[0]:
        st.markdown("""
        <div class="page-header">
            <h1>Income Predictor</h1>
            <p>Sistem prediksi pendapatan mingguan berbasis AI untuk gig worker Indonesia</p>
        </div>
        """, unsafe_allow_html=True)

        df_s  = load_survey()
        df_sy = load_synthetic()
        mc    = load_model_contract()
        reg_m, cls_m, _ = load_models()

        model_ready = reg_m is not None and cls_m is not None

        # Status banner
        if model_ready:
            st.success("Model siap digunakan. Buka tab **Prediksi Pendapatan** untuk mencoba.", icon=None)
        else:
            st.warning("Model belum tersedia. Jalankan Notebook 09 untuk melatih model terlebih dahulu.", icon=None)

        # KPI row
        n_resp_ov  = len(df_s) if df_s is not None else 0
        n_users_ov = df_sy["synthetic_user_id"].nunique() if (df_sy is not None and "synthetic_user_id" in df_sy.columns) else 0
        n_rows_ov  = len(df_sy) if df_sy is not None else 0

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Responden Survey", f"{n_resp_ov:,}")
        with c2:
            st.metric("Synthetic Users", f"{n_users_ov:,}")
        with c3:
            st.metric("Total Data Rows", f"{n_rows_ov:,}")

        st.markdown("<hr>", unsafe_allow_html=True)

        col_l, col_r = st.columns([1, 1], gap="large")

        with col_l:
            st.markdown('<div class="section-header">Tentang Modul Ini</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="panel">
                <h3>Apa itu Income Predictor?</h3>
                <p>Income Predictor adalah modul AI yang membantu gig worker &mdash; seperti pengemudi ojek online, 
                kurir, freelancer, dan pedagang online &mdash; untuk <strong style="color:#E8EDE9">memperkirakan 
                berapa pendapatan mereka minggu depan</strong>.</p>
                <br>
                <p>Dengan prediksi ini, pengguna dapat merencanakan pengeluaran lebih baik meski pendapatan 
                tidak pasti setiap minggunya.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-header">Pertanyaan Penelitian</div>', unsafe_allow_html=True)
            for q in [
                ("Seberapa akurat model prediksi?", "Model diuji dengan data 52 minggu per user untuk mengukur error prediksi (MAE, RMSE, MAPE)."),
                ("Fitur apa yang paling penting?", "Riwayat 4 minggu terakhir, tren, volatilitas, dan faktor musiman seperti Ramadan."),
                ("Apakah lebih baik dari manual?", "A/B Testing membuktikan error budget turun signifikan vs perencanaan manual."),
            ]:
                st.markdown(f"""
                <div style="padding: 10px 0; border-bottom: 1px solid var(--fingo-border);">
                    <div style="font-size:0.85rem;font-weight:600;color:var(--fingo-text);margin-bottom:3px;">{q[0]}</div>
                    <div style="font-size:0.8rem;color:var(--fingo-muted);">{q[1]}</div>
                </div>
                """, unsafe_allow_html=True)

        with col_r:
            st.markdown('<div class="section-header">Alur Pipeline</div>', unsafe_allow_html=True)
            steps = [
                ("01", "Data Preparation",       "survey_clean.csv"),
                ("02", "Temporal Mapping",        "survey_temporal_mapped.csv"),
                ("03", "EDA Survey",              "charts + insight"),
                ("04", "Synthetic Data (52w)",    "3.000 users × 52 minggu = 156.000 baris"),
                ("05", "Feature Engineering",     "income_features.csv + feature_columns.json"),
                ("06", "Model Dataset Split",     "train / val / test + scalers"),
                ("07", "Bias Validation",         "bias_validation_report.md"),
                ("08", "Dokumentasi",             "data_dictionary.csv + README.md"),
                ("09", "Model Training & Eval",   "best_income_regressor.pkl + metrics"),
                ("10", "A/B Testing",             "ab_testing_report.md + charts"),
            ]
            for num, name, output in steps:
                st.markdown(f"""
                <div class="pipeline-step">
                    <div class="pipeline-num">{num}</div>
                    <div class="pipeline-info">
                        <div class="pi-name">{name}</div>
                        <div class="pi-out">{output}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Preview chart
        chart_p = fpath("outputs", "charts", "regression_prediction_vs_actual.png")
        if os.path.exists(chart_p):
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">Preview Performa Model</div>', unsafe_allow_html=True)
            st.image(chart_p, caption="Actual vs Predicted Income — Model Terbaik", use_container_width=True)

    # ─────────────────────────────────────────────
    # TAB: DATA & TREN
    # ─────────────────────────────────────────────
    with sub_tabs[1]:
        st.markdown("""
        <div class="page-header">
            <h1>Data & Tren</h1>
            <p>Eksplorasi distribusi pendapatan gig worker berdasarkan data survey dan data sintetis</p>
        </div>
        """, unsafe_allow_html=True)

        df_s    = load_survey()
        df_long = load_survey_long()
        df_sy   = load_synthetic()

        if df_s is None:
            no_data_card("File <code>data/processed/survey_temporal_mapped.csv</code> belum tersedia. Jalankan Notebook 02.")
            st.stop()

        income_cols = [c for c in ["income_w1","income_w2","income_w3","income_w4"] if c in df_s.columns]

        # ── Filter bar
        if "gig_type" in df_s.columns:
            selected_gigs = st.multiselect(
                "Filter jenis pekerjaan:",
                options=ORDERED_GIG_TYPES,
                default=ORDERED_GIG_TYPES,
                format_func=lambda x: GIG_LABELS.get(x, x),
            )
            df_f = df_s[df_s["gig_type"].isin(selected_gigs)] if selected_gigs else df_s
        else:
            df_f = df_s
            selected_gigs = ORDERED_GIG_TYPES

        st.caption(f"Menampilkan {len(df_f):,} dari {len(df_s):,} responden")
        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Section 1: Distribusi
        st.markdown('<div class="section-header">Distribusi Responden</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap="large")

        with c1:
            if "gig_type" in df_f.columns:
                fig, ax = plt.subplots(figsize=(7, 4.5))
                gc = df_f["gig_type"].value_counts()
                labels = [GIG_LABELS.get(g, g) for g in gc.index]
                colors  = [FINGO_GREEN if i == 0 else FINGO_MUTED for i in range(len(gc))]
                bars = ax.barh(labels, gc.values, color=colors, alpha=0.9, height=0.65)
                for bar, val in zip(bars, gc.values):
                    ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
                            str(val), va="center", fontsize=8, color="#E8EDE9")
                ax.set_title("Jumlah Responden per Jenis Pekerjaan", color="#E8EDE9")
                ax.set_xlabel("")
                ax.invert_yaxis()
                plt.tight_layout(pad=0.8)
                st.pyplot(fig, use_container_width=True)
                plt.close()

        with c2:
            if "domisili_code" in df_f.columns:
                fig, ax = plt.subplots(figsize=(7, 4.5))
                dc = df_f["domisili_code"].value_counts().head(9)
                ax.barh(dc.index, dc.values, color=FINGO_BLUE, alpha=0.85, height=0.65)
                ax.set_title("Distribusi Domisili (Top 9)", color="#E8EDE9")
                ax.invert_yaxis()
                plt.tight_layout(pad=0.8)
                st.pyplot(fig, use_container_width=True)
                plt.close()
            else:
                no_data_card("Kolom domisili tidak tersedia di dataset.")

        # ── Section 2: Income Summary Table
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Ringkasan Pendapatan per Jenis Pekerjaan</div>', unsafe_allow_html=True)

        if income_cols and "gig_type" in df_f.columns:
            df_f = df_f.copy()
            df_f["_avg"] = df_f[income_cols].replace(0, np.nan).mean(axis=1)
            summary = df_f.groupby("gig_type").agg(
                Responden=("_avg", "count"),
                Median=("_avg", "median"),
                Rata_rata=("_avg", "mean"),
                Std=("_avg", "std"),
            ).reset_index()
            summary["Jenis Pekerjaan"] = summary["gig_type"].map(GIG_LABELS)
            summary["Kategori"]        = summary["gig_type"].map(GIG_ICONS)
            summary = summary.sort_values("Median", ascending=False)

            disp = summary[["Jenis Pekerjaan","Kategori","Responden","Median","Rata_rata","Std"]].copy()
            disp["Median"]    = disp["Median"].apply(fmt_idr)
            disp["Rata_rata"] = disp["Rata_rata"].apply(fmt_idr)
            disp["Std"]       = disp["Std"].apply(fmt_idr)
            disp.columns      = ["Jenis Pekerjaan","Kategori","n Responden","Median Mingguan","Rata-rata Mingguan","Std Dev"]
            st.dataframe(disp, use_container_width=True, hide_index=True)

            # Bar chart median income
            fig, ax = plt.subplots(figsize=(10, 4))
            sorted_s = summary.sort_values("Median", ascending=True)
            bar_colors = [FINGO_GREEN if v == sorted_s["Median"].max() else "#2A3F35" for v in sorted_s["Median"]]
            bars = ax.barh(sorted_s["Jenis Pekerjaan"], sorted_s["Median"]/1_000,
                           color=bar_colors, height=0.65, alpha=0.95)
            for bar, val in zip(bars, sorted_s["Median"].values):
                ax.text(val/1_000 + 5, bar.get_y() + bar.get_height()/2,
                        fmt_idr_short(val), va="center", fontsize=8, color="#E8EDE9")
            ax.set_title("Median Pendapatan Mingguan per Jenis Pekerjaan", color="#E8EDE9")
            ax.set_xlabel("Median (ribu Rp)")
            plt.tight_layout(pad=0.8)
            st.pyplot(fig, use_container_width=True)
            plt.close()

        # ── Section 3: Pola 4-Mingguan
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Pola Pendapatan 4 Minggu Terakhir</div>', unsafe_allow_html=True)

        col_exp = st.expander("Cara membaca grafik ini", expanded=False)
        with col_exp:
            st.markdown("""
            Data survey mengambil pendapatan **4 minggu terakhir** dari setiap responden:
            - **W4** = 4 minggu lalu (paling lama)
            - **W3** = 3 minggu lalu
            - **W2** = 2 minggu lalu
            - **W1** = minggu lalu (paling baru)

            Grafik ini menunjukkan apakah pendapatan cenderung naik, turun, atau fluktuatif dalam sebulan terakhir.
            """)

        if income_cols:
            ordered = ["income_w4","income_w3","income_w2","income_w1"]
            w_means   = [df_f[c].replace(0, np.nan).mean()   for c in ordered if c in df_f.columns]
            w_medians = [df_f[c].replace(0, np.nan).median() for c in ordered if c in df_f.columns]
            w_labels  = ["W4 (terlama)","W3","W2","W1 (terbaru)"][:len(w_means)]

            fig, ax = plt.subplots(figsize=(10, 4))
            x = np.arange(len(w_labels))
            ax.bar(x - 0.2, [v/1000 for v in w_means],   0.35, label="Rata-rata", color=FINGO_GREEN, alpha=0.85)
            ax.bar(x + 0.2, [v/1000 for v in w_medians], 0.35, label="Median",    color=FINGO_BLUE,  alpha=0.85)
            ax.set_xticks(x); ax.set_xticklabels(w_labels)
            ax.set_title("Rata-rata dan Median Pendapatan per Minggu (Semua Gig Type)", color="#E8EDE9")
            ax.set_ylabel("Income (ribu Rp)")
            ax.legend(fontsize=8)
            plt.tight_layout(pad=0.8)
            st.pyplot(fig, use_container_width=True)
            plt.close()

        # ── Section 4: Trend per gig type
        if df_long is not None and "gig_type" in df_long.columns and "relative_week" in df_long.columns:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">Tren Pendapatan per Jenis Pekerjaan</div>', unsafe_allow_html=True)

            df_long_f = df_long[df_long["gig_type"].isin(selected_gigs)] if selected_gigs else df_long
            if "weekly_income" in df_long_f.columns:
                fig, ax = plt.subplots(figsize=(10, 5))
                palette = plt.cm.tab10(np.linspace(0, 1, len(selected_gigs)))
                for i, gt in enumerate(selected_gigs):
                    sub = df_long_f[df_long_f["gig_type"] == gt].groupby("relative_week")["weekly_income"].mean()
                    if len(sub) == 0:
                        continue
                    s = sub.sort_index()
                    ax.plot([f"W{abs(r)}" for r in s.index], s.values/1000, "o-",
                            label=GIG_LABELS.get(gt, gt), linewidth=1.8,
                            markersize=5, color=palette[i])
                ax.set_title("Tren Rata-rata Pendapatan per Minggu dan Jenis Pekerjaan", color="#E8EDE9")
                ax.set_xlabel("Relative Week (W4=terlama → W1=terbaru)")
                ax.set_ylabel("Rata-rata Income (ribu Rp)")
                ax.legend(fontsize=7, ncol=2)
                plt.tight_layout(pad=0.8)
                st.pyplot(fig, use_container_width=True)
                plt.close()

        # ── Section 5: Survey vs Synthetic
        if df_sy is not None and income_cols:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">Validasi Data: Survey vs Sintetis</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="panel">
                <p>Karena data survey hanya 4 minggu per responden, kami membuat <strong style="color:#E8EDE9">data sintetis 52 minggu</strong> 
                per user berdasarkan pola distribusi yang sama. Grafik ini memvalidasi bahwa distribusi keduanya serupa.</p>
            </div>
            """, unsafe_allow_html=True)

            real_inc  = df_f[income_cols].replace(0, np.nan).values.flatten()
            real_inc  = real_inc[~np.isnan(real_inc)]
            synth_col = next((c for c in ["synthetic_weekly_income","weekly_income","income"] if c in df_sy.columns), None)

            if synth_col:
                synth_inc = df_sy[synth_col].values
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.hist(real_inc/1000, bins=50, alpha=0.55, label=f"Survey (n={len(real_inc):,})",
                        color=FINGO_BLUE, density=True)
                ax.hist(synth_inc/1000, bins=50, alpha=0.55, label=f"Sintetis (n={len(synth_inc):,})",
                        color=FINGO_GREEN, density=True)
                ax.set_title("Distribusi Income: Survey vs Sintetis 52 Minggu", color="#E8EDE9")
                ax.set_xlabel("Pendapatan Mingguan (ribu Rp)")
                ax.set_ylabel("Density")
                ax.legend(fontsize=8)
                plt.tight_layout(pad=0.8)
                st.pyplot(fig, use_container_width=True)
                plt.close()

                sample_n = min(500, len(real_inc), len(synth_inc))
                ks_s, ks_p = stats.ks_2samp(
                    np.random.choice(real_inc,  sample_n, replace=False),
                    np.random.choice(synth_inc, sample_n, replace=False),
                )
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Survey — Rata-rata", fmt_idr(np.mean(real_inc)))
                c2.metric("Sintetis — Rata-rata", fmt_idr(np.mean(synth_inc)))
                c3.metric("KS Statistic", f"{ks_s:.4f}")
                c4.metric("KS p-value", f"{ks_p:.4f}")
                st.caption("KS Test mengukur seberapa mirip kedua distribusi. Nilai KS kecil dan p-value besar berarti distribusi sangat serupa.")

        # ── Existing charts
        charts_dir = fpath("outputs", "charts")
        chart_keys = [
            ("feature_importance_best_model.png", "Fitur Terpenting dalam Model"),
            ("regression_residual_distribution.png", "Distribusi Error Prediksi"),
        ]
        avail = [(n, l) for n, l in chart_keys if os.path.exists(os.path.join(charts_dir, n))]
        if avail:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">Chart dari Analisis Model</div>', unsafe_allow_html=True)
            cols = st.columns(len(avail))
            for col, (n, l) in zip(cols, avail):
                with col:
                    st.image(os.path.join(charts_dir, n), caption=l, use_container_width=True)

    # ─────────────────────────────────────────────
    # TAB: PREDIKSI PENDAPATAN
    # ─────────────────────────────────────────────
    with sub_tabs[2]:
        st.markdown("""
        <div class="page-header">
            <h1>Prediksi Pendapatan</h1>
            <p>Masukkan riwayat pendapatan 4 minggu terakhir untuk mendapatkan estimasi minggu depan</p>
        </div>
        """, unsafe_allow_html=True)

        reg_model, cls_model, scalers = load_models()
        df_reg_m = load_regression_metrics()
        df_cls_m = load_classification_metrics()
        feat_meta   = load_feature_columns()
        FEATURE_COLS = feat_meta.get("feature_columns", []) if feat_meta else []

        model_ok = reg_model is not None and cls_model is not None

        # ── Model Performance Summary
        st.markdown('<div class="section-header">Performa Model Saat Ini</div>', unsafe_allow_html=True)

        if not model_ok:
            st.info("Model belum dimuat. Jalankan Notebook 09 untuk melatih model. Anda tetap bisa mencoba estimasi sederhana di bawah.")

        col_perf_r, col_perf_c = st.columns(2, gap="large")

        with col_perf_r:
            st.markdown("""
            <div class="panel">
                <h3>Prediksi Nominal (Regresi)</h3>
                <p>Seberapa dekat prediksi angka Rupiah dengan pendapatan aktual</p>
            </div>
            """, unsafe_allow_html=True)
            if df_reg_m is not None:
                test_r = df_reg_m[df_reg_m.get("model_name", pd.Series()).str.contains("TEST", na=False)] if "model_name" in df_reg_m.columns else pd.DataFrame()
                if len(test_r) > 0:
                    row = test_r.iloc[0]
                    m1, m2 = st.columns(2)
                    m1.metric("MAE (Error Rata-rata)", fmt_idr(row.get("val_mae", row.get("mae", 0))),
                              help="Rata-rata selisih absolut antara prediksi dan aktual")
                    m2.metric("MAPE (%)", f"{row.get('val_mape', row.get('mape', 0)):.2f}%",
                              help="Persentase rata-rata error relatif terhadap nilai aktual")
                    m3, m4 = st.columns(2)
                    m3.metric("RMSE", fmt_idr(row.get("val_rmse", row.get("rmse", 0))))
                    m4.metric("R²", f"{row.get('val_r2', row.get('r2', 0)):.4f}",
                              help="Semakin mendekati 1.0, semakin baik model menjelaskan variasi data")
                with st.expander("Lihat semua model regresi"):
                    st.dataframe(df_reg_m.head(10), use_container_width=True, hide_index=True)
            else:
                no_data_card("Jalankan Notebook 09 untuk melihat metrics regresi.")

        with col_perf_c:
            st.markdown("""
            <div class="panel">
                <h3>Prediksi Arah (Klasifikasi)</h3>
                <p>Seberapa akurat model menebak apakah pendapatan akan naik, stabil, atau turun</p>
            </div>
            """, unsafe_allow_html=True)
            if df_cls_m is not None:
                test_c = df_cls_m[df_cls_m.get("model_name", pd.Series()).str.contains("TEST", na=False)] if "model_name" in df_cls_m.columns else pd.DataFrame()
                if len(test_c) > 0:
                    row_c = test_c.iloc[0]
                    m1, m2 = st.columns(2)
                    m1.metric("Accuracy", f"{row_c.get('val_accuracy', row_c.get('accuracy', 0)):.4f}",
                              help="Persentase prediksi arah yang benar")
                    m2.metric("F1 Macro", f"{row_c.get('val_macro_f1', row_c.get('macro_f1', 0)):.4f}",
                              help="Keseimbangan antara presisi dan recall, dirata-rata antar kelas")
                    m3, m4 = st.columns(2)
                    m3.metric("Precision", f"{row_c.get('val_macro_precision', row_c.get('macro_precision', 0)):.4f}")
                    m4.metric("Recall",    f"{row_c.get('val_macro_recall', row_c.get('macro_recall', 0)):.4f}")
                with st.expander("Lihat semua model klasifikasi"):
                    st.dataframe(df_cls_m.head(10), use_container_width=True, hide_index=True)
            else:
                no_data_card("Jalankan Notebook 09 untuk melihat metrics klasifikasi.")

        # ── Model eval charts
        charts_dir = fpath("outputs", "charts")
        eval_charts = [
            ("regression_prediction_vs_actual.png", "Actual vs Predicted"),
            ("classification_confusion_matrix.png",  "Confusion Matrix — Prediksi Arah"),
        ]
        found_c = [(n, l) for n, l in eval_charts if os.path.exists(os.path.join(charts_dir, n))]
        if found_c:
            cols = st.columns(len(found_c), gap="large")
            for col, (n, l) in zip(cols, found_c):
                with col:
                    st.image(os.path.join(charts_dir, n), caption=l, use_container_width=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── PREDICTION FORM
        st.markdown("""
        <div class="section-header">Coba Prediksi Pendapatan Kamu</div>
        <div class="panel" style="margin-bottom:1.5rem;">
            <p>Isi pendapatan kamu selama 4 minggu terakhir. Semakin akurat data yang dimasukkan, 
            semakin akurat prediksinya. Tidak perlu angka pasti &mdash; perkiraan sudah cukup.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("pred_form", clear_on_submit=False):

            st.markdown("**Pendapatan 4 minggu terakhir (dalam Rupiah)**")
            st.caption("W4 = paling lama  →  W1 = minggu lalu")

            cw4, cw3, cw2, cw1 = st.columns(4)
            with cw4: w4 = st.number_input("W4 — 4 minggu lalu",  min_value=0, max_value=50_000_000, value=800_000,  step=50_000)
            with cw3: w3 = st.number_input("W3 — 3 minggu lalu",  min_value=0, max_value=50_000_000, value=750_000,  step=50_000)
            with cw2: w2 = st.number_input("W2 — 2 minggu lalu",  min_value=0, max_value=50_000_000, value=900_000,  step=50_000)
            with cw1: w1 = st.number_input("W1 — Minggu lalu",    min_value=0, max_value=50_000_000, value=850_000,  step=50_000)

            st.markdown("<div style='margin-top:1rem'><strong>Konteks Pekerjaan</strong></div>", unsafe_allow_html=True)
            ctx1, ctx2, ctx3 = st.columns(3)
            with ctx1:
                gig_input = st.selectbox("Jenis Pekerjaan", ORDERED_GIG_TYPES,
                                          format_func=lambda x: GIG_LABELS.get(x, x))
            with ctx2:
                month_names = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"]
                target_month = st.selectbox("Bulan yang diprediksi", list(range(1, 13)),
                                             index=4, format_func=lambda m: month_names[m-1])
            with ctx3:
                target_week = st.selectbox("Minggu ke- dalam bulan", [1,2,3,4], index=0,
                                            format_func=lambda w: f"Minggu {w}")

            submitted = st.form_submit_button("Hitung Prediksi", type="primary", use_container_width=True)

        # ── Compute & Display Result
        if submitted:
            lags = np.array([w4, w3, w2, w1], dtype=float)
            rm   = np.mean(lags)
            rs   = np.std(lags)

            # Feature engineering (mirrors Notebook 05)
            rmin  = np.min(lags);  rmax = np.max(lags)
            rrange = rmax - rmin;  rmed = np.median(lags)
            rcv   = rs / rm if rm > 0 else 0
            rm2   = np.mean([w2, w1])
            trend_4w_pct  = (w1 - w4) / w4 if w4 > 0 else 0
            last_chg_pct  = (w1 - w2) / w2 if w2 > 0 else 0
            is_up     = 1 if w1 > w2 * 1.05 else 0
            is_down   = 1 if w1 < w2 * 0.95 else 0
            is_stable = 1 if not is_up and not is_down else 0
            try:
                slope = float(np.polyfit([0,1,2,3], lags, 1)[0])
            except Exception:
                slope = 0.0

            quarter = (target_month - 1) // 3 + 1
            gig_enc = {g: i for i, g in enumerate(ORDERED_GIG_TYPES)}.get(gig_input, 0)

            feature_dict = {
                "lag_1_income": w1, "lag_2_income": w2, "lag_3_income": w3, "lag_4_income": w4,
                "rolling_mean_4w": rm, "rolling_std_4w": rs, "rolling_min_4w": rmin,
                "rolling_max_4w": rmax, "rolling_range_4w": rrange, "rolling_median_4w": rmed,
                "rolling_cv_4w": rcv, "rolling_last_vs_median_pct": (w1 - rmed)/rmed if rmed > 0 else 0,
                "rolling_mean_2w": rm2, "rolling_mean_8w": rm, "rolling_std_8w": rs,
                "income_trend_4w_abs": w1 - w4, "income_trend_4w_pct": trend_4w_pct,
                "last_income_change_abs": w1 - w2, "last_income_change_pct": last_chg_pct,
                "income_growth_1w": last_chg_pct, "income_volatility": rcv,
                "trend_slope_4w": slope, "is_previous_week_up": is_up,
                "is_previous_week_down": is_down, "is_previous_week_stable": is_stable,
                "lag_ratio_1_to_mean": w1/rm if rm > 0 else 1.0,
                "target_month": target_month, "target_week_of_month": target_week,
                "target_quarter": quarter,
                "target_is_month_end_week": 1 if target_week == 4 else 0,
                "target_is_month_start_week": 1 if target_week == 1 else 0,
                "is_ramadan_lebaran_period": 1 if target_month in [3,4] else 0,
                "is_harbolnas_period": 1 if target_month in [10,11,12] else 0,
                "is_payday_period": 1 if target_week in [1,4] else 0,
                "gig_type_encoded": gig_enc,
            }

            pred_idr      = None
            direction_pred = None
            LINEAR_MODELS  = {"LinearRegression","Ridge"}

            if FEATURE_COLS and reg_model is not None:
                try:
                    X = pd.DataFrame([feature_dict])
                    for c in FEATURE_COLS:
                        if c not in X.columns: X[c] = 0.0
                    X = X[FEATURE_COLS].fillna(0)
                    mn  = type(reg_model).__name__
                    Xp  = scalers["feature_scaler"].transform(X) if (scalers and "feature_scaler" in scalers and mn in LINEAR_MODELS) else X.values
                    pred_log  = reg_model.predict(Xp)[0]
                    pred_idr  = float(np.clip(np.expm1(pred_log), 0, None))

                    if cls_model is not None:
                        cn  = type(cls_model).__name__
                        Xc  = scalers["feature_scaler"].transform(X) if (scalers and "feature_scaler" in scalers and cn in LINEAR_MODELS) else X.values
                        dir_code       = cls_model.predict(Xc)[0]
                        direction_pred = {0:"Down", 1:"Stable", 2:"Up"}.get(int(dir_code), "Stable")
                except Exception as e:
                    st.error(f"Error saat prediksi: {e}")

            # Fallback
            if pred_idr is None:
                pred_idr       = float(rm)
                direction_pred = "Stable"
                st.info("Estimasi menggunakan rata-rata rolling 4 minggu (model belum dimuat).")

            # ── Result display
            delta_vs_avg = pred_idr - rm
            dir_label    = {"Up":"Naik","Stable":"Stabil","Down":"Turun"}.get(direction_pred,"Stabil")
            vol_label    = "Tinggi" if rcv > 0.3 else ("Sedang" if rcv > 0.15 else "Rendah")
            badge_dir_cls = "badge-green" if direction_pred=="Up" else ("badge-red" if direction_pred=="Down" else "badge-yellow")
            badge_vol_cls = "badge-red" if rcv > 0.3 else ("badge-yellow" if rcv > 0.15 else "badge-green")

            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">Estimasi Pendapatan Minggu Depan</div>
                <div class="result-value">{fmt_idr(pred_idr)}</div>
                <div class="result-sub">
                    {'+' if delta_vs_avg >= 0 else ''}{fmt_idr(delta_vs_avg)} vs rata-rata 4 minggu
                    &nbsp;&nbsp;
                    <span class="badge {badge_dir_cls}">Arah: {dir_label}</span>
                    &nbsp;
                    <span class="badge {badge_vol_cls}">Volatilitas: {vol_label}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Trend chart
            fig, ax = plt.subplots(figsize=(10, 4))
            w_labels = ["W4 (terlama)","W3","W2","W1 (terbaru)"]
            h_vals   = [v/1000 for v in [w4,w3,w2,w1]]
            ax.plot(w_labels, h_vals, "o-", color=FINGO_BLUE, linewidth=2.5, markersize=8, label="Historis")
            ax.plot(["W1 (terbaru)","Prediksi"], [w1/1000, pred_idr/1000],
                    "o--", color=FINGO_GREEN, linewidth=2.5, markersize=9,
                    label=f"Prediksi: {fmt_idr(pred_idr)}", zorder=5)
            ax.axhline(rm/1000, color=FINGO_WARN, linestyle=":", alpha=0.7,
                       label=f"Rata-rata 4w: {fmt_idr(rm)}")
            ax.fill_between(
                ["W1 (terbaru)","Prediksi"],
                [(w1-rs*0.5)/1000, (pred_idr-rs*0.5)/1000],
                [(w1+rs*0.5)/1000, (pred_idr+rs*0.5)/1000],
                alpha=0.12, color=FINGO_GREEN
            )
            ax.set_title(f"Tren Pendapatan — {GIG_LABELS.get(gig_input, gig_input)}", color="#E8EDE9")
            ax.set_ylabel("Pendapatan (ribu Rp)")
            ax.legend(fontsize=8)
            plt.tight_layout(pad=0.8)
            st.pyplot(fig, use_container_width=True)
            plt.close()

            # ── Budget recommendation
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">Saran Pembagian Anggaran (Metode 50/30/20)</div>', unsafe_allow_html=True)

            kebutuhan = pred_idr * 0.50
            tabungan  = pred_idr * 0.30
            keinginan = pred_idr * 0.20

            st.markdown("""
            <div class="panel">
                <p>Berdasarkan prediksi pendapatan minggu depan, berikut saran pembagian anggaran menggunakan 
                metode <strong style="color:#E8EDE9">50/30/20</strong>: 50% untuk kebutuhan pokok, 
                30% untuk tabungan/investasi, dan 20% untuk pengeluaran tambahan.</p>
            </div>
            """, unsafe_allow_html=True)

            bc1, bc2, bc3 = st.columns(3)
            bc1.metric("Kebutuhan Pokok (50%)", fmt_idr(kebutuhan),
                       help="Makan, transport, tagihan, sewa")
            bc2.metric("Tabungan / Investasi (30%)", fmt_idr(tabungan),
                       help="Dana darurat, deposito, investasi")
            bc3.metric("Pengeluaran Lain (20%)", fmt_idr(keinginan),
                       help="Hiburan, belanja, hobi")

            # Visual bars
            for label, amount, pct, color in [
                ("Kebutuhan Pokok", kebutuhan, 50, FINGO_GREEN),
                ("Tabungan / Investasi", tabungan, 30, FINGO_BLUE),
                ("Pengeluaran Lain", keinginan, 20, FINGO_WARN),
            ]:
                st.markdown(f"""
                <div class="budget-bar-wrap">
                    <div class="budget-bar-label">
                        <span>{label}</span>
                        <span>{fmt_idr(amount)} <span style="color:var(--fingo-muted)">({pct}%)</span></span>
                    </div>
                    <div class="budget-bar-track">
                        <div class="budget-bar-fill" style="width:{pct}%;background:{color}"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ── Personalized advice
            st.markdown("<div style='margin-top:1rem'>", unsafe_allow_html=True)
            if direction_pred == "Down":
                st.warning("Pendapatan diprediksi **turun** minggu depan. Pertimbangkan untuk sementara mengurangi pengeluaran tambahan dan memprioritaskan kebutuhan pokok serta tabungan darurat.")
            elif direction_pred == "Up":
                st.success("Pendapatan diprediksi **naik** minggu depan. Ini saat yang baik untuk menambah alokasi tabungan atau investasi.")
            else:
                st.info("Pendapatan diprediksi **stabil** minggu depan. Pertahankan pola pengeluaran saat ini dan pastikan alokasi tabungan tetap konsisten.")

            if vol_label == "Tinggi":
                st.warning(f"Volatilitas pendapatan kamu **tinggi** (CV={rcv:.2f}). Pendapatan berfluktuasi besar antar minggu — disarankan memiliki dana darurat minimal 2 bulan pengeluaran.")
            st.markdown("</div>", unsafe_allow_html=True)

        # ── Test set scatter
        df_pred_test = load_predictions_test()
        if df_pred_test is not None:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">Akurasi Model pada Data Uji (Test Set)</div>', unsafe_allow_html=True)
            if "next_week_income" in df_pred_test.columns and "predicted_next_week_income" in df_pred_test.columns:
                samp = df_pred_test.sample(min(500, len(df_pred_test)), random_state=42)
                fig, ax = plt.subplots(figsize=(7, 5))
                ax.scatter(samp["next_week_income"]/1e6, samp["predicted_next_week_income"]/1e6,
                           alpha=0.35, s=12, color=FINGO_GREEN)
                lims = [min(samp["next_week_income"].min(), samp["predicted_next_week_income"].min())/1e6,
                        max(samp["next_week_income"].max(), samp["predicted_next_week_income"].max())/1e6]
                ax.plot(lims, lims, "--", color=FINGO_WARN, linewidth=1.5, label="Ideal (aktual = prediksi)")
                ax.set_xlabel("Pendapatan Aktual (juta Rp)")
                ax.set_ylabel("Pendapatan Prediksi (juta Rp)")
                ax.set_title("Actual vs Predicted — Test Set (sample 500)", color="#E8EDE9")
                ax.legend(fontsize=8)
                plt.tight_layout(pad=0.8)
                st.pyplot(fig, use_container_width=True)
                plt.close()
                st.caption("Titik-titik yang mendekati garis putus-putus berarti prediksi sangat akurat.")

            with st.expander("Lihat data prediksi test set (20 baris pertama)"):
                st.dataframe(df_pred_test.head(20), use_container_width=True, hide_index=True)

    # ─────────────────────────────────────────────
    # TAB: A/B TESTING
    # ─────────────────────────────────────────────
    with sub_tabs[3]:
        st.markdown("""
        <div class="page-header">
            <h1>Hasil A/B Testing</h1>
            <p>Apakah Income Predictor terbukti lebih baik dari perencanaan anggaran manual?</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="panel">
            <h3>Metodologi Eksperimen</h3>
            <p>
                <strong style="color:#E8EDE9">Kelompok Control</strong> merencanakan anggaran menggunakan rata-rata 
                pendapatan 4 minggu terakhir (cara manual yang umum dilakukan).<br><br>
                <strong style="color:#E8EDE9">Kelompok Treatment</strong> menggunakan prediksi dari Income Predictor AI 
                sebagai dasar perencanaan anggaran.<br><br>
                Metrik utama: <em>Budget Error</em> (selisih antara anggaran yang direncanakan dengan pengeluaran aktual). 
                Semakin kecil, semakin akurat perencanaan.<br><br>
                <span style="color:var(--fingo-warn);font-size:0.82rem">
                Catatan: Seluruh hasil menggunakan data sintetis (proof-of-concept). Validasi dengan pengguna nyata diperlukan untuk produksi.
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        df_sy_ab = load_synthetic()
        if df_sy_ab is None:
            no_data_card("File <code>data/synthetic/synthetic_52week_user_income.csv</code> belum tersedia.")
        else:
            BUDGET_RATIO    = 0.70
            NOISE_CONTROL   = 0.08
            NOISE_TREATMENT = 0.05
            ALPHA           = 0.05
            COLORS_AB       = {"control": FINGO_BLUE, "treatment": FINGO_GREEN}

            np.random.seed(42)
            df_ab = df_sy_ab.copy()

            col_user  = next((c for c in df_ab.columns if "user_id" in c.lower()), None)
            col_week  = next((c for c in df_ab.columns if "week" in c.lower() and "index" in c.lower()), None)
            col_inc   = next((c for c in df_ab.columns if c.lower() in ["synthetic_weekly_income","weekly_income","income"]), None)
            col_gig   = next((c for c in df_ab.columns if "gig_type" in c.lower()), None)

            if not all([col_user, col_week, col_inc]):
                st.error("Kolom yang diperlukan tidak ditemukan dalam dataset sintetis.")
            else:
                df_ab = df_ab.rename(columns={col_user:"user_id", col_week:"week_index", col_inc:"actual_income"})
                if col_gig: df_ab = df_ab.rename(columns={col_gig:"gig_type"})

                # Assignment
                uu = df_ab.drop_duplicates("user_id")[["user_id"] + (["gig_type"] if "gig_type" in df_ab.columns else [])].reset_index(drop=True)
                assigned = []
                if "gig_type" in uu.columns:
                    for gt, grp in uu.groupby("gig_type"):
                        ids = grp["user_id"].values.copy(); np.random.shuffle(ids)
                        half = len(ids) // 2
                        for i, uid in enumerate(ids):
                            assigned.append({"user_id": uid, "group": "control" if i < half else "treatment"})
                else:
                    ids = uu["user_id"].values.copy(); np.random.shuffle(ids)
                    half = len(ids) // 2
                    for i, uid in enumerate(ids):
                        assigned.append({"user_id": uid, "group": "control" if i < half else "treatment"})

                df_sim = df_ab.merge(pd.DataFrame(assigned), on="user_id", how="left")
                df_sim = df_sim.sort_values(["user_id","week_index"])
                df_sim["rolling_mean_4w"] = (
                    df_sim.groupby("user_id")["actual_income"]
                    .transform(lambda x: x.shift(1).rolling(4, min_periods=1).mean())
                ).fillna(df_sim["actual_income"])

                noise_t = np.random.normal(0, NOISE_TREATMENT, len(df_sim))
                df_sim["predicted_income"] = np.where(
                    df_sim["group"] == "treatment",
                    df_sim["actual_income"] * (1 + noise_t),
                    df_sim["rolling_mean_4w"],
                )
                df_sim["planned_budget"]  = df_sim["predicted_income"] * BUDGET_RATIO
                noise_exp = np.random.normal(0, 0.06, len(df_sim))
                df_sim["actual_expense"]  = (df_sim["actual_income"] * (BUDGET_RATIO + noise_exp)).clip(lower=0)
                df_sim["budget_error"]    = np.abs(df_sim["planned_budget"] - df_sim["actual_expense"])
                df_sim["is_over_budget"]  = (df_sim["actual_expense"] > df_sim["planned_budget"]).astype(int)
                df_sim["saving_rate"]     = ((df_sim["actual_income"] - df_sim["actual_expense"]) / df_sim["actual_income"].clip(lower=1)).clip(0,1)

                agg_cols = {"user_id","group"} | ({"gig_type"} if "gig_type" in df_sim.columns else set())
                df_ua = df_sim.groupby(list(agg_cols)).agg(
                    total_weeks=("actual_income","count"),
                    n_over=("is_over_budget","sum"),
                    mean_error=("budget_error","mean"),
                    mean_saving=("saving_rate","mean"),
                ).reset_index()
                df_ua["adherence_rate"] = (df_ua["total_weeks"] - df_ua["n_over"]) / df_ua["total_weeks"]
                df_ua["over_rate"]      = df_ua["n_over"] / df_ua["total_weeks"]

                ctrl  = df_ua[df_ua["group"]=="control"]
                treat = df_ua[df_ua["group"]=="treatment"]
                n_c, n_t = len(ctrl), len(treat)
                be_c, be_t = ctrl["mean_error"].values, treat["mean_error"].values
                mean_c, mean_t = be_c.mean(), be_t.mean()
                rel_red = (mean_t - mean_c) / mean_c * 100 if mean_c > 0 else 0
                u_stat, u_p = mannwhitneyu(be_t, be_c, alternative="less")
                pooled = np.sqrt((be_c.std()**2 + be_t.std()**2) / 2)
                cohens_d = (mean_t - mean_c) / pooled if pooled > 0 else 0.0
                abs_d = abs(cohens_d)
                effect_label = "Sangat Besar" if abs_d >= 0.8 else ("Besar" if abs_d >= 0.5 else ("Sedang" if abs_d >= 0.2 else "Kecil"))
                significant = u_p < ALPHA and mean_t < mean_c

                # KPI
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown('<div class="section-header">Ringkasan Hasil</div>', unsafe_allow_html=True)
                k1, k2, k3, k4, k5 = st.columns(5)
                k1.metric("Peserta Control",    f"{n_c:,}")
                k2.metric("Peserta Treatment",  f"{n_t:,}")
                k3.metric("Budget Error Control",   fmt_idr(mean_c))
                k4.metric("Budget Error Treatment", fmt_idr(mean_t), delta=f"{rel_red:.1f}%")
                k5.metric("Cohen's d", f"{cohens_d:.3f}", delta=effect_label)

                if significant:
                    st.success(f"H0 ditolak (p = {u_p:.6f} < {ALPHA}). Treatment menghasilkan budget error lebih rendah sebesar {abs(rel_red):.1f}%. Ukuran efek: {effect_label} (d={cohens_d:.3f}).")
                else:
                    st.warning(f"H0 tidak ditolak (p = {u_p:.6f}). Perbedaan belum signifikan secara statistik pada level {ALPHA}.")

                # Charts
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown('<div class="section-header">Distribusi Budget Error</div>', unsafe_allow_html=True)

                fig, axes = plt.subplots(1, 3, figsize=(16, 5))
                axes[0].hist(be_c/1e3, bins=30, alpha=0.6, color=COLORS_AB["control"],  label=f"Control (n={n_c:,})",  density=True)
                axes[0].hist(be_t/1e3, bins=30, alpha=0.6, color=COLORS_AB["treatment"],label=f"Treatment (n={n_t:,})", density=True)
                axes[0].axvline(mean_c/1e3, color=COLORS_AB["control"],  linestyle="--", alpha=0.9)
                axes[0].axvline(mean_t/1e3, color=COLORS_AB["treatment"], linestyle="--", alpha=0.9)
                axes[0].set_title("Budget Error (Metrik Utama)", color="#E8EDE9")
                axes[0].set_xlabel("Rata-rata Budget Error (ribu Rp)")
                axes[0].legend(fontsize=8)

                bar_c = ctrl["adherence_rate"].values; bar_t = treat["adherence_rate"].values
                axes[1].hist(bar_c, bins=20, alpha=0.6, color=COLORS_AB["control"],  label="Control",   density=True)
                axes[1].hist(bar_t, bins=20, alpha=0.6, color=COLORS_AB["treatment"],label="Treatment",  density=True)
                axes[1].set_title("Budget Adherence Rate", color="#E8EDE9")
                axes[1].set_xlabel("Tingkat Kepatuhan Anggaran")
                axes[1].legend(fontsize=8)

                sc = ctrl["mean_saving"].values; st_sav = treat["mean_saving"].values
                axes[2].hist(sc,    bins=20, alpha=0.6, color=COLORS_AB["control"],  label="Control",  density=True)
                axes[2].hist(st_sav,bins=20, alpha=0.6, color=COLORS_AB["treatment"],label="Treatment", density=True)
                axes[2].set_title("Saving Allocation Rate", color="#E8EDE9")
                axes[2].set_xlabel("Tingkat Tabungan")
                axes[2].legend(fontsize=8)

                plt.tight_layout(pad=1)
                st.pyplot(fig, use_container_width=True)
                plt.close()

                # Bar mean + CI
                st.markdown('<div class="section-header">Perbandingan Rata-rata dan Confidence Interval 95%</div>', unsafe_allow_html=True)
                fig2, axes2 = plt.subplots(1, 2, figsize=(14, 5))

                grp_lbls = ["Control\n(Manual)", "Treatment\n(AI Predictor)"]
                means_be = [mean_c/1e3, mean_t/1e3]
                errs_be  = [1.96*be_c.std()/np.sqrt(n_c)/1e3, 1.96*be_t.std()/np.sqrt(n_t)/1e3]
                bars2 = axes2[0].bar(grp_lbls, means_be, color=[COLORS_AB["control"],COLORS_AB["treatment"]],
                                      yerr=errs_be, capsize=8, alpha=0.9)
                for bar, v, e in zip(bars2, means_be, errs_be):
                    axes2[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+e+2,
                                   f"Rp {v:.0f}rb", ha="center", fontsize=9, fontweight="bold", color="#E8EDE9")
                axes2[0].set_title("Rata-rata Budget Error ± 95% CI", color="#E8EDE9")
                axes2[0].set_ylabel("Budget Error (ribu Rp)")

                sec = {"Budget\nAdherence": [bar_c.mean(), bar_t.mean()],
                       "Saving\nRate":      [sc.mean(), st_sav.mean()],
                       "Over-Budget\nRate": [ctrl["over_rate"].mean(), treat["over_rate"].mean()]}
                xp = np.arange(len(sec)); wd = 0.3
                axes2[1].bar(xp-wd/2, [v[0] for v in sec.values()], wd, label="Control",   color=COLORS_AB["control"],   alpha=0.85)
                axes2[1].bar(xp+wd/2, [v[1] for v in sec.values()], wd, label="Treatment", color=COLORS_AB["treatment"], alpha=0.85)
                axes2[1].set_xticks(xp); axes2[1].set_xticklabels(list(sec.keys()), fontsize=9)
                axes2[1].set_title("Metrik Sekunder: Control vs Treatment", color="#E8EDE9")
                axes2[1].legend(fontsize=8)

                plt.tight_layout(pad=1)
                st.pyplot(fig2, use_container_width=True)
                plt.close()

                # Stat table
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown('<div class="section-header">Tabel Hasil Uji Statistik</div>', unsafe_allow_html=True)
                stat_rows = [{
                    "Metrik": "Budget Error (Utama)",
                    "Control": fmt_idr(mean_c), "Treatment": fmt_idr(mean_t),
                    "Perubahan (%)": f"{rel_red:.2f}%",
                    "U-Stat": f"{u_stat:.1f}", "p-value": f"{u_p:.6f}",
                    "Cohen's d": f"{cohens_d:.4f}", "Effect Size": effect_label,
                    "Signifikan": "Ya" if significant else "Tidak",
                }]
                for col, label, alt in [
                    ("adherence_rate","Budget Adherence Rate","greater"),
                    ("over_rate","Over-Budget Rate","less"),
                    ("mean_saving","Saving Rate","greater"),
                ]:
                    if col not in df_ua.columns: continue
                    cv = ctrl[col].dropna().values; tv = treat[col].dropna().values
                    try:
                        u2, p2 = mannwhitneyu(tv, cv, alternative=alt)
                        d2 = (tv.mean()-cv.mean()) / np.sqrt((cv.std()**2+tv.std()**2)/2) if np.sqrt((cv.std()**2+tv.std()**2)/2) > 0 else 0
                        stat_rows.append({
                            "Metrik": label,
                            "Control": f"{cv.mean():.4f}", "Treatment": f"{tv.mean():.4f}",
                            "Perubahan (%)": f"{(tv.mean()-cv.mean())/cv.mean()*100:.2f}%",
                            "U-Stat": f"{u2:.1f}", "p-value": f"{p2:.6f}",
                            "Cohen's d": f"{d2:.4f}",
                            "Effect Size": "Besar" if abs(d2)>=0.8 else ("Sedang" if abs(d2)>=0.5 else ("Kecil" if abs(d2)>=0.2 else "Trivial")),
                            "Signifikan": "Ya" if p2 < ALPHA else "Tidak",
                        })
                    except Exception: pass
                st.dataframe(pd.DataFrame(stat_rows), use_container_width=True, hide_index=True)

                # Subgroup
                if "gig_type" in df_ua.columns:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown('<div class="section-header">Analisis per Jenis Pekerjaan (Eksploratorif)</div>', unsafe_allow_html=True)
                    st.caption("Analisis subgroup bersifat eksploratorif. Tidak menggantikan hasil uji utama.")
                    sub_rows = []
                    for gt in sorted(df_ua["gig_type"].unique()):
                        sub = df_ua[df_ua["gig_type"]==gt]
                        cs = sub[sub["group"]=="control"]["mean_error"].values
                        ts = sub[sub["group"]=="treatment"]["mean_error"].values
                        if len(cs)<5 or len(ts)<5: continue
                        try:
                            us, ps = mannwhitneyu(ts, cs, alternative="less")
                            ds = (ts.mean()-cs.mean())/np.sqrt((cs.std()**2+ts.std()**2)/2) if np.sqrt((cs.std()**2+ts.std()**2)/2)>0 else 0
                            sub_rows.append({
                                "Jenis Pekerjaan": GIG_LABELS.get(gt, gt),
                                "n Control": len(cs), "n Treatment": len(ts),
                                "Error Control": fmt_idr(cs.mean()),
                                "Error Treatment": fmt_idr(ts.mean()),
                                "Reduksi (%)": f"{(ts.mean()-cs.mean())/cs.mean()*100:.2f}%",
                                "p-value": f"{ps:.4f}",
                                "Signifikan": "Ya" if ps<ALPHA else "Tidak",
                            })
                        except Exception: pass
                    if sub_rows:
                        st.dataframe(pd.DataFrame(sub_rows), use_container_width=True, hide_index=True)

                # Notebook charts if exist
                ab_charts = ["ab_income_predictor_distribution.png","ab_income_predictor_summary.png",
                              "ab_income_predictor_subgroup.png"]
                found_ab = [c for c in ab_charts if os.path.exists(fpath("outputs","charts",c))]
                if found_ab:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown('<div class="section-header">Chart dari Notebook 10</div>', unsafe_allow_html=True)
                    for i in range(0, len(found_ab), 2):
                        cols = st.columns(2, gap="large")
                        for j, cn in enumerate(found_ab[i:i+2]):
                            with cols[j]:
                                st.image(fpath("outputs","charts",cn),
                                         caption=cn.replace("_"," ").replace(".png",""),
                                         use_container_width=True)

                # Report
                rp = fpath("outputs","reports","ab_testing_income_predictor_budgeting_report.md")
                if os.path.exists(rp):
                    with st.expander("Baca laporan lengkap A/B Testing"):
                        with open(rp, encoding="utf-8") as f:
                            st.markdown(f.read())

    # ─────────────────────────────────────────────
    # TAB: REFERENSI DATA
    # ─────────────────────────────────────────────
    with sub_tabs[4]:
        st.markdown("""
        <div class="page-header">
            <h1>Referensi Data</h1>
            <p>Kamus data, daftar fitur model, dan kontrak model</p>
        </div>
        """, unsafe_allow_html=True)

        ref_tabs = st.tabs(["Kamus Data", "Fitur Model", "Model Contract"])

        with ref_tabs[0]:
            df_dict = load_data_dictionary()
            if df_dict is not None:
                st.caption(f"{len(df_dict)} entri dalam kamus data")
                search = st.text_input("Cari kolom atau deskripsi...", placeholder="Ketik nama kolom atau kata kunci")
                df_show = df_dict
                if search:
                    mask = df_dict.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)
                    df_show = df_dict[mask]
                st.dataframe(df_show, use_container_width=True, hide_index=True)
            else:
                st.info("Jalankan Notebook 08 untuk menghasilkan kamus data.")
                st.markdown("""
                | Kolom | Tipe | Deskripsi |
                |---|---|---|
                | `respondent_id` | string | ID unik responden |
                | `gig_type` | string | Jenis pekerjaan gig |
                | `income_w1` | float | Pendapatan minggu lalu (terbaru) |
                | `income_w4` | float | Pendapatan 4 minggu lalu (terlama) |
                | `synthetic_user_id` | string | ID user sintetis |
                | `next_week_income` | float | Target regresi |
                | `next_week_direction` | string | Target klasifikasi (Up/Stable/Down) |
                """)

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">Penjelasan Temporal W1–W4</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="panel">
                <p>
                <strong style="color:#E8EDE9">W1</strong> = Pendapatan H-7 hingga H-1 dari tanggal pengisian (paling baru)<br>
                <strong style="color:#E8EDE9">W2</strong> = Pendapatan H-14 hingga H-8<br>
                <strong style="color:#E8EDE9">W3</strong> = Pendapatan H-21 hingga H-15<br>
                <strong style="color:#E8EDE9">W4</strong> = Pendapatan H-28 hingga H-22 (paling lama)<br><br>
                Dalam model: <code>lag_4 = income_w4</code> (input pertama/terlama) → <code>lag_1 = income_w1</code> (input terakhir/terbaru)
                </p>
            </div>
            """, unsafe_allow_html=True)

        with ref_tabs[1]:
            feat_meta = load_feature_columns()
            if feat_meta and "feature_columns" in feat_meta:
                FEAT_COLS = feat_meta["feature_columns"]
                st.caption(f"{len(FEAT_COLS)} fitur digunakan oleh model")

                groups = {
                    "Lag Features (Riwayat Pendapatan)":     [c for c in FEAT_COLS if c.startswith("lag_")],
                    "Rolling Features (Statistik Rolling)":  [c for c in FEAT_COLS if c.startswith("rolling_")],
                    "Trend Features (Tren & Perubahan)":     [c for c in FEAT_COLS if any(k in c for k in ["trend","growth","change","slope"])],
                    "Direction Features (Arah & Volatilitas)":[c for c in FEAT_COLS if any(k in c for k in ["is_previous","volatility","ratio"])],
                    "Calendar Features (Musiman)":            [c for c in FEAT_COLS if any(k in c for k in ["target_","is_ramadan","is_harbolnas","is_payday"])],
                    "Categorical (Jenis Pekerjaan)":          [c for c in FEAT_COLS if any(k in c for k in ["gig_type","domisili"])],
                }
                other = [c for c in FEAT_COLS if not any(c in v for v in groups.values())]
                if other: groups["Lainnya"] = other

                for gname, cols in groups.items():
                    if not cols: continue
                    with st.expander(f"{gname}  ({len(cols)} fitur)", expanded=True):
                        st.write(", ".join([f"`{c}`" for c in cols]))

                with st.expander("Semua fitur (JSON)"):
                    st.json(feat_meta)
            else:
                no_data_card("Jalankan Notebook 05–06 untuk menghasilkan feature_columns.json.")

        with ref_tabs[2]:
            mc_full = load_model_contract()
            if mc_full:
                for k, v in mc_full.items():
                    if k == "feature_columns":
                        st.markdown(f"""<div class="kv-row"><span class="kv-key">{k}</span><span class="kv-val">{len(v)} kolom</span></div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""<div class="kv-row"><span class="kv-key">{k}</span><span class="kv-val">{v}</span></div>""", unsafe_allow_html=True)
            else:
                no_data_card("Jalankan Notebook 06 untuk menghasilkan model_contract.json.")

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">Pipeline Output Files</div>', unsafe_allow_html=True)
            pipeline_files = [
                ("01–02", "survey_clean.csv · survey_temporal_mapped.csv"),
                ("03",    "outputs/charts/*.png · outputs/reports/survey_eda_summary.md"),
                ("04",    "data/synthetic/synthetic_52week_user_income.csv"),
                ("05",    "data/processed/income_features.csv · outputs/model_contract/feature_columns.json"),
                ("06",    "outputs/model_contract/income_{train,val,test}.csv · income_scalers.pkl · model_contract.json"),
                ("07",    "outputs/reports/bias_validation_report.md"),
                ("08",    "outputs/dashboard/data_dictionary.csv · README.md"),
                ("09",    "best_income_regressor.pkl · best_direction_classifier.pkl · regression_metrics.csv · predictions_test.csv"),
                ("10",    "ab_testing_income_predictor_budgeting_report.md · ab_income_predictor_*.png"),
            ]
            for nb, files in pipeline_files:
                st.markdown(f"""
                <div class="pipeline-step">
                    <div class="pipeline-num" style="font-size:0.65rem">{nb}</div>
                    <div class="pipeline-info"><div class="pi-out" style="font-size:0.78rem">{files}</div></div>
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE: IMPULSIVE DETECTOR
# ══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown("""
    <div class="page-header">
        <h1>Impulsive Detector</h1>
        <p>Deteksi pengeluaran impulsif menggunakan machine learning</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Coming Soon Hero
    st.markdown("""
    <div class="coming-soon-wrap">
        <div class="coming-soon-badge">Coming Soon</div>
        <div class="coming-soon-title">Modul sedang dalam pengembangan</div>
        <div class="coming-soon-desc">
            Impulsive Detector akan membantu pengguna mengidentifikasi pola pengeluaran impulsif 
            secara otomatis — berdasarkan waktu, jumlah, dan kategori transaksi &mdash; 
            menggunakan model deep learning dengan perhatian temporal.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        st.markdown('<div class="section-header">Fitur yang Direncanakan</div>', unsafe_allow_html=True)
        features_planned = [
            ("EDA Pola Impulsif", "Heatmap jam transaksi, distribusi kategori pengeluaran, analisis hari vs waktu"),
            ("Klasifikasi AI", "Model impulsive_classifier.keras dengan lapisan perhatian temporal"),
            ("Evaluasi Model", "Confusion matrix, classification report, feature importance"),
            ("Peringatan Real-time", "Notifikasi saat terdeteksi pola pengeluaran impulsif"),
            ("A/B Testing", "Apakah peringatan AI terbukti mengurangi over-budget?"),
        ]
        for name, desc in features_planned:
            st.markdown(f"""
            <div style="padding: 12px 0; border-bottom: 1px solid var(--fingo-border);">
                <div style="font-size:0.87rem;font-weight:600;color:var(--fingo-text);margin-bottom:3px;">{name}</div>
                <div style="font-size:0.8rem;color:var(--fingo-muted);">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="section-header">Status Tim</div>', unsafe_allow_html=True)

        roles = [
            ("Data Scientist 1", "Nayyara Farhana Nisa", [
                ("Dataset transactions_clean.csv", True),
                ("Data Wrangling end-to-end", True),
                ("EDA impulsive buying (BQ1–BQ3)", True),
                ("Feature Engineering temporal", True),
                ("A/B Testing report (t-test + Cohen's d)", True),
            ]),
            ("AI Engineer 1", "Muhammad Fachri", [
                ("Model impulsive_classifier.keras", False),
                ("FastAPI endpoint /predict/impulsive", False),
                ("Target akurasi >= 85%", False),
            ]),
        ]

        for role, name, tasks in roles:
            st.markdown(f"""
            <div class="panel" style="margin-bottom:0.8rem">
                <h3>{role}</h3>
                <p style="color:var(--fingo-muted);margin-bottom:0.8rem">{name}</p>
            """, unsafe_allow_html=True)
            for task, done in tasks:
                badge = f'<span class="badge badge-green">Selesai</span>' if done else f'<span class="badge badge-yellow">Proses</span>'
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;padding:6px 0;
                            border-bottom:1px solid var(--fingo-border);font-size:0.82rem;">
                    <span style="color:{'var(--fingo-text)' if done else 'var(--fingo-muted)'};">{task}</span>
                    {badge}
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Preview Fitur Input Model</div>', unsafe_allow_html=True)

    preview_df = pd.DataFrame({
        "Nama Fitur":    ["hour_sin", "hour_cos", "day_of_week", "is_weekend",
                          "amount_vs_weekly_avg", "budget_remaining_ratio", "frekuensi_harian"],
        "Tipe":          ["float","float","int","bool","float","float","int"],
        "Deskripsi":     [
            "Pola waktu 24 jam — encoding sinus",
            "Pola waktu 24 jam — encoding kosinus",
            "Hari dalam seminggu (0 = Senin, 6 = Minggu)",
            "Apakah transaksi terjadi di akhir pekan?",
            "Rasio nominal transaksi terhadap rata-rata pengeluaran mingguan",
            "Proporsi sisa anggaran dibanding batas yang ditetapkan",
            "Jumlah transaksi yang sudah terjadi hari yang sama",
        ],
        "Contoh Nilai": ["0.866","0.5","1","False","1.32","0.24","3"],
    })
    st.dataframe(preview_df, use_container_width=True, hide_index=True)

    st.caption("Modul ini akan tersedia setelah dataset transactions_clean.csv dan model keras selesai dikembangkan.")