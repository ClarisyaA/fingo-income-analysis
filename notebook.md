# Notebook Pipeline — Fingo Income Predictor
**Tim:** CC26-PSU217 | **Versi:** v13-FINAL

---

## Alur Modular Notebook

Setiap notebook menarik output dari GitHub di awal (git pull) dan
mendorong hasilnya ke GitHub di akhir (git push).

```
01_Data_Preparation
       ↓ survey_clean.csv (dengan timestamp)
02_Temporal_Mapping
       ↓ survey_temporal_mapped.csv
       ↓ survey_weekly_income_long.csv
03_EDA_Survey
       ↓ charts + survey_eda_summary.md
04_Synthetic_Data_Generation
       ↓ synthetic_52week_user_income.csv
       ↓ synthetic_params.json
05_Feature_Engineering
       ↓ income_features.csv
       ↓ feature_columns.json
06_Model_Dataset_Split
       ↓ income_train.csv / income_val.csv / income_test.csv
       ↓ income_scalers.pkl
       ↓ model_contract.json
07_Bias_Validation
       ↓ bias_validation_report.md + charts
08_Documentation_Export
       ↓ README.md / notebook.md / data_dictionary.md
```

---

## Detail per Notebook

### 01_Data_Preparation.ipynb
**Input:** `data/raw/form_responses.csv`, BPS files  
**Proses:**
- Clone/pull repo GitHub
- Setup environment + install library
- Load raw data survey (384 responden)
- Form column mapping berdasarkan posisi kolom
- Drop PII (consent, kontak_gopay)
- **Parse timestamp (DIPERTAHANKAN untuk notebook 02)**
- Convert numerik + clip nilai tidak realistis
- Standardisasi kategori (GIG_MAP, DOMISILI_MAP)
- Multi-hot encoding kolom multi-select
- Feature engineering dasar (avg_weekly_income, income_cv_4w, dll)
- Validasi missing value

**Output:** `data/processed/survey_clean.csv` (dengan timestamp)

---

### 02_Temporal_Mapping.ipynb
**Input:** `data/processed/survey_clean.csv`  
**Proses:**
- Mapping `income_w1–income_w4` ke periode kalender berdasarkan timestamp
- `income_w1`: H-7 s/d H-1 dari timestamp responden (terbaru)
- `income_w2`: H-14 s/d H-8
- `income_w3`: H-21 s/d H-15
- `income_w4`: H-28 s/d H-22 (terlama)
- Tambah kolom: period_start, period_end, calendar_month, week_of_month, iso_week
- Buat long-format dataset untuk analisis mingguan

**Output:**
- `data/processed/survey_temporal_mapped.csv`
- `data/processed/survey_weekly_income_long.csv`

---

### 03_EDA_Survey.ipynb
**Input:** survey_temporal_mapped.csv + survey_weekly_income_long.csv  
**Proses:**
- Analisis distribusi income per gig_type, domisili, relative_week
- Analisis calendar_month dan week_of_month dari temporal mapping
- Jawab: income tertinggi di relative_week mana? week_of_month berapa?

**Output:** Charts + `outputs/reports/survey_eda_summary.md`

---

### 04_Synthetic_Data_Generation.ipynb
**Input:** `data/processed/survey_temporal_mapped.csv`  
**Proses:**
- Generate 3.000 synthetic users dari distribusi survey
- AR(1) income generation dengan noise/shock per gig_type
- Seasonal multiplier (Ramadan, Harbolnas, payday, weekend)

**Output:**
- `data/synthetic/synthetic_52week_user_income.csv`
- `data/synthetic/synthetic_params.json`

---

### 05_Feature_Engineering.ipynb
**Input:** `data/synthetic/synthetic_52week_user_income.csv`  
**Proses:**
- Sliding window 4 lag dari 52-week history
- Rolling mean, std, min, max (4w, 2w, 8w)
- Lag features: lag_1 (terbaru) → lag_4 (terlama)
- income_growth_1w, income_volatility, trend_slope_4w
- Calendar features, seasonal flags, OHE gig_type
- Anti-leakage check

**Output:** `data/processed/income_features.csv`

---

### 06_Model_Dataset_Split.ipynb
**Input:** `data/processed/income_features.csv`  
**Proses:**
- Kronologis split by synthetic_user_id: 70/15/15
- Fit scaler (log1p → MinMaxScaler) on train only
- Simpan model contract

**Output:** train/val/test CSVs + scalers + model_contract.json

---

### 07_Bias_Validation.ipynb
**Input:** income_features.csv + survey_temporal_mapped.csv + synthetic_52week_user_income.csv  
**Proses:**
- Mean vs BPS benchmark
- Distribution test (KS)
- Seasonal direction check
- Autocorrelation lag-1
- BPS range per domisili
- Income per gig_type: synthetic vs survey

**Output:** `outputs/reports/bias_validation_report.md` + charts

---

### 08_Documentation_Export.ipynb
**Input:** semua output notebook sebelumnya  
**Output:** `README.md`, `notebook.md`, `data_dictionary.md`

---

## File Final untuk AI Engineer

File di `outputs/model_contract/`:
- `income_train.csv` — dataset training (70%)
- `income_val.csv` — dataset validasi (15%)
- `income_test.csv` — dataset test (15%)
- `income_scalers.pkl` — scaler (target + feature)
- `feature_columns.json` — daftar fitur + metadata
- `model_contract.json` — kontrak lengkap pipeline
