# Fingo — Income Analysis (DS2)

Data Science 2 | Coding Camp 2026 × DBS Foundation
Tim CC26-PSU217 | Data Scientist: Clarisya Adeline

## Deskripsi
Pipeline data untuk fitur Income Predictor Fingo.
Menghasilkan `income_clean.csv` untuk model LSTM (Martha).

## Struktur
- `data/raw/` — dataset mentah (Kaggle + survei)
- `data/processed/` — data hasil cleaning & feature engineering
- `data/synthetic/` — data sintetis hasil generate
- `notebooks/` — notebook analisis per tahap
- `streamlit/` — dashboard Streamlit 6 modul
- `outputs/` — chart EDA & laporan validasi

## Urutan Notebook
1. 01_survey_cleaning.ipynb
2. 02_kaggle_calibration.ipynb
3. 03_generate_synthetic.ipynb
4. 04_merge_and_feature_eng.ipynb
5. 05_eda_income.ipynb
6. 06_train_val_test_split.ipynb

## Setup
pip install -r requirements.txt