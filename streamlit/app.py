"""
Fingo Dashboard - CC26-PSU217
Financial Intelligence Platform
Insight & Kesimpulan | Income Predictor | Impulsive Detector
"""

import os, json, pickle, warnings, datetime
from textwrap import dedent
from pathlib import Path

import requests
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# PATH SETUP
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

DATA_DIR    = ROOT_DIR / "data"
OUTPUTS_DIR = ROOT_DIR / "outputs"
MODELS_DIR  = BASE_DIR / "models"

INCOME_PROC_DIR  = DATA_DIR / "processed"
INCOME_RAW_DIR   = DATA_DIR / "raw"
INCOME_SYNTH_DIR = DATA_DIR / "synthetic"

INCOME_CONTRACT_DIR = OUTPUTS_DIR / "model_contract"
INCOME_RESULTS_DIR  = OUTPUTS_DIR / "model_results"
INCOME_REPORTS_DIR  = OUTPUTS_DIR / "reports"
INCOME_CHARTS_DIR   = OUTPUTS_DIR / "charts" / "income"

IMP_FINAL_DIR = BASE_DIR / "data" / "impulsive"
IMP_SPLIT_DIR = BASE_DIR / "data" / "impulsive" / "split"

INCOME_STREAMLIT_DIR = BASE_DIR / "data" / "income"
INCOME_TEST_PATH     = INCOME_STREAMLIT_DIR / "income_test.csv"
INCOME_VAL_PATH      = INCOME_STREAMLIT_DIR / "income_val.csv"

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fingo - Financial Intelligence Platform",
    page_icon="F",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display:ital@0;1&display=swap');
:root{
    --fg:#00C471;--fg-acc:#00E882;--fg-warn:#F5A623;
    --fg-red:#E8504A;--fg-blue:#4A9EE8;--fg-muted:#6B7E74;
    --bg:#0B0F0E;--bg-surf:#111714;--bg-card:#161D1A;
    --border:#1E2B25;--text:#E8EDE9;
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;color:var(--text);}
.stApp{background:var(--bg);}
.block-container{padding:2rem 2.5rem 3rem;max-width:1400px;}
[data-testid="stSidebar"]{background:var(--bg-surf);border-right:1px solid var(--border);}
[data-testid="stSidebar"] *{color:var(--text) !important;}
[data-testid="stSidebarContent"]{padding:1.5rem 1.2rem;}
.stRadio > label{display:none;}
.stRadio div[role="radiogroup"]{display:flex;flex-direction:column;gap:4px;}
.stRadio div[role="radiogroup"] label{
    display:flex !important;align-items:center;padding:10px 14px;
    border-radius:8px;cursor:pointer;font-size:.9rem;font-weight:500;
    border:1px solid transparent;transition:background .15s;
}
.stRadio div[role="radiogroup"] label:hover{background:var(--border);}
.stRadio label:has(input:checked){
    background:rgba(0,196,113,.12) !important;
    border-color:rgba(0,196,113,.3) !important;color:var(--fg-acc) !important;
}
.page-header{border-bottom:1px solid var(--border);padding-bottom:1.2rem;margin-bottom:2rem;}
.page-header h1{font-family:'DM Serif Display',serif;font-size:2.2rem;font-weight:400;
    color:var(--text);margin:0 0 4px;line-height:1.2;}
.page-header p{color:var(--fg-muted);font-size:.9rem;margin:0;}
.section-header{font-size:.7rem;font-weight:600;color:var(--fg-muted);
    text-transform:uppercase;letter-spacing:.12em;margin:1.8rem 0 .8rem;}
.panel{background:var(--bg-card);border:1px solid var(--border);border-radius:10px;
    padding:1.4rem 1.6rem;margin-bottom:1rem;}
.panel h3{font-family:'DM Serif Display',serif;font-size:1.2rem;font-weight:400;
    margin:0 0 .5rem;color:var(--text);}
.panel p{color:var(--fg-muted);font-size:.88rem;line-height:1.6;margin:0;}
.badge{display:inline-block;padding:3px 10px;border-radius:100px;
    font-size:.72rem;font-weight:600;text-transform:uppercase;letter-spacing:.06em;}
.badge-green{background:rgba(0,196,113,.15);color:var(--fg);border:1px solid rgba(0,196,113,.3);}
.badge-yellow{background:rgba(245,166,35,.12);color:var(--fg-warn);border:1px solid rgba(245,166,35,.3);}
.badge-red{background:rgba(232,80,74,.12);color:var(--fg-red);border:1px solid rgba(232,80,74,.3);}
.stButton button{border-radius:8px !important;font-weight:500 !important;}
.stButton button[kind="primary"]{background:var(--fg) !important;border:none !important;color:#000 !important;}
/* Metric cards - prevent truncation */
[data-testid="metric-container"]{
    background:var(--bg-card);border:1px solid var(--border);
    border-radius:10px;padding:1rem 1rem !important;overflow:visible;}
[data-testid="metric-container"] label{
    color:#DDE7E1 !important;font-size:.72rem !important;font-weight:600 !important;
    text-transform:uppercase;letter-spacing:.06em;white-space:normal !important;
    word-break:break-word;line-height:1.3;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{
    color:#FFFFFF !important;font-size:1.5rem !important;font-weight:700 !important;
    white-space:normal !important;overflow:visible !important;word-break:break-word;}
[data-testid="stMetricDelta"]{
    color:#00E882 !important;font-size:.78rem !important;font-weight:600 !important;}
[data-testid="stMetricDelta"][data-direction="decrease"]{color:#E8504A !important;}
.stTabs [data-baseweb="tab-list"]{gap:0;background:var(--bg-card);border:1px solid var(--border);
    border-radius:8px;padding:3px;width:fit-content;}
.stTabs [data-baseweb="tab"]{border-radius:6px;padding:6px 16px;font-size:.82rem;
    font-weight:500;color:var(--fg-muted) !important;background:transparent;}
.stTabs [aria-selected="true"]{background:var(--border) !important;color:var(--text) !important;}
.stTabs [data-baseweb="tab-panel"]{padding-top:1.5rem;}
hr{border:none;border-top:1px solid var(--border);margin:1.5rem 0;}
.stImage img{border-radius:8px;border:1px solid var(--border);}
.result-card{background:linear-gradient(135deg,rgba(0,196,113,.08),rgba(0,196,113,.03));
    border:1px solid rgba(0,196,113,.25);border-radius:12px;padding:1.6rem 2rem;margin:1.5rem 0;}
.result-card .result-label{font-size:.75rem;font-weight:600;text-transform:uppercase;
    letter-spacing:.1em;color:var(--fg);margin-bottom:.5rem;}
.result-card .result-value{font-family:'DM Serif Display',serif;font-size:2.6rem;
    color:var(--text);line-height:1;margin-bottom:.4rem;}
.result-card .result-sub{font-size:.85rem;color:var(--fg-muted);}
.budget-bar-wrap{margin:.6rem 0;}
.budget-bar-label{display:flex;justify-content:space-between;font-size:.83rem;margin-bottom:4px;color:var(--text);}
.budget-bar-track{height:8px;background:var(--border);border-radius:100px;overflow:hidden;}
.budget-bar-fill{height:100%;border-radius:100px;}
.sidebar-brand{display:flex;align-items:center;gap:10px;padding:0 0 1.2rem;
    border-bottom:1px solid var(--border);margin-bottom:1.2rem;}
.brand-icon{width:36px;height:36px;background:var(--fg);border-radius:9px;
    display:flex;align-items:center;justify-content:center;
    font-size:1.1rem;font-weight:700;color:#000;flex-shrink:0;}
.brand-name{font-family:'DM Serif Display',serif;font-size:1.3rem;color:var(--text);line-height:1;}
.brand-sub{font-size:.7rem;color:var(--fg-muted);margin-top:2px;}
.kv-row{display:flex;justify-content:space-between;align-items:center;
    padding:8px 0;border-bottom:1px solid var(--border);font-size:.85rem;}
.kv-row:last-child{border-bottom:none;}
.kv-key{color:var(--fg-muted);}
.kv-val{color:var(--text);font-weight:500;font-family:monospace;font-size:.8rem;}
.rq-card{background:var(--bg-card);border:1px solid var(--border);border-radius:10px;
    padding:1.2rem 1.5rem;margin-bottom:1rem;}
.rq-card .rq-num{font-size:.7rem;font-weight:600;color:var(--fg);text-transform:uppercase;
    letter-spacing:.1em;margin-bottom:.4rem;}
.rq-card .rq-q{font-size:.95rem;font-weight:600;color:var(--text);margin-bottom:.6rem;}
.rq-card .rq-a{font-size:.85rem;color:var(--fg-muted);line-height:1.6;}
.rq-card .rq-highlight{color:var(--text);font-weight:500;}
.chat-bubble-user{background:rgba(0,196,113,.1);border:1px solid rgba(0,196,113,.2);
    border-radius:12px 12px 4px 12px;padding:.8rem 1rem;margin:.5rem 0;font-size:.88rem;}
.chat-bubble-ai{background:var(--bg-card);border:1px solid var(--border);
    border-radius:12px 12px 12px 4px;padding:.8rem 1rem;margin:.5rem 0;font-size:.88rem;line-height:1.6;}
.model-info-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.1rem;
    min-height: 105px;
    overflow: visible;
}

.model-info-label {
    color: #DDE7E1;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.55rem;
}

.model-info-value {
    color: #FFFFFF;
    font-size: 1.45rem;
    font-weight: 700;
    line-height: 1.2;
    white-space: normal;
    overflow-wrap: anywhere;
    word-break: break-word;
}
            
.ab-metric-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(170px, 1fr));
    gap: 14px;
    margin: 1.4rem 0 1.6rem;
}

.ab-metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.1rem;
    min-height: 120px;
    overflow: visible;
}

.ab-metric-label {
    color: #DDE7E1;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    line-height: 1.25;
    margin-bottom: 0.65rem;
    white-space: normal;
}

.ab-metric-value {
    color: #FFFFFF;
    font-size: 1.85rem;
    font-weight: 700;
    line-height: 1.1;
    white-space: normal;
    word-break: keep-all;
    overflow-wrap: normal;
}

.ab-metric-delta {
    display: inline-block;
    margin-top: 0.55rem;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
    line-height: 1.2;
}

.ab-delta-positive {
    background: rgba(0, 196, 113, 0.18);
    color: #00E882;
}

.ab-delta-negative {
    background: rgba(232, 80, 74, 0.18);
    color: #FFFFFF;
}

@media (max-width: 1100px) {
    .ab-metric-grid {
        grid-template-columns: repeat(2, minmax(180px, 1fr));
    }
}

@media (max-width: 700px) {
    .ab-metric-grid {
        grid-template-columns: 1fr;
    }
}
            
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MATPLOTLIB DARK THEME
# ─────────────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":"#161D1A","axes.facecolor":"#161D1A",
    "axes.edgecolor":"#2A3F35","axes.labelcolor":"#E8EDE9",
    "xtick.color":"#E8EDE9","ytick.color":"#E8EDE9","text.color":"#E8EDE9",
    "grid.color":"#2A3F35","grid.alpha":1.0,"axes.grid":True,"grid.linewidth":0.6,
    "figure.dpi":120,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlepad":12,"axes.titlesize":12,"axes.titleweight":"bold",
    "axes.titlecolor":"#FFFFFF","axes.labelsize":10,
    "xtick.labelsize":9,"ytick.labelsize":9,"font.family":"sans-serif",
    "savefig.facecolor":"#161D1A","savefig.edgecolor":"none",
    "legend.facecolor":"#161D1A","legend.edgecolor":"#2A3F35","legend.labelcolor":"#E8EDE9",
})

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
FG="#00C471"; FG_ACC="#00E882"; FG_WARN="#F5A623"
FG_RED="#E8504A"; FG_BLUE="#4A9EE8"; FG_MUTED="#6B7E74"

INCOME_API_URL = "https://mes1205-fingo.hf.space/predict/income"
CHAT_API_URL   = "https://mes1205-fingo.hf.space/chat"

GIG_TYPES = ["ojek_online","kurir","jualan_online","freelance_desain",
             "freelance_it","content_creator","tutor","pekerja_harian"]
GIG_LABELS = {
    "ojek_online":"Ojek Online","kurir":"Kurir","jualan_online":"Jualan Online",
    "freelance_desain":"Freelance Desain","freelance_it":"Freelance IT",
    "content_creator":"Content Creator","tutor":"Tutor","pekerja_harian":"Pekerja Harian"
}

HEDONIC_CATS = {"Hiburan","Belanja"}
CATEGORY_TYPES = {
    "Makanan":"utilitarian","Transportasi":"utilitarian","Pendidikan":"utilitarian",
    "Kesehatan":"utilitarian","Tagihan":"utilitarian",
    "Hiburan":"hedonic","Belanja":"hedonic","Lainnya":"neutral"
}

# Exact features the model was trained on (verified from feature_names_in_)
IMP_MODEL_FEATURES = [
    "amount","amount_log","amount_z","amount_score","impulsive_score",
    "hour","day_of_week","driver_count",
    "category","metode_pembayaran","source","time_segment",
    "category_type","is_hedonic_category","is_night","is_weekend","signal_band"
]

METODE_OPTIONS = [
    "Cash","Credit Card","Debit Card","Online Payment","SPayLater",
    "COD (Bayar di Tempat)","Kartu Kredit/Debit","Saldo ShopeePay",
    "Indomaret/i.Saku","BCA OneKlik"
]

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def fmt_idr(v):
    """Full IDR format without rb/jt abbreviation."""
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "N/A"
    return f"Rp {float(v):,.0f}"

def fmt_idr_full(v):
    """Full IDR format without rb/jt abbreviation."""
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "N/A"
    return f"Rp {float(v):,.0f}"

def no_data(msg):
    st.markdown(
        f'<div style="background:var(--bg-card);border:1px dashed var(--border);'
        f'border-radius:10px;padding:2rem;text-align:center;color:var(--fg-muted);'
        f'font-size:.88rem;">{msg}</div>', unsafe_allow_html=True)

def _try_paths(*paths):
    for p in paths:
        p = Path(p)
        if p.exists(): return p
    return None

# ─────────────────────────────────────────────────────────────────────────────
# IMPULSIVE FEATURE DERIVATION
# Used both for Coba Deteksi (manual input) and to patch test set missing cols
# ─────────────────────────────────────────────────────────────────────────────
def compute_impulsive_score_and_drivers(row_series, amt_mean=150000, amt_std=200000, amt_med=150000):
    """
    Given a pandas Series (one row of a DataFrame), compute:
      - impulsive_score  (0–10 float)
      - driver_count     (int 0–4)
    Uses available columns: amount_z, is_night, is_weekend, category (via category_score col or lookup),
    night_score, category_score, weekend_score if present.
    """
    # --- amount_z
    amount_z = row_series.get("amount_z", 0.0)
    if pd.isna(amount_z): amount_z = 0.0

    # --- is_night / is_weekend
    is_night   = bool(row_series.get("is_night", False))
    is_weekend = bool(row_series.get("is_weekend", False))

    # --- category_score: prefer existing column, else derive
    if "category_score" in row_series.index and not pd.isna(row_series["category_score"]):
        cat_score = float(row_series["category_score"])
    else:
        cat_map = {"Hiburan":2.0,"Belanja":1.5,"Makanan":0.5,
                   "Transportasi":0.3,"Pendidikan":0.0,"Kesehatan":0.0,
                   "Tagihan":0.0,"Lainnya":0.5}
        cat_score = cat_map.get(str(row_series.get("category","Lainnya")), 0.5)

    # --- night_score: prefer existing column
    if "night_score" in row_series.index and not pd.isna(row_series["night_score"]):
        night_score = float(row_series["night_score"])
    else:
        hour = int(row_series.get("hour", 12))
        night_score = 1.5 if is_night else (0.5 if hour >= 20 else 0.0)

    # --- weekend_score: prefer existing column
    if "weekend_score" in row_series.index and not pd.isna(row_series["weekend_score"]):
        weekend_score = float(row_series["weekend_score"])
    else:
        weekend_score = 0.5 if is_weekend else 0.0

    amt_component = min(float(amount_z) * 0.5, 2.0) if float(amount_z) > 0 else 0.0

    # If dataset has fingo_impulse_signal, use it directly
    if "fingo_impulse_signal" in row_series.index and not pd.isna(row_series.get("fingo_impulse_signal")):
        impulsive_score = float(np.clip(row_series["fingo_impulse_signal"], 0, 10))
    else:
        impulsive_score = float(np.clip(night_score + cat_score + weekend_score + amt_component, 0, 10))

    # --- driver_count
    is_hedonic = bool(row_series.get("is_hedonic_category", False))
    driver_night   = 1 if is_night else 0
    driver_hedonic = 1 if is_hedonic else 0
    driver_high    = 1 if float(amount_z) > 1.5 else 0
    driver_weekend = 1 if is_weekend else 0
    driver_count   = driver_night + driver_hedonic + driver_high + driver_weekend

    return impulsive_score, driver_count


def build_model_row(amount, category, metode_bayar, hour, day_of_week,
                    is_weekend, is_night, time_segment, df_ref):
    """Build a single-row DataFrame matching IMP_MODEL_FEATURES exactly."""
    if df_ref is not None and len(df_ref) > 0 and "amount" in df_ref.columns:
        amt_mean = df_ref["amount"].mean()
        amt_std  = df_ref["amount"].std()
        amt_med  = float(np.percentile(df_ref["amount"].dropna(), 50))
    else:
        amt_mean = 150000; amt_std = 200000; amt_med = 150000

    amount_log   = float(np.log1p(amount))
    amount_z     = float((amount - amt_mean) / amt_std) if amt_std > 0 else 0.0
    amount_score = float(np.clip(amount / amt_med if amt_med > 0 else 1.0, 0, 5))
    is_hedonic   = category in HEDONIC_CATS
    cat_type     = CATEGORY_TYPES.get(category, "neutral")

    cat_score_map = {"Hiburan":2.0,"Belanja":1.5,"Makanan":0.5,
                     "Transportasi":0.3,"Pendidikan":0.0,"Kesehatan":0.0,
                     "Tagihan":0.0,"Lainnya":0.5}
    cat_score    = cat_score_map.get(category, 0.5)
    night_score  = 1.5 if is_night else (0.5 if hour >= 20 else 0.0)
    wknd_score   = 0.5 if is_weekend else 0.0
    amt_comp     = min(amount_z * 0.5, 2.0) if amount_z > 0 else 0.0
    imp_score    = float(np.clip(night_score + cat_score + wknd_score + amt_comp, 0, 10))

    if imp_score >= 4.0:   sig = "high"
    elif imp_score >= 2.0: sig = "watch"
    else:                   sig = "low"

    d_night   = 1 if is_night else 0
    d_hedonic = 1 if is_hedonic else 0
    d_high    = 1 if amount_z > 1.5 else 0
    d_wknd    = 1 if is_weekend else 0
    drv_count = d_night + d_hedonic + d_high + d_wknd

    row = pd.DataFrame([{
        "amount":             float(amount),
        "amount_log":         amount_log,
        "amount_z":           amount_z,
        "amount_score":       amount_score,
        "impulsive_score":    imp_score,
        "hour":               int(hour),
        "day_of_week":        int(day_of_week),
        "driver_count":       int(drv_count),
        "category":           str(category),
        "metode_pembayaran":  str(metode_bayar),
        "source":             "manual_input",
        "time_segment":       str(time_segment),
        "category_type":      str(cat_type),
        "is_hedonic_category":bool(is_hedonic),
        "is_night":           bool(is_night),
        "is_weekend":         bool(is_weekend),
        "signal_band":        sig,
    }])
    return row, imp_score, sig, drv_count


def patch_test_df_for_model(df, expected_cols):
    """
    Given a test DataFrame that may be missing 'impulsive_score' and/or 'driver_count',
    compute and add them so evaluation can proceed correctly.
    Returns patched DataFrame and a list of columns that were computed (for display).
    """
    df = df.copy()
    computed = []

    if "impulsive_score" not in df.columns:
        # Use fingo_impulse_signal if present
        if "fingo_impulse_signal" in df.columns:
            df["impulsive_score"] = df["fingo_impulse_signal"].clip(0, 10)
        else:
            # Derive from component scores
            amt_z_col = df["amount_z"] if "amount_z" in df.columns else 0.0
            ns = df["night_score"] if "night_score" in df.columns else 0.0
            cs = df["category_score"] if "category_score" in df.columns else 0.5
            ws = df["weekend_score"] if "weekend_score" in df.columns else 0.0
            amt_comp = (amt_z_col * 0.5).clip(upper=2.0).where(amt_z_col > 0, 0.0)
            df["impulsive_score"] = (ns + cs + ws + amt_comp).clip(0, 10)
        computed.append("impulsive_score (computed)")

    if "driver_count" not in df.columns:
        is_night_col   = df["is_night"].astype(int)   if "is_night"   in df.columns else 0
        is_wknd_col    = df["is_weekend"].astype(int) if "is_weekend" in df.columns else 0
        is_hedonic_col = df["is_hedonic_category"].astype(int) if "is_hedonic_category" in df.columns else 0
        amt_z_col      = df["amount_z"] if "amount_z" in df.columns else 0.0
        is_high        = (amt_z_col > 1.5).astype(int)
        df["driver_count"] = is_night_col + is_wknd_col + is_hedonic_col + is_high
        computed.append("driver_count (computed)")

    return df, computed

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADERS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_survey():
    p = _try_paths(INCOME_PROC_DIR / "survey_temporal_mapped.csv")
    if not p: return None
    df = pd.read_csv(p)
    if "timestamp_parsed" in df.columns:
        df["timestamp_parsed"] = pd.to_datetime(df["timestamp_parsed"], errors="coerce")
    return df

@st.cache_data(show_spinner=False)
def load_survey_weekly_long():
    p = _try_paths(INCOME_PROC_DIR / "survey_weekly_income_long.csv")
    if not p: return None
    df = pd.read_csv(p)
    for c in ["period_start", "period_end"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return df

@st.cache_data(show_spinner=False)
def load_synthetic():
    p = _try_paths(INCOME_SYNTH_DIR / "synthetic_52week_user_income.csv")
    if not p: return None
    return pd.read_csv(p)

@st.cache_data(show_spinner=False)
def load_income_features():
    p = _try_paths(INCOME_PROC_DIR / "income_features.csv")
    if not p: return None
    return pd.read_csv(p)

@st.cache_data(show_spinner=False)
def load_training_metadata():
    p = _try_paths(INCOME_RESULTS_DIR / "training_metadata.json")
    if not p: return None
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

@st.cache_data(show_spinner=False)
def load_regression_metrics():
    p = _try_paths(INCOME_RESULTS_DIR / "regression_metrics.csv")
    if not p: return None
    return pd.read_csv(p)

@st.cache_data(show_spinner=False)
def load_classification_metrics():
    p = _try_paths(INCOME_RESULTS_DIR / "classification_metrics.csv")
    if not p: return None
    return pd.read_csv(p)

@st.cache_data(show_spinner=False)
def load_predictions_test():
    p = _try_paths(INCOME_RESULTS_DIR / "predictions_test.csv")
    if not p: return None
    return pd.read_csv(p)

@st.cache_data(show_spinner=False)
def load_impulsive_data():
    for nm in ["04_Merged_labeled_transaction.csv",
               "transactions_labeled.csv","Merged_labeled_transaction.csv"]:
        p = _try_paths(IMP_FINAL_DIR / nm, DATA_DIR / "impulsive" / nm)
        if p: return pd.read_csv(p)
    return None

@st.cache_data(show_spinner=False)
def load_impulsive_test():
    p = _try_paths(
        IMP_SPLIT_DIR / "test_df.csv",
        BASE_DIR / "data" / "impulsive" / "04_split_final" / "test_df.csv",
        BASE_DIR / "data" / "impulsive" / "test_df.csv",
        IMP_FINAL_DIR / "test_df.csv",
    )
    if not p: return None
    return pd.read_csv(p)

@st.cache_data(show_spinner=False)
def load_impulsive_split_summary():
    paths = {
        "Train": _try_paths(IMP_SPLIT_DIR / "train_df.csv"),
        "Validation": _try_paths(IMP_SPLIT_DIR / "validation_df.csv"),
        "Test": _try_paths(IMP_SPLIT_DIR / "test_df.csv"),
    }
    summary = {}
    for name, path in paths.items():
        if path:
            try:
                summary[name] = len(pd.read_csv(path, usecols=[0]))
            except Exception:
                summary[name] = None
        else:
            summary[name] = None
    return summary

@st.cache_resource(show_spinner=False)
def load_income_bundle():
    p = _try_paths(MODELS_DIR / "fingo_deploy.pkl")
    if not p: return None
    try:
        with open(p, "rb") as f: return pickle.load(f)
    except Exception: return None

@st.cache_resource(show_spinner=False)
def load_impulsive_model():
    try:
        import joblib
        p = _try_paths(
            MODELS_DIR / "fingo_label_classifier.joblib",
            MODELS_DIR / "impulsive_classifier.joblib",
        )
        if not p: return None
        return joblib.load(p)
    except Exception: return None

@st.cache_resource(show_spinner=False)
def load_impulsive_eval_bundle():
    p = _try_paths(
        BASE_DIR / "data" / "impulsive" / "evaluation" / "impulsive_eval_bundle.pkl",
        MODELS_DIR / "impulsive_eval_bundle.pkl",
        BASE_DIR / "data" / "models" / "impulsive_eval_bundle.pkl",
    )
    if not p:
        return None
    with open(p, "rb") as f:
        return pickle.load(f)


@st.cache_resource(show_spinner=False)
def load_impulsive_official_eval_result():
    p = _try_paths(
        BASE_DIR / "data" / "impulsive" / "evaluation" / "random_split_with_score_eval_result.pkl",
        MODELS_DIR / "random_split_with_score_eval_result.pkl",
    )
    if not p:
        return None
    with open(p, "rb") as f:
        return pickle.load(f)


@st.cache_data(show_spinner=False)
def load_impulsive_official_predictions():
    p = _try_paths(
        BASE_DIR / "data" / "impulsive" / "evaluation" / "random_split_with_score_predictions.csv",
        MODELS_DIR / "random_split_with_score_predictions.csv",
    )
    if not p:
        return None
    return pd.read_csv(p)

# ─────────────────────────────────────────────────────────────────────────────
# INCOME API
# ─────────────────────────────────────────────────────────────────────────────
def call_income_api(income_history_4w, usia, hari_kerja, jam_kerja, gig_type):
    payload = {
        "income_history": [float(x) for x in income_history_4w],
        "usia": int(usia),
        "hari_kerja_per_minggu": int(hari_kerja),
        "jam_kerja_per_hari": int(jam_kerja),
    }

    if len(payload["income_history"]) != 4:
        return None, "Income history harus berisi tepat 4 nilai pendapatan mingguan terakhir."
    for g in GIG_TYPES:
        payload[f"gig_{g}"] = 1 if g == gig_type else 0
    try:
        resp = requests.post(INCOME_API_URL, json=payload, timeout=30)
        if resp.status_code == 200: return resp.json(), None
        try: detail = resp.json().get("detail", resp.text)
        except Exception: detail = resp.text
        return None, f"API error {resp.status_code}: {detail}"
    except requests.exceptions.Timeout:
        return None, "Request timeout (30 detik). Endpoint mungkin sedang sleep."
    except requests.exceptions.ConnectionError:
        return None, "Tidak dapat terhubung. Periksa koneksi atau status HuggingFace Space."
    except Exception as e:
        return None, f"Error: {e}"

# ─────────────────────────────────────────────────────────────────────────────
# INCOME LOCAL FALLBACK
# ─────────────────────────────────────────────────────────────────────────────
def predict_income_local(income_history, gig_type, usia, hari_kerja, jam_kerja,
                         target_month, target_week):
    bundle = load_income_bundle()
    if bundle is None: return None, None
    try:
        FEAT     = bundle["feature_columns"]
        sk_reg   = bundle["sk_reg_model"]
        sk_cls   = bundle["sk_cls_model"]
        f_scaler = bundle["feature_scaler"]
        i_min    = bundle["income_min"]
        i_max    = bundle["income_max"]
        h = np.array(income_history, dtype=float)
        w1,w2,w3,w4 = h[-1],h[-2],h[-3],h[-4]
        lags4 = h[-4:]; lags8 = h[-8:] if len(h)>=8 else h
        rm4=np.mean(lags4); rs4=np.std(lags4)
        rm8=np.mean(lags8); rs8=np.std(lags8)
        fd = {c:0.0 for c in FEAT}
        fd.update({"target_idx":1,"current_income":w1,"lag_2_income":w2,
                   "lag_3_income":w3,"lag_4_income":w4,
                   "rolling_mean_4w":rm4,"rolling_std_4w":rs4,
                   "rolling_min_4w":np.min(lags4),"rolling_max_4w":np.max(lags4),
                   "rolling_range_4w":np.max(lags4)-np.min(lags4),
                   "rolling_median_4w":np.median(lags4),
                   "rolling_cv_4w":rs4/rm4 if rm4>0 else 0,
                   "rolling_last_vs_median_pct":(w1-np.median(lags4))/np.median(lags4) if np.median(lags4)>0 else 0,
                   "rolling_mean_2w":np.mean([w2,w1]),"rolling_mean_8w":rm8,"rolling_std_8w":rs8,
                   "income_trend_4w_abs":w1-w4,"income_trend_4w_pct":(w1-w4)/w4 if w4>0 else 0,
                   "last_income_change_abs":w1-w2,"last_income_change_pct":(w1-w2)/w2 if w2>0 else 0,
                   "income_growth_1w":(w1-w2)/w2 if w2>0 else 0,
                   "income_volatility":rs4/rm4 if rm4>0 else 0,
                   "trend_slope_4w":float(np.polyfit(range(4),lags4,1)[0]),
                   "is_previous_week_up":1 if w1>w2*1.05 else 0,
                   "is_previous_week_down":1 if w1<w2*0.95 else 0,
                   "is_previous_week_stable":1 if not(w1>w2*1.05) and not(w1<w2*0.95) else 0,
                   "lag_ratio_1_to_mean":w1/rm4 if rm4>0 else 1.0,
                   "target_month":target_month,"target_week_of_month":target_week,
                   "target_quarter":(target_month-1)//3+1,
                   "target_is_month_start":1 if target_week==1 else 0,
                   "target_is_month_end":1 if target_week==4 else 0,
                   "target_is_payday_period":1 if target_week in[1,4] else 0,
                   "target_is_ramadan_lebaran":1 if target_month in[3,4] else 0,
                   "target_is_harbolnas":1 if target_month in[11,12] else 0,
                   "target_is_christmas_year_end":1 if target_month==12 else 0,
                   "target_is_new_year":1 if target_month==1 else 0,
                   "usia":usia,"hari_kerja_per_minggu":hari_kerja,
                   "jam_kerja_per_hari":jam_kerja,"total_jam_seminggu":hari_kerja*jam_kerja})
        for g in GIG_TYPES: fd[f"gig_{g}"]=1 if g==gig_type else 0
        X = pd.DataFrame([fd])[FEAT].fillna(0)
        income_scaled_cols = bundle.get("income_cols_scaled",[])
        for c in income_scaled_cols:
            if c in X.columns:
                norm = (X[c].values[0]-i_min)/(i_max-i_min) if (i_max-i_min)>0 else 0
                X[c] = np.clip(norm,0,1)
        try: Xs = f_scaler.transform(X)
        except Exception: Xs = X.values
        pred_norm = sk_reg.predict(Xs)[0]
        pred_idr  = float(np.clip(pred_norm*(i_max-i_min)+i_min, i_min, i_max))
        try:
            dc = sk_cls.predict(Xs)[0]
            dir_pred = {0:"Down",1:"Stable",2:"Up"}.get(int(dc),"Stable")
        except Exception: dir_pred = "Stable"
        return pred_idr, dir_pred
    except Exception: return None, None

# ─────────────────────────────────────────────────────────────────────────────
# CHAT API
# ─────────────────────────────────────────────────────────────────────────────
def call_chat_api(user_message, income, expense, budget_remaining, impulsive_count):
    payload = {"user_message": user_message,
               "financial_context":{"income":income,"expense":expense,
                                     "budget_remaining":budget_remaining,
                                     "impulsive_count":impulsive_count}}
    try:
        resp = requests.post(CHAT_API_URL, json=payload, timeout=30)
        if resp.status_code == 200: return resp.json().get("reply",""), None
        if resp.status_code == 429: return None, "Gemini API rate limit tercapai. Coba lagi beberapa saat."
        try: detail = resp.json().get("detail", resp.text)
        except Exception: detail = resp.text
        return None, f"API error {resp.status_code}: {detail}"
    except requests.exceptions.Timeout: return None, "Request timeout. Endpoint mungkin sedang sleep."
    except Exception as e: return None, f"Error: {e}"

# ─────────────────────────────────────────────────────────────────────────────
# CONFUSION MATRIX
# ─────────────────────────────────────────────────────────────────────────────
def plot_confusion_matrix(cm, classes):
    fig, ax = plt.subplots(figsize=(7, 5.5))

    sns.heatmap(
        cm,
        annot=False,
        cmap="YlGnBu",
        xticklabels=classes,
        yticklabels=classes,
        linewidths=0.8,
        linecolor="#1E2B25",
        cbar=True,
        ax=ax
    )

    vmax = cm.max() if cm.max() > 0 else 1

    for i in range(len(classes)):
        for j in range(len(classes)):
            val = cm[i, j]
            norm_val = val / vmax

            # teks putih untuk cell gelap, teks hitam untuk cell terang
            tc = "#FFFFFF" if norm_val >= 0.45 else "#111111"

            ax.text(
                j + 0.5,
                i + 0.5,
                f"{val}",
                ha="center",
                va="center",
                color=tc,
                fontsize=16,
                fontweight="bold"
            )

    ax.set_xlabel("Predicted Label", color="#FFFFFF", fontsize=11, fontweight="bold")
    ax.set_ylabel("Actual Label", color="#FFFFFF", fontsize=11, fontweight="bold")
    ax.set_title("Confusion Matrix - Test Set", color="#FFFFFF", fontsize=13, fontweight="bold")
    ax.tick_params(axis="x", colors="#FFFFFF", labelsize=10)
    ax.tick_params(axis="y", colors="#FFFFFF", labelsize=10)

    try:
        cbar = ax.collections[0].colorbar
        cbar.ax.yaxis.set_tick_params(color="#FFFFFF")
        plt.setp(cbar.ax.get_yticklabels(), color="#FFFFFF")
    except Exception:
        pass

    plt.tight_layout()
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-icon">F</div>
        <div>
            <div class="brand-name">Fingo</div>
            <div class="brand-sub">Financial Intelligence Platform</div>
        </div>
    </div>""", unsafe_allow_html=True)

    module = st.radio("module", [
        "Insight & Kesimpulan", "Income Predictor", "Impulsive Detector"
    ], label_visibility="collapsed")

    st.markdown("<hr style='border-color:var(--border);margin:1rem 0'>", unsafe_allow_html=True)

    df_s = load_survey()
    df_sy = load_synthetic()
    df_imp_sidebar = load_impulsive_data()
    imp_split = load_impulsive_split_summary()
    imp_eval_pred = load_impulsive_official_predictions()
    income_meta = load_training_metadata()

    n_resp = len(df_s) if df_s is not None else 0
    n_users = (
        df_sy["synthetic_user_id"].nunique()
        if df_sy is not None and "synthetic_user_id" in df_sy.columns else 0
    )
    n_synth_rows = len(df_sy) if df_sy is not None else 0
    n_income_features = (
        int(income_meta.get("train_rows", 0))
        + int(income_meta.get("val_rows", 0))
        + int(income_meta.get("test_rows", 0))
        if income_meta is not None else 0
    )
    n_imp_rows = len(df_imp_sidebar) if df_imp_sidebar is not None else 0
    n_imp_eval = len(imp_eval_pred) if imp_eval_pred is not None else 0

    if module == "Income Predictor":
        sidebar_title = "Income Predictor Data"
        sidebar_owner = "DS2: Clarisya Adeline"
        sidebar_scope = "Repo income analysis"
        sidebar_rows = [
            ("Responden Survey", f"{n_resp:,}"),
            ("Synthetic Users", f"{n_users:,}"),
            ("Synthetic Rows", f"{n_synth_rows:,}"),
            ("Model Rows", f"{n_income_features:,}" if n_income_features else "N/A"),
        ]
    elif module == "Impulsive Detector":
        sidebar_title = "Impulsive Detector Data"
        sidebar_owner = "DS1: Nayyara"
        sidebar_scope = "Transaction labeling"
        sidebar_rows = [
            ("Labeled Transactions", f"{n_imp_rows:,}"),
            ("Train Rows", f"{imp_split.get('Train'):,}" if imp_split.get("Train") is not None else "N/A"),
            ("Validation Rows", f"{imp_split.get('Validation'):,}" if imp_split.get("Validation") is not None else "N/A"),
            ("Test Rows", f"{imp_split.get('Test'):,}" if imp_split.get("Test") is not None else "N/A"),
            ("Eval Predictions", f"{n_imp_eval:,}" if n_imp_eval else "N/A"),
        ]
    else:
        sidebar_title = "Project Data Snapshot"
        sidebar_owner = "CC26-PSU217"
        sidebar_scope = "Fingo Team"
        sidebar_rows = [
            ("Income Survey", f"{n_resp:,}"),
            ("Income Synthetic Users", f"{n_users:,}"),
            ("Impulsive Transactions", f"{n_imp_rows:,}"),
            ("Tim", "CC26-PSU217"),
        ]

    sidebar_rows_html = "".join(
        f'<div class="kv-row"><span class="kv-key">{k}</span><span class="kv-val">{v}</span></div>'
        for k, v in sidebar_rows
    )
    st.markdown(f"""
    <div style="font-size:.73rem;color:var(--fg-muted);line-height:2">
        <div style="font-size:.72rem;font-weight:700;color:#E8EDE9;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.45rem">
            {sidebar_title}
        </div>
        {sidebar_rows_html}
        <div class="kv-row"><span class="kv-key">Owner</span><span class="kv-val">{sidebar_owner}</span></div>
        <div class="kv-row"><span class="kv-key">Scope</span><span class="kv-val">{sidebar_scope}</span></div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:var(--border);margin:1rem 0'>", unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:.7rem;color:var(--fg-muted);line-height:1.8">'
        '<strong style="color:#E8EDE9">Team Members</strong><br>'
        'DS1: Nayyara<br>'
        'DS2: Clarisya Adeline<br>'
        'AI1: M. Fachri<br>'
        'AI2: Martha Meslina<br>'
        'Coding Camp 2026 - DBS Foundation<br><br>'
        '&copy; 2026 Fingo Team</div>',
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════════════════════════════════
# MODULE 1 - INSIGHT & KESIMPULAN
# ══════════════════════════════════════════════════════════════════════════════
if module == "Insight & Kesimpulan":
    st.markdown("""
    <div class="page-header">
        <h1>Insight &amp; Kesimpulan Keseluruhan</h1>
        <p>Ringkasan jawaban atas 5 Research Questions proyek Fingo CC26-PSU217</p>
    </div>""", unsafe_allow_html=True)

    df_imp   = load_impulsive_data()
    df_pred  = load_predictions_test()
    clf_imp  = load_impulsive_model()

    # RQ1
    st.markdown('<div class="section-header">RQ1 - Persentase Transaksi Impulsif</div>', unsafe_allow_html=True)
    if df_imp is not None and "label" in df_imp.columns:
        total = len(df_imp)
        lvc   = df_imp["label"].value_counts()
        n_aman,n_pert,n_imp = lvc.get("AMAN",0),lvc.get("PERTIMBANGAN",0),lvc.get("IMPULSIF",0)
        p_aman=n_aman/total*100; p_pert=n_pert/total*100; p_imp=n_imp/total*100

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Total Transaksi", f"{total:,}")
        c2.metric("AMAN",            f"{n_aman:,}", delta=f"{p_aman:.1f}%")
        c3.metric("PERTIMBANGAN",    f"{n_pert:,}", delta=f"{p_pert:.1f}%")
        c4.metric("IMPULSIF",        f"{n_imp:,}",  delta=f"{p_imp:.1f}%")

        st.markdown(f"""
        <div class="rq-card">
            <div class="rq-num">Research Question 1</div>
            <div class="rq-q">Berapa persentase transaksi impulsif pada gig worker dan mahasiswa Gen Z?</div>
            <div class="rq-a">
                Dari <span class="rq-highlight">{total:,} transaksi</span>,
                terdapat <span class="rq-highlight">{n_imp:,} IMPULSIF ({p_imp:.1f}%)</span>,
                <span class="rq-highlight">{n_pert:,} PERTIMBANGAN ({p_pert:.1f}%)</span>, dan
                <span class="rq-highlight">{n_aman:,} AMAN ({p_aman:.1f}%)</span>.
                Total <span class="rq-highlight">{p_imp+p_pert:.1f}% transaksi</span> berpotensi impulsif.
            </div>
        </div>""", unsafe_allow_html=True)

        fig,ax = plt.subplots(figsize=(5,4))
        wedges,texts = ax.pie([n_aman,n_pert,n_imp],
            labels=[f"AMAN\n{p_aman:.1f}%",f"PERTIMBANGAN\n{p_pert:.1f}%",f"IMPULSIF\n{p_imp:.1f}%"],
            colors=[FG,FG_WARN,FG_RED], startangle=90, wedgeprops=dict(width=0.6))
        for t in texts: t.set_color("#E8EDE9"); t.set_fontsize(9)
        ax.set_title("Distribusi Label Transaksi", color="#FFFFFF")
        st.pyplot(fig, use_container_width=False); plt.close()
    else:
        no_data("Dataset impulsive tidak ditemukan. Pastikan file 04_Merged_labeled_transaction.csv ada di streamlit/data/impulsive/")

    # RQ2
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">RQ2 - Waktu &amp; Kategori Transaksi Impulsif</div>', unsafe_allow_html=True)
    if df_imp is not None and "label" in df_imp.columns:
        df_i = df_imp.copy()
        df_i["is_imp_bin"] = (df_i["label"]=="IMPULSIF").astype(int)
        col_l,col_r = st.columns(2, gap="large")
        cat_rate=ts_rate=None
        with col_l:
            if "category" in df_i.columns:
                cat_rate = (df_i.groupby("category")
                    .agg(count=("is_imp_bin","count"),imp_rate=("is_imp_bin","mean"))
                    .reset_index().sort_values("imp_rate",ascending=False))
                fig,ax = plt.subplots(figsize=(7,4.5))
                bars = ax.barh(cat_rate["category"], cat_rate["imp_rate"]*100,
                    color=[FG_RED if r>0.15 else FG_WARN if r>0.05 else FG_MUTED for r in cat_rate["imp_rate"]],
                    height=0.6, alpha=0.9)
                for bar,v in zip(bars,cat_rate["imp_rate"]):
                    ax.text(v*100+0.3, bar.get_y()+bar.get_height()/2,
                        f"{v*100:.1f}%", va="center", fontsize=9, color="#FFFFFF", fontweight="bold")
                ax.set_title("Impulsive Rate per Kategori", color="#FFFFFF")
                ax.set_xlabel("Impulsive Rate (%)"); ax.invert_yaxis()
                plt.tight_layout(pad=0.8); st.pyplot(fig, use_container_width=True); plt.close()
        with col_r:
            if "time_segment" in df_i.columns:
                ts_rate = (df_i.groupby("time_segment")
                    .agg(count=("is_imp_bin","count"),imp_rate=("is_imp_bin","mean"))
                    .reset_index().sort_values("imp_rate",ascending=False))
                fig,ax = plt.subplots(figsize=(7,4.5))
                bars = ax.bar(ts_rate["time_segment"], ts_rate["imp_rate"]*100,
                    color=[FG_RED if r>0.15 else FG_WARN if r>0.05 else FG_MUTED for r in ts_rate["imp_rate"]],
                    alpha=0.9)
                for bar,v in zip(bars,ts_rate["imp_rate"]):
                    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
                        f"{v*100:.1f}%", ha="center", fontsize=9, color="#FFFFFF", fontweight="bold")
                ax.set_title("Impulsive Rate per Time Segment", color="#FFFFFF")
                ax.set_ylabel("Impulsive Rate (%)")
                plt.xticks(rotation=30,ha="right",fontsize=9)
                plt.tight_layout(pad=0.8); st.pyplot(fig, use_container_width=True); plt.close()

        top_cat      = cat_rate.iloc[0]["category"]    if cat_rate is not None else "N/A"
        top_ts       = ts_rate.iloc[0]["time_segment"] if ts_rate  is not None else "N/A"
        top_cat_rate = cat_rate.iloc[0]["imp_rate"]*100 if cat_rate is not None else 0
        top_ts_rate  = ts_rate.iloc[0]["imp_rate"]*100  if ts_rate  is not None else 0
        wknd_txt=""
        if "is_weekend" in df_i.columns:
            wr = df_i.groupby("is_weekend")["is_imp_bin"].mean()
            if 1 in wr.index and 0 in wr.index:
                wknd_txt=f"Transaksi akhir pekan memiliki impulsive rate {wr[1]*100:.1f}% vs {wr[0]*100:.1f}% di hari kerja."
        st.markdown(f"""
        <div class="rq-card">
            <div class="rq-num">Research Question 2</div>
            <div class="rq-q">Pada waktu dan kategori apa transaksi impulsif paling sering terjadi?</div>
            <div class="rq-a">
                Kategori paling impulsif: <span class="rq-highlight">{top_cat} ({top_cat_rate:.1f}%)</span>.
                Segmen waktu paling impulsif: <span class="rq-highlight">{top_ts} ({top_ts_rate:.1f}%)</span>.
                {wknd_txt}
            </div>
        </div>""", unsafe_allow_html=True)

    # RQ3
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">RQ3 - A/B Testing: Efektivitas AI Warning</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="rq-card">
        <div class="rq-num">Research Question 3</div>
        <div class="rq-q">Apakah sistem peringatan AI dapat mengurangi over-budget?</div>
        <div class="rq-a">
            <strong style="color:#E8EDE9">Income Predictor A/B Testing (Notebook 10):</strong><br>
            3.000 user sintetis (Control: 1.502, Treatment: 1.498).
            Mean budget error turun dari <strong style="color:#E8EDE9">Rp 47rb</strong> menjadi
            <strong style="color:#00C471">Rp 14rb</strong> (reduksi -70.14%).
            Mann-Whitney U p-value = 0.000000. Cohen's d = -1.2188 (efek besar).<br><br>
            <strong style="color:#E8EDE9">Impulsive Detector A/B Testing:</strong>
            Belum tersedia dalam file dashboard ini.
        </div>
    </div>""", unsafe_allow_html=True)

    # RQ4
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        '<div class="section-header">RQ4 - Akurasi Model Income Predictor Final</div>',
        unsafe_allow_html=True
    )

    bundle = load_income_bundle()

    mae_val = None
    rmse_val = None
    mae_norm_val = None
    rmse_norm_val = None
    r2_val = None
    acc_val = None
    f1_val = None
    tol_5 = None

    local_note = ""

    if bundle is not None:
        income_min = bundle.get("income_min", None)
        income_max = bundle.get("income_max", None)

        range_text = ""
        if income_min is not None and income_max is not None:
            range_text = (
                f" | Training range: {fmt_idr_full(float(income_min))} - "
                f"{fmt_idr_full(float(income_max))}"
            )

        local_note = (
            f"Model: {bundle.get('final_reg_name', 'N/A')}"
            f"{range_text}"
        )

        # Prioritas utama: actual metrics dari fingo_deploy.pkl terbaru
        mae_val = bundle.get("final_reg_test_mae_idr", None)
        rmse_val = bundle.get("final_reg_test_rmse_idr", None)

        mae_norm_val = bundle.get("final_reg_test_mae_norm", None)
        rmse_norm_val = bundle.get("final_reg_test_rmse_norm", None)

        r2_val = bundle.get("final_reg_test_r2", None)
        acc_val = bundle.get("final_cls_test_accuracy", None)
        f1_val = bundle.get("final_cls_test_macro_f1", None)
        tol_5 = bundle.get("tolerance_acc_5pct", None)

    # Fallback jika PKL belum punya actual metrics
    if mae_val is None and df_pred is not None and len(df_pred) > 0:
        if "absolute_error" in df_pred.columns:
            mae_val = df_pred["absolute_error"].mean()

        if "absolute_error_norm" in df_pred.columns:
            mae_norm_val = df_pred["absolute_error_norm"].mean()

        if "predicted_income_norm" in df_pred.columns and "actual_income_norm" in df_pred.columns:
            resid_norm = df_pred["actual_income_norm"] - df_pred["predicted_income_norm"]
            rmse_norm_val = float(np.sqrt((resid_norm ** 2).mean()))

        if "direction_correct" in df_pred.columns:
            acc_val = df_pred["direction_correct"].mean()

        if "next_week_income" in df_pred.columns and "predicted_next_week_income" in df_pred.columns:
            resid = df_pred["next_week_income"] - df_pred["predicted_next_week_income"]
            rmse_val = float(np.sqrt((resid ** 2).mean()))
            ss_res = (resid ** 2).sum()
            ss_tot = ((df_pred["next_week_income"] - df_pred["next_week_income"].mean()) ** 2).sum()
            r2_val = 1 - ss_res / ss_tot if ss_tot > 0 else None

       note_html = f"<br>{local_note}" if local_note else ""

        st.html(f"""
        <div class="panel" style="margin-bottom:.5rem">
          <div style="color:var(--fg-warn);font-size:.82rem;line-height:1.6">
            Project Plan awal: LSTM TensorFlow. Implementasi final:
            <strong style="color:#E8EDE9">GradientBoosting / Ensemble (fingo_deploy.pkl)</strong>
            via API <strong style="color:#E8EDE9">https://mes1205-fingo.hf.space/predict/income</strong>.
            {note_html}
          </div>
        </div>
        """)

    if mae_norm_val is not None or mae_val is not None:
        mae_norm_display = f"{mae_norm_val:.4f}" if mae_norm_val is not None else "N/A"
        rmse_norm_display = f"{rmse_norm_val:.4f}" if rmse_norm_val is not None else "N/A"
        r2_display = f"{r2_val:.4f}" if r2_val is not None else "N/A"
        acc_display = f"{acc_val * 100:.2f}%" if acc_val is not None else "N/A"
        f1_display = f"{f1_val:.4f}" if f1_val is not None else "N/A"

        mae_idr_display = fmt_idr_full(mae_val) if mae_val is not None else ""
        rmse_idr_display = fmt_idr_full(rmse_val) if rmse_val is not None else ""

        c1, c2, c3 = st.columns(3)

        with c1:
            with st.container(border=True):
                st.caption("MAE NORMALIZED")
                st.markdown(f"### {mae_norm_display}")
                st.caption(mae_idr_display)

        with c2:
            with st.container(border=True):
                st.caption("RMSE NORMALIZED")
                st.markdown(f"### {rmse_norm_display}")
                st.caption(rmse_idr_display)

        with c3:
            with st.container(border=True):
                st.caption("R2 SCORE")
                st.markdown(f"### {r2_display}")
                st.caption("Regression fit")

        c4, c5 = st.columns(2)

        with c4:
            with st.container(border=True):
                st.caption("DIRECTION ACCURACY")
                st.markdown(f"### {acc_display}")
                st.caption("Trend classification")

        with c5:
            with st.container(border=True):
                st.caption("MACRO F1")
                st.markdown(f"### {f1_display}")
                st.caption("Class balance score")

    else:
        no_data("Metrik final belum tersedia. Pastikan fingo_deploy.pkl terbaru sudah disalin ke streamlit/models/.")
        
    tolerance_html = f"Tolerance accuracy &lt;5% = {tol_5:.2f}%." if tol_5 is not None else ""

    st.html(f"""
    <div class="rq-card">
      <div class="rq-num">Research Question 4</div>
      <div class="rq-q">Seberapa akurat model final Income Predictor?</div>
      <div class="rq-a">
        Model final menunjukkan
        <span class="rq-highlight">MAE normalized {f"{mae_norm_val:.4f}" if mae_norm_val is not None else "N/A"}</span>
        ({fmt_idr_full(mae_val) if mae_val is not None else "N/A"}),
        <span class="rq-highlight">RMSE normalized {f"{rmse_norm_val:.4f}" if rmse_norm_val is not None else "N/A"}</span>
        ({fmt_idr_full(rmse_val) if rmse_val is not None else "N/A"}),
        <span class="rq-highlight">R2 {f"{r2_val:.4f}" if r2_val is not None else "N/A"}</span>,
        <span class="rq-highlight">Direction Accuracy {f"{acc_val * 100:.2f}%" if acc_val is not None else "N/A"}</span>,
        dan <span class="rq-highlight">Macro F1 {f"{f1_val:.4f}" if f1_val is not None else "N/A"}</span>.
        {tolerance_html}
      </div>
    </div>
    """)

    # RQ5
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">RQ5 - Fitur Terpenting Klasifikasi Impulsif</div>', unsafe_allow_html=True)
    if clf_imp is not None:
        try:
            fn   = clf_imp.named_steps["preprocessor"].get_feature_names_out()
            imps = clf_imp.named_steps["classifier"].feature_importances_
            imp_df = pd.DataFrame({"feature":fn,"importance":imps})
            def _orig(f):
                if "__" in f:
                    _,rest = f.split("__",1)
                    for kc in IMP_MODEL_FEATURES:
                        if rest==kc or rest.startswith(kc+"_"): return kc
                    return rest
                return f
            imp_df["original"] = imp_df["feature"].apply(_orig)
            agg = imp_df.groupby("original")["importance"].sum().sort_values(ascending=False).head(10)

            col_l2,col_r2 = st.columns(2, gap="large")
            with col_l2:
                fig,ax = plt.subplots(figsize=(7,5))
                clrs = [FG if i==0 else FG_BLUE if i<3 else FG_MUTED for i in range(len(agg))]
                ax.barh(agg.index[::-1], agg.values[::-1]*100, color=clrs[::-1], height=0.6, alpha=0.9)
                for bar,v in zip(ax.patches, agg.values[::-1]):
                    ax.text(v*100+0.3, bar.get_y()+bar.get_height()/2,
                        f"{v*100:.1f}%", va="center", fontsize=9, color="#FFFFFF", fontweight="bold")
                ax.set_title("Top 10 Feature Importance - Impulsive Classifier", color="#FFFFFF")
                ax.set_xlabel("Importance (%)")
                plt.tight_layout(pad=0.8); st.pyplot(fig, use_container_width=True); plt.close()
            with col_r2:
                t1,t2,t3 = agg.index[0],agg.index[1],agg.index[2]
                p1,p2,p3 = agg.values[0]*100,agg.values[1]*100,agg.values[2]*100
                st.markdown(f"""
                <div class="rq-card">
                    <div class="rq-num">Research Question 5</div>
                    <div class="rq-q">Fitur apa yang paling berpengaruh dalam klasifikasi transaksi impulsif?</div>
                    <div class="rq-a">
                        Berdasarkan RandomForestClassifier (fingo_label_classifier.joblib):<br><br>
                        1. <span class="rq-highlight">{t1}</span> ({p1:.1f}%)<br>
                        2. <span class="rq-highlight">{t2}</span> ({p2:.1f}%)<br>
                        3. <span class="rq-highlight">{t3}</span> ({p3:.1f}%)<br><br>
                        Fitur berbasis sinyal impulsif mendominasi karena merangkum faktor waktu, kategori, dan nominal.
                    </div>
                </div>""", unsafe_allow_html=True)
        except Exception as e:
            no_data(f"Gagal memuat feature importance: {e}")
    else:
        no_data("Model Impulsive Detector tidak ditemukan di streamlit/models/")

# ══════════════════════════════════════════════════════════════════════════════
# MODULE 2 - INCOME PREDICTOR
# ══════════════════════════════════════════════════════════════════════════════
elif module == "Income Predictor":
    tabs = st.tabs(["Overview Pipeline","EDA & Dataset","Evaluasi Model","Visualisasi",
                    "Coba Prediksi","A/B Testing","Fingo Assistant"])

    with tabs[0]:
        st.markdown("""
        <div class="page-header">
            <h1>Income Predictor</h1>
            <p>Sistem prediksi pendapatan mingguan berbasis AI untuk gig worker Indonesia</p>
        </div>""", unsafe_allow_html=True)
        df_sy = load_synthetic(); df_s = load_survey()
        n_resp  = len(df_s) if df_s is not None else 0
        n_users = df_sy["synthetic_user_id"].nunique() if df_sy is not None and "synthetic_user_id" in df_sy.columns else 0
        n_rows  = len(df_sy) if df_sy is not None else 0
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Responden Survey", f"{n_resp:,}")
        c2.metric("Synthetic Users",  f"{n_users:,}")
        c3.metric("Total Data Rows",  f"{n_rows:,}")
        c4.metric("Minggu per User",  "52")
        st.markdown("<hr>", unsafe_allow_html=True)
        col_l,col_r = st.columns(2, gap="large")
        with col_l:
            st.markdown("""
            <div class="panel">
                <h3>Apa itu Income Predictor?</h3>
                Memperkirakan pendapatan <strong style="color:#E8EDE9">4 minggu ke depan</strong>
                berdasarkan fitur pendapatan <strong style="color:#E8EDE9">4 minggu terakhir</strong>.
                Output digunakan sebagai dasar Budget Planner 50/30/20.<br><br>
                <strong style="color:var(--fg-warn)">Model Final:</strong> Ens(DL=0.15 + GradientBoosting) untuk regresi pendapatan
                dan Ens_cls(DL=0.50) untuk klasifikasi arah tren, disimpan dalam <code>fingo_deploy.pkl</code>
                dan digunakan melalui API <code>https://mes1205-fingo.hf.space/predict/income</code>.<br><br>
                <strong style="color:var(--fg-warn)">Catatan:</strong>
                Project Plan awal menggunakan LSTM TensorFlow. Implementasi final menggunakan ensemble
                Deep Learning + GradientBoosting karena memberikan performa test set terbaik dan lebih stabil
                untuk dataset tabular time-series.
            </div>""", unsafe_allow_html=True)
        with col_r:
            st.markdown('<div class="section-header">Pipeline Data Science (10 Notebook)</div>', unsafe_allow_html=True)
            for num,name,out in [
                ("01","Data Preparation","survey_clean.csv"),
                ("02","Temporal Mapping","survey_temporal_mapped.csv"),
                ("03","EDA Survey","charts + reports"),
                ("04","Synthetic Data 52w","3.000 users x 52 minggu"),
                ("05","Feature Engineering","feature_columns.json"),
                ("06","Model Dataset Split","train/val/test + scalers"),
                ("07","Bias Validation","bias_validation_report.md"),
                ("08","Dokumentasi","data_dictionary.csv"),
                ("09","Model Training","GradientBoosting + metrics"),
                ("10","A/B Testing","ab_testing_report.md"),
            ]:
                st.markdown(f"""
                <div style="display:flex;gap:14px;padding:10px 0;border-bottom:1px solid var(--border);align-items:flex-start;">
                    <div style="flex-shrink:0;width:28px;height:28px;background:var(--border);border-radius:6px;
                        display:flex;align-items:center;justify-content:center;font-size:.72rem;font-weight:700;color:{FG}">{num}</div>
                    <div>
                        <div style="font-size:.88rem;font-weight:600;color:var(--text)">{name}</div>
                        <div style="font-size:.78rem;color:var(--fg-muted);margin-top:2px;font-family:monospace">{out}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("""
        <div class="page-header">
            <h1>EDA & Dataset Income Predictor</h1>
            <p>Ringkasan eksplorasi dari notebook 01-07: survey, temporal mapping, synthetic data, feature engineering, dan bias validation</p>
        </div>""", unsafe_allow_html=True)

        df_s = load_survey()
        df_w = load_survey_weekly_long()
        df_sy = load_synthetic()
        df_feat = load_income_features()
        meta = load_training_metadata()

        n_resp = len(df_s) if df_s is not None else 0
        n_weekly = len(df_w) if df_w is not None else 0
        n_synth_users = df_sy["synthetic_user_id"].nunique() if df_sy is not None and "synthetic_user_id" in df_sy.columns else 0
        n_feature_rows = len(df_feat) if df_feat is not None else 0

        mean_weekly = df_w["weekly_income"].mean() if df_w is not None and "weekly_income" in df_w.columns else None
        median_weekly = df_w["weekly_income"].median() if df_w is not None and "weekly_income" in df_w.columns else None
        avg_cv = df_s["income_cv_4w"].mean() if df_s is not None and "income_cv_4w" in df_s.columns else None
        top_gig = (
            df_s["gig_type"].value_counts().idxmax()
            if df_s is not None and "gig_type" in df_s.columns and len(df_s) > 0 else None
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Survey Respondents", f"{n_resp:,}")
        c2.metric("Weekly Survey Rows", f"{n_weekly:,}")
        c3.metric("Synthetic Users", f"{n_synth_users:,}")
        c4.metric("Feature Rows", f"{n_feature_rows:,}")

        c5, c6, c7, c8 = st.columns(4)
        c5.metric("Mean Weekly Income", fmt_idr_full(mean_weekly))
        c6.metric("Median Weekly Income", fmt_idr_full(median_weekly))
        c7.metric("Avg Income CV 4w", f"{avg_cv:.3f}" if avg_cv is not None else "N/A")
        c8.metric("Top Gig Type", GIG_LABELS.get(top_gig, top_gig) if top_gig else "N/A")

        st.markdown("""
        <div class="panel">
            <h3>Inti Temuan EDA</h3>
            <p>
            Survey real digunakan sebagai anchor distribusi pendapatan, lalu dipetakan ke kalender agar
            pola mingguan, week-of-month, dan seasonal signal bisa terbaca. Dataset sintetis 52 minggu
            dibangun dari distribusi survey dengan AR(1), shock/noise per gig type, serta event seperti
            payday, Ramadan/Lebaran, Harbolnas, dan akhir tahun. Fitur model kemudian dibentuk dengan
            sliding window 4 minggu sehingga target minggu depan tidak bocor ke input model.
            </p>
        </div>""", unsafe_allow_html=True)

        eda_tabs = st.tabs(["Survey EDA", "Temporal Mapping", "Synthetic & Bias", "Feature Engineering"])

        with eda_tabs[0]:
            st.markdown('<div class="section-header">Distribusi Survey</div>', unsafe_allow_html=True)

            chart_cols = st.columns(2, gap="large")
            for idx, (fn, cap) in enumerate([
                ("gig_type_distribution.png", "Distribusi responden per gig type"),
                ("income_by_gig_type.png", "Distribusi pendapatan mingguan per gig type"),
                ("weekly_income_trend_w4_to_w1.png", "Tren income survey dari W4 ke W1"),
                ("eda_income_rw_by_gig.png", "Relative week income per gig type"),
            ]):
                p = OUTPUTS_DIR / "charts" / fn
                if p.exists():
                    with chart_cols[idx % 2]:
                        st.image(str(p), caption=cap, use_container_width=True)

            if df_w is not None and "weekly_income" in df_w.columns:
                st.markdown('<div class="section-header">Ringkasan Relative Week</div>', unsafe_allow_html=True)
                rel = (
                    df_w.groupby("income_col")["weekly_income"]
                    .agg(["count", "mean", "median", "std"])
                    .reset_index()
                )
                rel["Urutan"] = rel["income_col"].map({
                    "income_w1": "W1 - terbaru",
                    "income_w2": "W2",
                    "income_w3": "W3",
                    "income_w4": "W4 - terlama",
                }).fillna(rel["income_col"])
                for c in ["mean", "median", "std"]:
                    rel[c] = rel[c].apply(fmt_idr_full)
                st.dataframe(
                    rel[["Urutan", "count", "mean", "median", "std"]],
                    use_container_width=True,
                    hide_index=True,
                )

            summary_path = INCOME_REPORTS_DIR / "survey_eda_summary.md"
            if summary_path.exists():
                with st.expander("Baca ringkasan EDA survey dari notebook 03"):
                    with open(summary_path, encoding="utf-8") as f:
                        st.markdown(f.read())

        with eda_tabs[1]:
            st.markdown('<div class="section-header">Temporal Mapping</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="panel">
                <p>
                Notebook 02 mengubah income_w1 sampai income_w4 menjadi periode kalender:
                <strong style="color:#E8EDE9">income_w1</strong> adalah H-7 sampai H-1 dari timestamp responden,
                sedangkan <strong style="color:#E8EDE9">income_w4</strong> adalah periode terlama.
                Mapping ini dipakai untuk membaca month, week_of_month, ISO week, dan pola seasonal.
                </p>
            </div>""", unsafe_allow_html=True)

            chart_cols = st.columns(2, gap="large")
            for idx, (fn, cap) in enumerate([
                ("temporal_mapping_overview.png", "Overview temporal mapping"),
                ("eda_calendar_month_wom.png", "Income by calendar month dan week of month"),
                ("eda_calendar_month_wom_relative_week.png", "Calendar pattern by relative week"),
            ]):
                p = OUTPUTS_DIR / "charts" / fn
                if p.exists():
                    with chart_cols[idx % 2]:
                        st.image(str(p), caption=cap, use_container_width=True)

            if df_w is not None and {"calendar_month", "week_of_month", "weekly_income"}.issubset(df_w.columns):
                st.markdown('<div class="section-header">Mean Income by Month & Week of Month</div>', unsafe_allow_html=True)
                wom = (
                    df_w.groupby(["calendar_month", "week_of_month"])["weekly_income"]
                    .agg(["count", "mean", "median"])
                    .reset_index()
                    .sort_values(["calendar_month", "week_of_month"])
                )
                wom["mean"] = wom["mean"].apply(fmt_idr_full)
                wom["median"] = wom["median"].apply(fmt_idr_full)
                st.dataframe(wom, use_container_width=True, hide_index=True)

        with eda_tabs[2]:
            st.markdown('<div class="section-header">Synthetic Data Generation & Bias Validation</div>', unsafe_allow_html=True)
            s1, s2, s3, s4 = st.columns(4)
            synth_rows = len(df_sy) if df_sy is not None else 0
            synth_mean = df_sy["synthetic_weekly_income"].mean() if df_sy is not None and "synthetic_weekly_income" in df_sy.columns else None
            synth_min = df_sy["synthetic_weekly_income"].min() if df_sy is not None and "synthetic_weekly_income" in df_sy.columns else None
            synth_max = df_sy["synthetic_weekly_income"].max() if df_sy is not None and "synthetic_weekly_income" in df_sy.columns else None
            s1.metric("Synthetic Rows", f"{synth_rows:,}")
            s2.metric("Mean Synthetic Income", fmt_idr_full(synth_mean))
            s3.metric("Min Synthetic Income", fmt_idr_full(synth_min))
            s4.metric("Max Synthetic Income", fmt_idr_full(synth_max))

            p = OUTPUTS_DIR / "charts" / "bias_validation_charts.png"
            if p.exists():
                st.image(str(p), caption="Bias validation charts", use_container_width=True)

            col_l, col_r = st.columns(2, gap="large")
            with col_l:
                st.markdown('<div class="section-header">Synthetic vs Survey per Gig Type</div>', unsafe_allow_html=True)
                vp = INCOME_REPORTS_DIR / "gig_type_income_validation.csv"
                if vp.exists():
                    val = pd.read_csv(vp)
                    for c in ["real_median_weekly", "synthetic_median_weekly"]:
                        if c in val.columns:
                            val[c] = val[c].apply(fmt_idr_full)
                    if "pct_diff" in val.columns:
                        val["pct_diff"] = val["pct_diff"].apply(lambda v: f"{v:.2f}%")
                    st.dataframe(val, use_container_width=True, hide_index=True)
                else:
                    no_data("gig_type_income_validation.csv belum tersedia.")

            with col_r:
                st.markdown('<div class="section-header">BPS Range Validation</div>', unsafe_allow_html=True)
                bp = INCOME_REPORTS_DIR / "bps_range_validation.csv"
                if bp.exists():
                    bps = pd.read_csv(bp)
                    for c in ["synthetic_mean", "bps_weekly"]:
                        if c in bps.columns:
                            bps[c] = bps[c].apply(fmt_idr_full)
                    if "ratio" in bps.columns:
                        bps["ratio"] = bps["ratio"].apply(lambda v: f"{v:.2f}x")
                    st.dataframe(bps, use_container_width=True, hide_index=True)
                else:
                    no_data("bps_range_validation.csv belum tersedia.")

            rp = INCOME_REPORTS_DIR / "bias_validation_report.md"
            if rp.exists():
                with st.expander("Baca bias validation report dari notebook 07"):
                    with open(rp, encoding="utf-8") as f:
                        st.markdown(f.read())

        with eda_tabs[3]:
            st.markdown('<div class="section-header">Feature Engineering & Split Contract</div>', unsafe_allow_html=True)
            if meta is not None:
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Feature Count", f"{meta.get('feature_count', 0):,}")
                m2.metric("Train Rows", f"{meta.get('train_rows', 0):,}")
                m3.metric("Val Rows", f"{meta.get('val_rows', 0):,}")
                m4.metric("Test Rows", f"{meta.get('test_rows', 0):,}")
                st.caption(
                    f"Split strategy: {meta.get('split_strategy', 'N/A')} | "
                    f"Anti-leakage check: {meta.get('anti_leakage_check', 'N/A')}"
                )

            if df_feat is not None:
                col_l, col_r = st.columns(2, gap="large")
                with col_l:
                    if "next_week_direction" in df_feat.columns:
                        st.markdown('<div class="section-header">Target Direction Distribution</div>', unsafe_allow_html=True)
                        target_dist = (
                            df_feat["next_week_direction"]
                            .value_counts(normalize=False)
                            .rename_axis("direction")
                            .reset_index(name="count")
                        )
                        target_dist["share"] = (target_dist["count"] / target_dist["count"].sum() * 100).apply(lambda v: f"{v:.2f}%")
                        st.dataframe(target_dist, use_container_width=True, hide_index=True)

                with col_r:
                    if "seasonal_event_type" in df_feat.columns:
                        st.markdown('<div class="section-header">Seasonal Event Coverage</div>', unsafe_allow_html=True)
                        events = (
                            df_feat["seasonal_event_type"]
                            .fillna("normal")
                            .value_counts()
                            .rename_axis("event")
                            .reset_index(name="count")
                        )
                        events["share"] = (events["count"] / events["count"].sum() * 100).apply(lambda v: f"{v:.2f}%")
                        st.dataframe(events, use_container_width=True, hide_index=True)

                st.markdown('<div class="section-header">Contoh Feature Row</div>', unsafe_allow_html=True)
                preview_cols = [
                    "synthetic_user_id", "target_week_index", "next_week_income", "next_week_direction",
                    "lag_1_income", "lag_2_income", "lag_3_income", "lag_4_income",
                    "rolling_mean_4w", "income_growth_1w", "income_volatility",
                    "target_month", "target_week_of_month", "seasonal_event_type", "gig_type",
                ]
                preview_cols = [c for c in preview_cols if c in df_feat.columns]
                st.dataframe(df_feat[preview_cols].head(20), use_container_width=True, hide_index=True)
            else:
                no_data("income_features.csv belum tersedia di data/processed/.")

    with tabs[2]:
        st.markdown("""
        <div class="page-header">
            <h1>Evaluasi Model</h1>
            <p>Performa model Income Predictor pada test set</p>
        </div>""", unsafe_allow_html=True)
        
        bundle = load_income_bundle()
        df_pred2 = load_predictions_test()
        n_tr = len(df_pred2) if df_pred2 is not None else 0

        mae_t = None
        rmse_t = None
        r2_t = None
        acc_t = None
        f1_t = None
        tol_2 = None
        tol_5 = None
        tol_10 = None

        if bundle is not None:
            st.markdown(
                '<div class="section-header">Model Bundle Info (fingo_deploy.pkl)</div>',
                unsafe_allow_html=True
            )

            regressor_name = bundle.get("final_reg_name", "N/A")
            classifier_name = bundle.get("final_cls_name", "N/A")
            income_min = bundle.get("income_min", None)
            income_max = bundle.get("income_max", None)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    f"""
                    <div class="model-info-card">
                        <div class="model-info-label">Regressor</div>
                        <div class="model-info-value">{regressor_name}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    f"""
                    <div class="model-info-card">
                        <div class="model-info-label">Classifier</div>
                        <div class="model-info-value">{classifier_name}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown(
                '<div class="section-header">Model Training Range dari PKL</div>',
                unsafe_allow_html=True
            )

            r1, r2 = st.columns(2)
            r1.metric(
                "Income Minimum",
                fmt_idr_full(float(income_min)) if income_min is not None else "N/A"
            )
            r2.metric(
                "Income Maximum",
                fmt_idr_full(float(income_max)) if income_max is not None else "N/A"
            )

            # Prioritas utama: actual metrics dari fingo_deploy.pkl terbaru
            mae_t = bundle.get("final_reg_test_mae_idr")
            rmse_t = bundle.get("final_reg_test_rmse_idr")
            r2_t = bundle.get("final_reg_test_r2")
            acc_t = bundle.get("final_cls_test_accuracy")
            f1_t = bundle.get("final_cls_test_macro_f1")
            tol_2 = bundle.get("tolerance_acc_2pct")
            tol_5 = bundle.get("tolerance_acc_5pct")
            tol_10 = bundle.get("tolerance_acc_10pct")

        # Fallback kalau PKL belum punya actual metrics
        if mae_t is None and df_pred2 is not None and len(df_pred2) > 0:
            if "absolute_error" in df_pred2.columns:
                mae_t = df_pred2["absolute_error"].mean()

            if "direction_correct" in df_pred2.columns:
                acc_t = df_pred2["direction_correct"].mean()

            if "next_week_income" in df_pred2.columns and "predicted_next_week_income" in df_pred2.columns:
                resid = df_pred2["next_week_income"] - df_pred2["predicted_next_week_income"]
                rmse_t = float(np.sqrt((resid ** 2).mean()))

                ss_res = (resid ** 2).sum()
                ss_tot = ((df_pred2["next_week_income"] - df_pred2["next_week_income"].mean()) ** 2).sum()
                r2_t = 1 - ss_res / ss_tot if ss_tot > 0 else None

        if mae_t is not None:
            mae_norm_t = bundle.get("final_reg_test_mae_norm") if bundle is not None else None
            rmse_norm_t = bundle.get("final_reg_test_rmse_norm") if bundle is not None else None
            target_mae = bundle.get("target_mae", 0.02) if bundle is not None else 0.02
            mae_gap = mae_norm_t - target_mae if mae_norm_t is not None else None

            st.markdown(
                '<div class="section-header">Final Model Deployment - Test Set</div>',
                unsafe_allow_html=True
            )

            st.markdown("""
            <div class="panel">
                <p>
                Metrik berikut diambil dari <strong style="color:#E8EDE9">fingo_deploy.pkl</strong>,
                yaitu model final yang digunakan untuk deployment/API. Validation set digunakan untuk memilih kandidat model,
                sedangkan test set hanya digunakan untuk evaluasi akhir.
                </p>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric(
                "MAE Normalized",
                f"{mae_norm_t:.4f}" if mae_norm_t is not None else "N/A",
                delta=f"gap {mae_gap:+.4f} dari target 0.0200" if mae_gap is not None else None
            )
            c2.metric(
                "RMSE Normalized",
                f"{rmse_norm_t:.4f}" if rmse_norm_t is not None else "N/A"
            )
            c3.metric("R² Score", f"{r2_t:.4f}" if r2_t is not None else "N/A")
            c4.metric("MAE Rupiah", fmt_idr_full(mae_t))

            c5, c6, c7 = st.columns(3)
            c5.metric("Tolerance <2%", f"{tol_2:.1f}%" if tol_2 is not None else "N/A")
            c6.metric("Tolerance <5%", f"{tol_5:.1f}%" if tol_5 is not None else "N/A")
            c7.metric("Tolerance <10%", f"{tol_10:.1f}%" if tol_10 is not None else "N/A")

            st.markdown(
                '<div class="section-header">Final Direction Classification - Test Set</div>',
                unsafe_allow_html=True
            )

            k1, k2 = st.columns(2)
            k1.metric(
                "Accuracy",
                f"{acc_t * 100:.2f}%" if acc_t is not None else "N/A",
                delta="below target" if acc_t is not None and acc_t < 0.85 else "target achieved"
            )
            k2.metric("Macro F1", f"{f1_t:.4f}" if f1_t is not None else "N/A")

            st.warning(
                "Regression model hampir mencapai target MAE normalized ≤ 0.02 dengan gap kecil. "
                "Namun, classification direction masih below target karena accuracy test 79.09% dan Macro F1 0.6105."
            )
        df_reg_m = load_regression_metrics()
        df_cls_m = load_classification_metrics()
        if df_reg_m is not None:
           st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            '<div class="section-header">Final Model Comparison - AI Engineer Evaluation</div>',
            unsafe_allow_html=True
        )

        model_comparison = pd.DataFrame([
            {"Model": "LinearRegression", "Val MAE": 0.0490, "Test MAE": 0.0475},
            {"Model": "Ridge", "Val MAE": 0.0490, "Test MAE": 0.0475},
            {"Model": "LightGBM", "Val MAE": 0.0230, "Test MAE": 0.0230},
            {"Model": "GradientBoosting", "Val MAE": 0.0214, "Test MAE": 0.0214},
            {"Model": "XGBoost", "Val MAE": 0.0229, "Test MAE": 0.0230},
            {"Model": "RandomForest", "Val MAE": 0.0235, "Test MAE": 0.0235},
            {"Model": "DL", "Val MAE": 0.0236, "Test MAE": 0.0237},
            {"Model": "Ens(DL=0.15+GradientBoosting) - FINAL", "Val MAE": 0.0213, "Test MAE": 0.0214},
        ])

        st.dataframe(
            model_comparison,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Val MAE digunakan untuk membandingkan kandidat model. "
            "Test MAE digunakan untuk evaluasi akhir. Model final dipilih berdasarkan performa terbaik dan stabilitas deployment."
        )
        if df_cls_m is not None:
            st.markdown(
                '<div class="section-header">Classification Report - Test Set</div>',
                unsafe_allow_html=True
            )

            classification_report_df = pd.DataFrame([
                {"Class": "Down", "Precision": 0.67, "Recall": 0.21, "F1-score": 0.32, "Support": 2558},
                {"Class": "Stable", "Precision": 0.80, "Recall": 0.95, "F1-score": 0.87, "Support": 15006},
                {"Class": "Up", "Precision": 0.77, "Recall": 0.55, "F1-score": 0.64, "Support": 4036},
                {"Class": "Macro Avg", "Precision": 0.75, "Recall": 0.57, "F1-score": 0.61, "Support": 21600},
                {"Class": "Weighted Avg", "Precision": 0.78, "Recall": 0.79, "F1-score": 0.76, "Support": 21600},
            ])

            st.dataframe(
                classification_report_df,
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "Kelas Stable mendominasi performa model, sementara kelas Down masih memiliki recall rendah. "
                "Ini menjelaskan mengapa accuracy cukup tinggi tetapi Macro F1 masih 0.6105."
            )

    with tabs[3]:
        st.markdown("""
        <div class="page-header">
            <h1>Visualisasi</h1>
            <p>Chart final dari hasil evaluasi model Income Predictor terbaru</p>
        </div>""", unsafe_allow_html=True)

        # st.markdown(
        #     """
        #     <div class="panel">
        #         <p>
        #             Visualisasi pada halaman ini membaca file PNG final dari folder
        #             <strong style="color:#E8EDE9">outputs/charts</strong>.
        #             Pastikan chart sudah diekspor ulang dari notebook terbaru agar hasilnya konsisten
        #             dengan <strong style="color:#E8EDE9">fingo_deploy.pkl</strong>.
        #         </p>
        #     </div>
        #     """,
        #     unsafe_allow_html=True
        # )

        chart_items = [
            (
                "income_final_evaluation_dashboard.png",
                "Final Evaluation Dashboard"
            ),
            (
                "income_actual_vs_predicted.png",
                "Actual vs Predicted Income"
            ),
            (
                "income_error_distribution.png",
                "Income Prediction Error Distribution"
            ),
            (
                "income_normalized_error_distribution.png",
                "Normalized Error Distribution"
            ),
            (
                "income_regression_model_comparison.png",
                "Regression Model Comparison"
            ),
            (
                "income_classification_model_comparison.png",
                "Classification Model Comparison"
            ),
            (
                "income_direction_confusion_matrix.png",
                "Direction Classification Confusion Matrix"
            ),
            (
                "income_tolerance_accuracy.png",
                "Tolerance Accuracy"
            ),
            (
                "income_error_by_direction.png",
                "Prediction Error by Direction"
            ),
            (
                "income_prediction_timeline_sample.png",
                "Actual vs Predicted Timeline Sample"
            ),
        ]

        found_charts = []

        for filename, caption in chart_items:
            chart_path = INCOME_CHARTS_DIR / filename

            if chart_path.exists():
                found_charts.append(filename)

                st.markdown(
                    f'<div class="section-header">{caption}</div>',
                    unsafe_allow_html=True
                )

                st.image(
                    str(chart_path),
                    caption=caption,
                    use_container_width=True
                )

        if not found_charts:
            no_data(
                "Belum ada chart final di outputs/charts. "
                "Jalankan cell export PNG di notebook terbaru, lalu pastikan file PNG masuk ke folder outputs/charts."
            )
        else:
            with st.expander("Daftar chart yang berhasil dimuat"):
                for fn in found_charts:
                    st.write(fn)

    with tabs[4]:
        st.markdown("""
        <div class="page-header">
            <h1>Coba Prediksi Pendapatan</h1>
            <p>Masukkan riwayat pendapatan 4 minggu terakhir untuk mendapatkan estimasi 4 minggu ke depan</p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="panel" style="margin-bottom:1.5rem">
            <p>
            Model memerlukan riwayat <strong style="color:#E8EDE9">4 minggu terakhir</strong>.
            W1 = 4 minggu lalu, W4 = minggu terakhir. Output berupa estimasi pendapatan
            minggu depan dan proyeksi 4 minggu ke depan.
            </p>
        </div>""", unsafe_allow_html=True)

        with st.form("pred_income_form"):
            st.markdown("**Pendapatan 4 minggu terakhir (Rupiah)**")

            r1c1, r1c2, r1c3, r1c4 = st.columns(4)

            w1 = r1c1.number_input(
                "W1 (4 minggu lalu)",
                min_value=0,
                max_value=50_000_000,
                value=830_000,
                step=50_000
            )

            w2 = r1c2.number_input(
                "W2 (3 minggu lalu)",
                min_value=0,
                max_value=50_000_000,
                value=760_000,
                step=50_000
            )

            w3 = r1c3.number_input(
                "W3 (2 minggu lalu)",
                min_value=0,
                max_value=50_000_000,
                value=800_000,
                step=50_000
            )

            w4 = r1c4.number_input(
                "W4 (minggu terakhir)",
                min_value=0,
                max_value=50_000_000,
                value=810_000,
                step=50_000
            )

            st.markdown(
                "<div style='margin-top:.8rem'><strong>Konteks Pekerjaan</strong></div>",
                unsafe_allow_html=True
            )

            ctx1, ctx2, ctx3 = st.columns(3)

            gig_in = ctx1.selectbox(
                "Jenis Pekerjaan",
                GIG_TYPES,
                format_func=lambda x: GIG_LABELS.get(x, x)
            )

            usia_in = ctx2.number_input(
                "Usia",
                min_value=15,
                max_value=60,
                value=25,
                step=1
            )

            hari_in = ctx3.number_input(
                "Hari kerja / minggu",
                min_value=1,
                max_value=7,
                value=5,
                step=1
            )

            jam_in = st.number_input(
                "Jam kerja / hari",
                min_value=1,
                max_value=24,
                value=8,
                step=1
            )

            submitted = st.form_submit_button(
                "Hitung Prediksi",
                type="primary",
                use_container_width=True
            )

        if submitted:
            income_history = [w1, w2, w3, w4]
            h_arr = np.array(income_history, dtype=float)
            avg_last4 = float(np.mean(h_arr))

            with st.spinner("Menghubungi API..."):
                api_result, api_error = call_income_api(
                    income_history_4w=income_history,
                    usia=usia_in,
                    hari_kerja=hari_in,
                    jam_kerja=jam_in,
                    gig_type=gig_in
                )

            if api_result is not None:
                pred_next = float(api_result.get("prediction_next_week", avg_last4))
                pred_4w = api_result.get("prediction_4_weeks_ahead", [pred_next] * 4)
                total_proj = float(api_result.get("total_projected_income", sum(pred_4w)))
                dir_pred = api_result.get("income_direction", "Stable")
                dir_proba = api_result.get("direction_proba", {})
                avg_4w_api = float(api_result.get("avg_income_last_4w", avg_last4))
                src_lbl = "API - mes1205-fingo.hf.space"
            else:
                st.warning(f"API tidak tersedia: {api_error}. Mencoba model lokal...")
                pred_next, dir_pred = predict_income_local(
                    income_history,
                    gig_in,
                    usia_in,
                    hari_in,
                    jam_in,
                    5,
                    2
                )

                if pred_next is None:
                    pred_next = avg_last4
                    dir_pred = "Stable"
                    st.info("Model lokal tidak tersedia. Menggunakan rata-rata 4 minggu.")

                pred_4w = [pred_next] * 4
                total_proj = pred_next * 4
                dir_proba = {}
                avg_4w_api = avg_last4
                src_lbl = "Local model - fingo_deploy.pkl"

            delta = pred_next - avg_4w_api
            dir_label = {
                "Up": "Naik",
                "Stable": "Stabil",
                "Down": "Turun"
            }.get(dir_pred, "Stabil")

            badge_dir = (
                "badge-green" if dir_pred == "Up"
                else "badge-red" if dir_pred == "Down"
                else "badge-yellow"
            )

            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">Estimasi Pendapatan Minggu Depan ({src_lbl})</div>
                <div class="result-value">{fmt_idr_full(pred_next)}</div>
                <div class="result-sub">
                    {'+' if delta >= 0 else ''}{fmt_idr(delta)} vs rata-rata 4 minggu terakhir
                    &nbsp;&nbsp;<span class="badge {badge_dir}">Tren: {dir_label}</span>
                </div>
            </div>""", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            c1.metric("Rata-rata 4 Minggu Terakhir", fmt_idr_full(avg_4w_api))
            c2.metric("Total Proyeksi 4 Minggu", fmt_idr_full(total_proj))
            c3.metric("Arah Tren", dir_label)

            if dir_proba:
                st.markdown(
                    '<div class="section-header">Probabilitas Arah Tren</div>',
                    unsafe_allow_html=True
                )

                for dk, dcolor in [("Up", FG), ("Stable", FG_WARN), ("Down", FG_RED)]:
                    pv = float(dir_proba.get(dk, 0.0))
                    st.markdown(f"""
                    <div class="budget-bar-wrap">
                        <div class="budget-bar-label">
                            <span style="color:{dcolor};font-weight:600">{dk}</span>
                            <span>{pv * 100:.1f}%</span>
                        </div>
                        <div class="budget-bar-track">
                            <div class="budget-bar-fill" style="width:{pv * 100:.1f}%;background:{dcolor}"></div>
                        </div>
                    </div>""", unsafe_allow_html=True)

            st.markdown(
                '<div class="section-header">Histori 4 Minggu + Proyeksi 4 Minggu</div>',
                unsafe_allow_html=True
            )

            fig, ax = plt.subplots(figsize=(12, 4.5))

            ax.plot(
                range(1, 5),
                [v / 1000 for v in income_history],
                "o-",
                color=FG_BLUE,
                linewidth=2.2,
                markersize=6,
                label="Histori 4 Minggu"
            )

            ax.plot(
                [4] + list(range(5, 9)),
                [income_history[-1] / 1000] + [v / 1000 for v in pred_4w],
                "o--",
                color=FG,
                linewidth=2.2,
                markersize=7,
                label="Proyeksi 4 Minggu",
                zorder=5
            )

            ax.axvline(
                4.5,
                color=FG_MUTED,
                linestyle=":",
                linewidth=1,
                alpha=0.6
            )

            ax.axhline(
                avg_4w_api / 1000,
                color=FG_WARN,
                linestyle=":",
                alpha=0.6,
                label=f"Rata-rata 4w: {fmt_idr(avg_4w_api)}"
            )

            ax.set_title(
                f"Tren Pendapatan - {GIG_LABELS.get(gig_in, gig_in)}",
                color="#FFFFFF"
            )

            ax.set_xlabel("Minggu")
            ax.set_ylabel("Pendapatan (ribu Rp)")
            ax.set_xticks(range(1, 9))
            ax.set_xticklabels(
                ["W1", "W2", "W3", "W4", "W+1", "W+2", "W+3", "W+4"],
                rotation=45,
                ha="right",
                fontsize=8
            )

            ax.legend(fontsize=8)
            plt.tight_layout(pad=0.8)
            st.pyplot(fig, use_container_width=True)
            plt.close()

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(
                '<div class="section-header">Saran Anggaran 50/30/20 - Berdasarkan Prediksi Minggu Depan</div>',
                unsafe_allow_html=True
            )

            keb = pred_next * 0.50
            tab = pred_next * 0.30
            lain = pred_next * 0.20

            bc1, bc2, bc3 = st.columns(3)
            bc1.metric("Kebutuhan Pokok (50%)", fmt_idr_full(keb))
            bc2.metric("Tabungan / Investasi (30%)", fmt_idr_full(tab))
            bc3.metric("Pengeluaran Lain (20%)", fmt_idr_full(lain))

            for lbl, amt, pct, col in [
                ("Kebutuhan Pokok", keb, 50, FG),
                ("Tabungan / Investasi", tab, 30, FG_BLUE),
                ("Pengeluaran Lain", lain, 20, FG_WARN)
            ]:
                st.markdown(f"""
                <div class="budget-bar-wrap">
                    <div class="budget-bar-label">
                        <span>{lbl}</span>
                        <span>{fmt_idr_full(amt)} ({pct}%)</span>
                    </div>
                    <div class="budget-bar-track">
                        <div class="budget-bar-fill" style="width:{pct}%;background:{col}"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

            if dir_pred == "Down":
                st.warning(
                    "Pendapatan diprediksi turun. Kurangi pengeluaran tambahan dan prioritaskan tabungan darurat."
                )
            elif dir_pred == "Up":
                st.success(
                    "Pendapatan diprediksi naik. Saat tepat untuk menambah alokasi tabungan atau investasi."
                )
            else:
                st.info(
                    "Pendapatan diprediksi stabil. Pertahankan pola pengeluaran dan pastikan tabungan tetap konsisten."
                )
    with tabs[5]:
        st.markdown("""
        <div class="page-header">
            <h1>Hasil A/B Testing - Income Predictor</h1>
            <p>Apakah Income Predictor terbukti membantu perencanaan anggaran yang lebih akurat?</p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="panel">
            <h3>Metodologi Eksperimen (Notebook 10)</h3>
            <p>
            <strong style="color:#E8EDE9">Data:</strong> synthetic_52week_user_income.csv - 3.000 user x 52 minggu<br>
            <strong style="color:#E8EDE9">Control (1.502):</strong> Budget manual berdasarkan rolling mean 4 minggu<br>
            <strong style="color:#E8EDE9">Treatment (1.498):</strong> Budget adaptif dari Income Predictor AI<br>
            <strong style="color:#E8EDE9">Metrik:</strong> mean_budget_error (selisih planned vs ideal budget)<br>
            <strong style="color:#E8EDE9">Uji Statistik:</strong> Mann-Whitney U (one-tailed, alpha = 0.05)<br><br>
            <span style="color:var(--fg-warn);font-size:.82rem">
            Disclaimer: Seluruh hasil menggunakan data sintetis (proof-of-concept).
            </span>
            </p>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-header">Ringkasan Hasil Eksperimen</div>', unsafe_allow_html=True)

        ab1, ab2, ab3 = st.columns(3)

        with ab1:
            st.metric("N Control", "1,502 users")

        with ab2:
            st.metric("N Treatment", "1,498 users")

        with ab3:
            st.metric("Cohen d", "-1.2188", delta="Efek Besar")

        ab4, ab5 = st.columns(2)

        with ab4:
            st.metric("Mean Error Control", "Rp 47,000")

        with ab5:
            st.metric("Mean Error Treatment", "Rp 14,000", delta="-70.14%")
        
        st.success("H0 ditolak - p-value = 0.000000 (< 0.05). Budget error turun 70.14%. Cohen d = -1.2188 (efek besar).")
        for cn,cap in [
            ("ab_income_predictor_distribution.png","Distribusi Budget Error: Control vs Treatment"),
            ("ab_income_predictor_summary.png","Summary Hasil A/B Testing"),
            ("ab_income_predictor_subgroup.png","Analisis Subgroup per Jenis Pekerjaan"),
            ("ab_income_predictor_qq_plot.png","Q-Q Plot Uji Normalitas"),
        ]:
            p = _try_paths(INCOME_CHARTS_DIR / cn, OUTPUTS_DIR / "charts" / cn)
            if p: st.image(str(p), caption=cap, use_container_width=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame([{
            "Metrik": "Budget Error",
            "Control": "Rp 47,000",
            "Treatment": "Rp 14,000",
            "Reduksi": "-70.14%",
            "U-Stat": "288517",
            "p-value": "0.000000",
            "Cohen d": "-1.2188",
            "Signifikan": "Ya"
        }]), use_container_width=True, hide_index=True)
        rp = INCOME_REPORTS_DIR/"ab_testing_income_predictor_budgeting_report.md"
        if rp.exists():
            with st.expander("Baca laporan lengkap A/B Testing"):
                with open(rp,encoding="utf-8") as f: st.markdown(f.read())
        
    with tabs[6]:
        st.markdown("""
        <div class="page-header">
            <h1>Fingo Assistant</h1>
            <p>Konsultasi keuangan personal berbasis AI - Gemini via mes1205-fingo.hf.space</p>
        </div>""", unsafe_allow_html=True)
        st.markdown("""
        <div class="panel" style="margin-bottom:1.5rem">
            <p>Tulis pertanyaan keuangan. Isi konteks agar saran lebih personal.<br>
            <code>POST https://mes1205-fingo.hf.space/chat</code><br>
            <span style="color:var(--fg-warn);font-size:.82rem">
            Endpoint membutuhkan Gemini API Key aktif di HuggingFace Space.
            </span></p>
        </div>""", unsafe_allow_html=True)
        with st.form("chat_form"):
            user_msg = st.text_area("Pertanyaan keuangan",
                placeholder="Contoh: Gimana cara aku nabung dari pendapatan bulan ini?", height=100)
            st.markdown("**Konteks Keuangan (opsional)**")
            ch1,ch2,ch3,ch4 = st.columns(4)
            ctx_inc  = ch1.number_input("Pendapatan (Rp)",  0,100_000_000,5_000_000,100_000)
            ctx_exp  = ch2.number_input("Pengeluaran (Rp)", 0,100_000_000,3_500_000,100_000)
            ctx_rem  = ch3.number_input("Sisa Budget (Rp)", 0,100_000_000,1_500_000,100_000)
            ctx_imp  = ch4.number_input("Transaksi Impulsif Bulan Ini", 0,100,3,1)
            chat_sub = st.form_submit_button("Kirim", type="primary", use_container_width=True)
        if chat_sub and user_msg.strip():
            with st.spinner("Menghubungi Fingo Assistant..."):
                reply,err = call_chat_api(user_msg.strip(),ctx_inc,ctx_exp,ctx_rem,ctx_imp)
            st.markdown(f'<div class="chat-bubble-user">{user_msg}</div>', unsafe_allow_html=True)
            if reply: st.markdown(f'<div class="chat-bubble-ai">{reply}</div>', unsafe_allow_html=True)
            else: st.error(f"Fingo Assistant tidak dapat merespons: {err}")
        elif chat_sub: st.warning("Tulis pertanyaan terlebih dahulu.")

# ══════════════════════════════════════════════════════════════════════════════
# MODULE 3 - IMPULSIVE DETECTOR
# ══════════════════════════════════════════════════════════════════════════════
elif module == "Impulsive Detector":
    tabs = st.tabs(["Overview Data","EDA","Performa Model","Feature Importance","Coba Deteksi"])

    df_imp  = load_impulsive_data()
    df_test = load_impulsive_test()
    clf_imp = load_impulsive_model()
    eval_bundle = load_impulsive_eval_bundle()
    official_eval = load_impulsive_official_eval_result()
    official_pred = load_impulsive_official_predictions()
    
    with tabs[0]:
        st.markdown("""
        <div class="page-header">
            <h1>Impulsive Detector</h1>
            <p>Overview data final transaksi berlabel - 04_Merged_labeled_transaction.csv</p>
        </div>""", unsafe_allow_html=True)
        if df_imp is None:
            no_data("Dataset tidak ditemukan. Pastikan file ada di streamlit/data/impulsive/")
        else:
            total = len(df_imp)
            lvc   = df_imp["label"].value_counts() if "label" in df_imp.columns else pd.Series()
            n_a,n_p,n_i = lvc.get("AMAN",0),lvc.get("PERTIMBANGAN",0),lvc.get("IMPULSIF",0)
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Total Transaksi", f"{total:,}")
            c2.metric("AMAN",            f"{n_a:,}", delta=f"{n_a/total*100:.1f}%")
            c3.metric("PERTIMBANGAN",    f"{n_p:,}", delta=f"{n_p/total*100:.1f}%")
            c4.metric("IMPULSIF",        f"{n_i:,}", delta=f"{n_i/total*100:.1f}%")

            col_l,col_r = st.columns(2, gap="large")
            with col_l:
                fig,ax = plt.subplots(figsize=(6,4))
                bars = ax.bar(["AMAN","PERTIMBANGAN","IMPULSIF"],[n_a,n_p,n_i],
                              color=[FG,FG_WARN,FG_RED],alpha=0.9)
                for bar,v in zip(bars,[n_a,n_p,n_i]):
                    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+30,
                        f"{v:,}\n{v/total*100:.1f}%", ha="center", fontsize=9,
                        color="#FFFFFF", fontweight="bold")
                ax.set_title("Distribusi Label Transaksi", color="#FFFFFF")
                plt.tight_layout(pad=0.8); st.pyplot(fig, use_container_width=True); plt.close()
            with col_r:
                if "source" in df_imp.columns:
                    sc = df_imp["source"].value_counts()
                    fig,ax = plt.subplots(figsize=(6,4))
                    ax.barh(sc.index, sc.values, color=FG_BLUE, height=0.65, alpha=0.85)
                    for bar,v in zip(ax.patches, sc.values):
                        ax.text(v+5, bar.get_y()+bar.get_height()/2,
                            str(v), va="center", fontsize=9, color="#FFFFFF")
                    ax.set_title("Jumlah Transaksi per Sumber", color="#FFFFFF")
                    ax.invert_yaxis()
                    plt.tight_layout(pad=0.8); st.pyplot(fig, use_container_width=True); plt.close()
            if "category" in df_imp.columns:
                cc = df_imp["category"].value_counts()
                fig,ax = plt.subplots(figsize=(10,3.5))
                bars = ax.bar(cc.index, cc.values,
                    color=[FG_RED if c in HEDONIC_CATS else FG_BLUE for c in cc.index], alpha=0.9)
                for bar,v in zip(bars,cc.values):
                    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+10,
                        str(v), ha="center", fontsize=8, color="#FFFFFF", fontweight="bold")
                ax.set_title("Jumlah Transaksi per Kategori (merah = hedonic)", color="#FFFFFF")
                plt.tight_layout(pad=0.8); st.pyplot(fig, use_container_width=True); plt.close()

    with tabs[1]:
        st.markdown("""
        <div class="page-header">
            <h1>Exploratory Data Analysis</h1>
            <p>Pola waktu, kategori, dan sinyal impulsif pada dataset transaksi</p>
        </div>""", unsafe_allow_html=True)
        if df_imp is None:
            no_data("Dataset tidak ditemukan.")
        else:
            df_e = df_imp.copy()
            df_e["is_imp_bin"] = (df_e["label"]=="IMPULSIF").astype(int)
            col_l,col_r = st.columns(2, gap="large")
            with col_l:
                if "category" in df_e.columns:
                    cat_r = (df_e.groupby("category")
                        .agg(count=("is_imp_bin","count"),rate=("is_imp_bin","mean"))
                        .reset_index().sort_values("rate",ascending=False))
                    fig,axes = plt.subplots(1,2,figsize=(10,4))
                    clrs = [FG_RED if r>0.15 else FG_WARN if r>0.05 else FG_MUTED for r in cat_r["rate"]]
                    axes[0].barh(cat_r["category"],cat_r["count"],color=FG_BLUE,height=0.6,alpha=0.85)
                    axes[0].set_title("Volume per Kategori",color="#FFFFFF"); axes[0].invert_yaxis()
                    axes[1].barh(cat_r["category"],cat_r["rate"]*100,color=clrs,height=0.6,alpha=0.9)
                    axes[1].set_title("Impulsive Rate per Kategori (%)",color="#FFFFFF"); axes[1].invert_yaxis()
                    plt.tight_layout(pad=0.8); st.pyplot(fig, use_container_width=True); plt.close()
                if "is_weekend" in df_e.columns:
                    wr = df_e.groupby("is_weekend")["is_imp_bin"].mean()
                    fig,ax = plt.subplots(figsize=(5,3.5))
                    ax.bar(["Hari Kerja","Akhir Pekan"],
                           [wr.get(0,0)*100,wr.get(1,0)*100],
                           color=[FG_BLUE,FG_RED],alpha=0.9)
                    ax.set_title("Impulsive Rate: Weekday vs Weekend",color="#FFFFFF"); ax.set_ylabel("Rate (%)")
                    plt.tight_layout(pad=0.8); st.pyplot(fig, use_container_width=True); plt.close()
            with col_r:
                if "time_segment" in df_e.columns:
                    ts_r = (df_e.groupby("time_segment")
                        .agg(count=("is_imp_bin","count"),rate=("is_imp_bin","mean"))
                        .reset_index().sort_values("rate",ascending=False))
                    fig,ax = plt.subplots(figsize=(7,4))
                    clrs=[FG_RED if r>0.15 else FG_WARN if r>0.05 else FG_MUTED for r in ts_r["rate"]]
                    bars=ax.bar(ts_r["time_segment"],ts_r["rate"]*100,color=clrs,alpha=0.9)
                    for bar,v in zip(bars,ts_r["rate"]):
                        ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.3,
                            f"{v*100:.1f}%",ha="center",fontsize=9,color="#FFFFFF",fontweight="bold")
                    ax.set_title("Impulsive Rate per Time Segment",color="#FFFFFF"); ax.set_ylabel("Rate (%)")
                    plt.xticks(rotation=30,ha="right",fontsize=9)
                    plt.tight_layout(pad=0.8); st.pyplot(fig, use_container_width=True); plt.close()
                if "hour" in df_e.columns:
                    hr_r = df_e.groupby("hour")["is_imp_bin"].mean()
                    fig,ax = plt.subplots(figsize=(7,4))
                    ax.bar(hr_r.index, hr_r.values*100,
                        color=[FG_RED if h>=22 or h<=4 else FG_WARN if h>=19 else FG_BLUE for h in hr_r.index],
                        alpha=0.85)
                    ax.set_title("Impulsive Rate per Jam",color="#FFFFFF")
                    ax.set_xlabel("Jam"); ax.set_ylabel("Rate (%)"); ax.set_xticks(range(0,24,2))
                    plt.tight_layout(pad=0.8); st.pyplot(fig, use_container_width=True); plt.close()
            score_col = "impulsive_score" if "impulsive_score" in df_e.columns else \
                        "fingo_impulse_signal" if "fingo_impulse_signal" in df_e.columns else None
            if score_col:
                st.markdown('<div class="section-header">Distribusi Impulsive Score per Label</div>', unsafe_allow_html=True)
                fig,ax = plt.subplots(figsize=(10,4))
                for lb,color in {"AMAN":FG,"PERTIMBANGAN":FG_WARN,"IMPULSIF":FG_RED}.items():
                    sub = df_e[df_e["label"]==lb][score_col]
                    if len(sub)>0: ax.hist(sub,bins=30,alpha=0.5,label=lb,color=color,density=True)
                ax.set_title("Distribusi Impulsive Score per Label",color="#FFFFFF")
                ax.set_xlabel("Impulsive Score"); ax.legend(fontsize=8)
                plt.tight_layout(pad=0.8); st.pyplot(fig, use_container_width=True); plt.close()

    with tabs[2]:
        st.markdown("""
        <div class="page-header">
            <h1>Performa Model Impulsive Detector</h1>
            <p>Official evaluation results dari AI-Fingo evaluation scripts</p>
        </div>""", unsafe_allow_html=True)

        if eval_bundle is not None:
            official = eval_bundle["official_metrics"]

            st.markdown('<div class="section-header">Official Evaluation Results</div>', unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            c1.metric(
                "Random Split",
                f"{official['random_split_with_impulsive_score']['accuracy'] * 100:.3f}%",
                "With impulsive_score"
            )
            c2.metric(
                "Time-Based Holdout",
                f"{official['time_based_holdout_with_score_features']['accuracy'] * 100:.3f}%",
                "With score-derived features"
            )
            c3.metric(
                "Rolling CV",
                f"{official['rolling_cv_with_score_features']['average_accuracy'] * 100:.3f}%",
                "Average 5 splits"
            )

            st.markdown('<div class="section-header">Ablation Results</div>', unsafe_allow_html=True)

            a1, a2, a3 = st.columns(3)
            a1.metric(
                "Random Split Without Score",
                f"{official['random_split_without_impulsive_score']['accuracy'] * 100:.3f}%"
            )
            a2.metric(
                "Time Holdout Without Score",
                f"{official['time_based_holdout_without_score_features']['accuracy'] * 100:.3f}%"
            )
            a3.metric(
                "Rolling CV Without Score",
                f"{official['rolling_cv_without_score_features']['average_accuracy'] * 100:.3f}%"
            )

            st.info(
                "Angka di atas berasal dari official AI-Fingo evaluation scripts. "
                "Evaluasi ulang dari test_df.csv hanya digunakan sebagai diagnostic check jika test set lengkap."
            )

        else:
            no_data("impulsive_eval_bundle.pkl belum tersedia di streamlit/models/")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Evaluation Output dari AI-Fingo Script</div>', unsafe_allow_html=True)

        if official_eval is None:
            no_data(
                "random_split_with_score_eval_result.pkl belum tersedia. "
                "Jalankan compare_impulsive_score_cla.py lalu copy hasilnya ke "
                "streamlit/data/impulsive/evaluation/."
            )
        else:
            acc = official_eval["accuracy"]
            prec = official_eval["macro_precision"]
            rec = official_eval["macro_recall"]
            f1 = official_eval["macro_f1"]

            d1, d2, d3, d4 = st.columns(4)
            d1.metric("Accuracy", f"{acc * 100:.3f}%")
            d2.metric("Macro Precision", f"{prec:.4f}")
            d3.metric("Macro Recall", f"{rec:.4f}")
            d4.metric("Macro F1", f"{f1:.4f}")

            classes = official_eval.get("classes", ["AMAN", "IMPULSIF", "PERTIMBANGAN"])
            cm = np.array(official_eval["confusion_matrix"])

            st.markdown('<div class="section-header">Confusion Matrix</div>', unsafe_allow_html=True)
            fig_cm = plot_confusion_matrix(cm, classes)
            st.pyplot(fig_cm, use_container_width=False)
            plt.close()

            with st.expander("Classification Report"):
                if "classification_report_text" in official_eval:
                    st.code(official_eval["classification_report_text"])
                else:
                    st.json(official_eval.get("classification_report", {}))

        if official_pred is not None:
            col_d1, col_d2 = st.columns(2, gap="large")

            with col_d1:
                st.markdown('<div class="section-header">Distribusi Label Aktual</div>', unsafe_allow_html=True)
                st.dataframe(
                    official_pred["actual_label"]
                    .value_counts()
                    .rename_axis("label")
                    .reset_index(name="count"),
                    use_container_width=True,
                    hide_index=True,
                )

            with col_d2:
                st.markdown('<div class="section-header">Distribusi Label Prediksi</div>', unsafe_allow_html=True)
                st.dataframe(
                    official_pred["predicted_label"]
                    .value_counts()
                    .rename_axis("label")
                    .reset_index(name="count"),
                    use_container_width=True,
                    hide_index=True,
                )

            with st.expander("Preview Evaluation Predictions"):
                st.dataframe(
                    official_pred.head(50),
                    use_container_width=True,
                    hide_index=True,
                )

    with tabs[3]:
        st.markdown("""
        <div class="page-header">
            <h1>Feature Importance</h1>
            <p>Fitur paling berpengaruh dalam model Impulsive Detector</p>
        </div>""", unsafe_allow_html=True)

        if clf_imp is None:
            no_data("Model tidak ditemukan di streamlit/models/fingo_label_classifier.joblib")
        else:
            try:
                prep_s = clf_imp.named_steps["preprocessor"]
                cls_s  = clf_imp.named_steps["classifier"]
                fn     = prep_s.get_feature_names_out()
                imps   = cls_s.feature_importances_

                imp_df = pd.DataFrame({"feature":fn,"importance":imps})

                def _agg_name(f):
                    if "__" in f:
                        _,rest = f.split("__",1)
                        for kc in IMP_MODEL_FEATURES:
                            if rest==kc or rest.startswith(kc+"_"): return kc
                        return rest
                    return f

                imp_df["original"] = imp_df["feature"].apply(_agg_name)
                agg = imp_df.groupby("original")["importance"].sum().sort_values(ascending=False)

                col_l,col_r = st.columns(2, gap="large")
                with col_l:
                    top_raw = imp_df.nlargest(15,"importance")
                    fig,ax = plt.subplots(figsize=(7,6))
                    clrs=[FG if i<3 else FG_BLUE if i<7 else FG_MUTED for i in range(len(top_raw))]
                    ax.barh(top_raw["feature"][::-1], top_raw["importance"][::-1]*100,
                            color=clrs[::-1], height=0.6, alpha=0.9)
                    for bar,v in zip(ax.patches, top_raw["importance"][::-1].values):
                        ax.text(v*100+0.1, bar.get_y()+bar.get_height()/2,
                            f"{v*100:.1f}%", va="center", fontsize=8, color="#FFFFFF", fontweight="bold")
                    ax.set_title("Top 15 Raw Features", color="#FFFFFF")
                    ax.set_xlabel("Importance (%)")
                    plt.tight_layout(pad=0.8); st.pyplot(fig, use_container_width=True); plt.close()

                with col_r:
                    top_agg = agg.head(10)
                    fig,ax = plt.subplots(figsize=(7,6))
                    clrs=[FG if i<3 else FG_BLUE if i<6 else FG_MUTED for i in range(len(top_agg))]
                    ax.barh(top_agg.index[::-1], top_agg.values[::-1]*100,
                            color=clrs[::-1], height=0.6, alpha=0.9)
                    for i,v in enumerate(top_agg.values[::-1]):
                        ax.text(v*100+0.2, i, f"{v*100:.1f}%",
                            va="center", fontsize=9, color="#FFFFFF", fontweight="bold")
                    ax.set_title("Feature Importance (Agregasi per Fitur Asal)", color="#FFFFFF")
                    ax.set_xlabel("Importance (%)")
                    plt.tight_layout(pad=0.8); st.pyplot(fig, use_container_width=True); plt.close()

                st.markdown('<div class="section-header">Tabel Feature Importance</div>', unsafe_allow_html=True)
                ket = {
                    "impulsive_score":"Skor agregat sinyal impulsif (0-10)",
                    "signal_band":"Band intensitas (low/watch/high)",
                    "driver_count":"Jumlah driver aktif (night/hedonic/high_amount/weekend)",
                    "is_weekend":"Transaksi di akhir pekan","day_of_week":"Hari dalam seminggu",
                    "amount_z":"Z-score nominal transaksi","amount_score":"Skor nominal vs median",
                    "time_segment":"Segmen waktu (pagi/siang/malam/late_night)",
                    "hour":"Jam transaksi","amount":"Nominal transaksi (IDR)",
                    "amount_log":"Log natural nominal transaksi","category":"Kategori transaksi",
                    "is_hedonic_category":"Apakah kategori hedonic","source":"Sumber dataset",
                    "metode_pembayaran":"Metode pembayaran",
                    "category_type":"Tipe kategori (hedonic/utilitarian/neutral)",
                    "is_night":"Transaksi dini hari / larut malam",
                }
                agg_df = agg.reset_index()
                agg_df.columns=["Fitur","Importance"]
                agg_df["Importance (%)"] = agg_df["Importance"].apply(lambda v:f"{v*100:.2f}%")
                agg_df["Keterangan"]     = agg_df["Fitur"].map(ket).fillna("")
                st.dataframe(agg_df[["Fitur","Importance (%)","Keterangan"]],
                             use_container_width=True, hide_index=True)

            except Exception as e:
                st.error(f"Error memuat feature importance: {e}")

    with tabs[4]:
        st.markdown("""
        <div class="page-header">
            <h1>Coba Deteksi Transaksi</h1>
            <p>Gunakan model fingo_label_classifier.joblib untuk mendeteksi apakah transaksi impulsif</p>
        </div>""", unsafe_allow_html=True)

        if clf_imp is None:
            no_data("Model tidak ditemukan di streamlit/models/fingo_label_classifier.joblib")
        else:
            try:
                model_expected = list(clf_imp.feature_names_in_)
            except Exception:
                model_expected = IMP_MODEL_FEATURES

            st.markdown("""
            <div class="panel" style="margin-bottom:1.5rem">
                <p>Masukkan detail transaksi. Model akan memprediksi label
                <strong style="color:#00C471">AMAN</strong>,
                <strong style="color:#F5A623">PERTIMBANGAN</strong>, atau
                <strong style="color:#E8504A">IMPULSIF</strong>
                beserta probabilitas per kelas.</p>
            </div>""", unsafe_allow_html=True)

            with st.form("imp_detect_form"):
                col1,col2 = st.columns(2, gap="large")
                with col1:
                    amount_in   = st.number_input("Nominal Transaksi (Rp)", 0,100_000_000,150_000,5_000)
                    category_in = st.selectbox("Kategori",
                        ["Makanan","Transportasi","Hiburan","Belanja",
                         "Pendidikan","Kesehatan","Tagihan","Lainnya"])
                    metode_in   = st.selectbox("Metode Pembayaran", METODE_OPTIONS)
                with col2:
                    tgl_in  = st.date_input("Tanggal Transaksi", datetime.date.today())
                    hour_in = st.slider("Jam Transaksi", 0, 23, 20)
                    budget_in = st.number_input("Budget mingguan (opsional, Rp)", 0,50_000_000,0,50_000)
                sub_imp = st.form_submit_button("Deteksi Sekarang", type="primary", use_container_width=True)

            if sub_imp:
                dow           = tgl_in.weekday()
                is_weekend_in = dow >= 5
                is_night_in   = hour_in >= 22 or hour_in <= 4
                if hour_in<=4 or hour_in>=22: ts="late_night"
                elif 5<=hour_in<=10:          ts="morning"
                elif 11<=hour_in<=14:         ts="midday"
                elif 15<=hour_in<=18:         ts="evening"
                else:                          ts="night"

                row, imp_score, sig_band, drv_count = build_model_row(
                    amount_in, category_in, metode_in, hour_in, dow,
                    is_weekend_in, is_night_in, ts, df_imp)

                # Ensure all expected columns exist
                for c in model_expected:
                    if c not in row.columns: row[c] = 0
                row = row[model_expected]
                for c in ["is_hedonic_category","is_night","is_weekend"]:
                    if c in row.columns: row[c] = row[c].astype(bool)

                try:
                    label_pred = clf_imp.predict(row)[0]
                    proba_raw  = clf_imp.predict_proba(row)[0]
                    proba_dict = dict(zip(clf_imp.classes_, proba_raw))
                except Exception as e:
                    st.error(f"Prediction error: {e}")
                    label_pred=None; proba_dict={}

                if label_pred is not None:
                    if label_pred=="AMAN":
                        bg="rgba(0,196,113,.08)"; bd="rgba(0,196,113,.3)"; lc="#00C471"
                    elif label_pred=="PERTIMBANGAN":
                        bg="rgba(245,166,35,.08)"; bd="rgba(245,166,35,.3)"; lc="#F5A623"
                    else:
                        bg="rgba(232,80,74,.08)"; bd="rgba(232,80,74,.3)"; lc="#E8504A"

                    alert_txt   = "NO_ALERT" if label_pred=="AMAN" else "ALERT"
                    alert_badge = "badge-green" if label_pred=="AMAN" else "badge-red"
                    is_hedonic  = category_in in HEDONIC_CATS

                    st.markdown(f"""
                    <div style="background:{bg};border:1px solid {bd};border-radius:12px;padding:1.6rem 2rem;margin:1rem 0">
                        <div style="font-size:.75rem;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:{lc};margin-bottom:.5rem">Hasil Deteksi</div>
                        <div style="font-family:'DM Serif Display',serif;font-size:2.5rem;color:#E8EDE9;line-height:1;margin-bottom:.4rem;font-weight:700">{label_pred}</div>
                        <div style="font-size:.85rem;color:#6B7E74;margin-bottom:.8rem">
                            {fmt_idr_full(amount_in)} - {category_in} - {ts} - {'Akhir Pekan' if is_weekend_in else 'Hari Kerja'}
                        </div>
                        <span class="badge {alert_badge}">{alert_txt}</span>
                        &nbsp;
                        <span style="font-size:.8rem;color:#6B7E74">
                            Impulsive score: {imp_score:.2f} | Signal: {sig_band} | Drivers aktif: {drv_count}
                        </span>
                    </div>""", unsafe_allow_html=True)

                    if proba_dict:
                        st.markdown('<div class="section-header">Probabilitas per Kelas</div>', unsafe_allow_html=True)
                        for lb,lc2 in [("AMAN",FG),("PERTIMBANGAN",FG_WARN),("IMPULSIF",FG_RED)]:
                            pv = float(proba_dict.get(lb,0.0))
                            st.markdown(f"""
                            <div class="budget-bar-wrap">
                                <div class="budget-bar-label">
                                    <span style="color:{lc2};font-weight:600">{lb}</span>
                                    <span>{pv*100:.1f}%</span>
                                </div>
                                <div class="budget-bar-track">
                                    <div class="budget-bar-fill" style="width:{pv*100:.1f}%;background:{lc2}"></div>
                                </div>
                            </div>""", unsafe_allow_html=True)

                    st.markdown('<div class="section-header">Faktor Risiko Aktif</div>', unsafe_allow_html=True)
                    risks=[]
                    if is_hedonic:   risks.append(f"Kategori hedonic: {category_in}")
                    if is_night_in:  risks.append("Transaksi larut malam / dini hari")
                    if is_weekend_in:risks.append("Transaksi di akhir pekan")
                    if df_imp is not None and "amount" in df_imp.columns:
                        ref_mean = df_imp["amount"].mean(); ref_std = df_imp["amount"].std()
                        if ref_std and (amount_in-ref_mean)/ref_std > 1.5:
                            risks.append("Nominal jauh di atas rata-rata dataset")
                    if risks:
                        for r in risks: st.markdown(f'<span class="badge badge-yellow">{r}</span>&nbsp;', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="badge badge-green">Tidak ada faktor risiko signifikan</span>', unsafe_allow_html=True)

                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown('<div class="section-header">Rekomendasi</div>', unsafe_allow_html=True)
                    if label_pred=="IMPULSIF":
                        st.error("Transaksi ini berpotensi IMPULSIF. Tunda keputusan pembelian minimal 24 jam.")
                        if is_hedonic: st.warning(f"Kategori {category_in} termasuk hedonic dengan impulsive rate tinggi.")
                        if is_night_in or ts in["night","late_night"]: st.warning("Transaksi larut malam cenderung lebih impulsif.")
                        if is_weekend_in: st.warning("Transaksi akhir pekan memiliki risiko impulsif lebih tinggi.")
                    elif label_pred=="PERTIMBANGAN":
                        st.warning("Transaksi ini memerlukan pertimbangan. Pastikan sesuai budget sebelum melanjutkan.")
                    else:
                        st.success("Transaksi ini tergolong AMAN. Tetap pantau total pengeluaran harian.")

                    if budget_in > 0 and label_pred != "AMAN":
                        pct_b = amount_in/budget_in*100
                        st.markdown(f"""
                        <div class="panel" style="margin-top:1rem">
                            <h3>Proyeksi Dampak Budget</h3>
                            <p>Transaksi ini menyerap <strong style="color:#E8EDE9">{pct_b:.1f}%</strong>
                            dari budget mingguan ({fmt_idr_full(budget_in)}).
                            Sisa: <strong style="color:#E8EDE9">{fmt_idr_full(budget_in-amount_in)}</strong>.</p>
                        </div>""", unsafe_allow_html=True)
