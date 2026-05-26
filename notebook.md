# Notebook Process Flow — Fingo Weekly Income Forecasting

Dokumen ini menjelaskan alur keseluruhan proses yang dilakukan pada `Notebook_Income.ipynb`.

## 1. Tujuan Notebook

Notebook ini membangun pipeline **weekly income forecasting** untuk pekerja gig/informal Indonesia. Fokus utamanya adalah:

1. Membersihkan data survei real sebanyak **384 responden**.
2. Menggunakan survei real sebagai **empirical baseline/distribusi acuan**.
3. Membentuk dataset synthetic longitudinal sebanyak **3.000 synthetic users × 52 minggu**.
4. Membuat dataset forecasting mingguan berbasis sliding window.
5. Melatih dan mengevaluasi model untuk:
   - regresi: prediksi `next_week_income`;
   - klasifikasi: prediksi `next_week_direction` (`Up`, `Stable`, `Down`).
6. Menghasilkan file kontrak data/model yang bisa dipakai oleh AI Engineer.

## 2. Peran Dataset

| Dataset | Peran |
|---|---|
| Survey real 384 responden | Distribusi acuan, EDA, synthetic generation baseline, dan sanity check. |
| BPS income benchmark | Referensi pendapatan regional per domisili, khususnya `bps_jasa_weekly`. |
| Synthetic 3.000 users × 52 minggu | Dataset training utama karena survei real hanya memiliki histori 4 minggu. |
| Real 4-week forecasting dataset | Sanity check/empirical reference, bukan training utama. |

## 3. Alur Notebook per Bagian

### BAGIAN 0 — Setup & Instalasi

Notebook dimulai dengan clone/pull repo GitHub secara aman di Google Colab. Setelah itu dibuat struktur folder yang benar-benar dipakai dalam pipeline, lalu dilakukan instalasi/import library seperti `pandas`, `numpy`, `scikit-learn`, `xgboost`, `matplotlib`, `seaborn`, dan helper function untuk baca/simpan file.

Output penting:
- Struktur folder `data/processed`, `data/synthetic`, `outputs/charts`, `outputs/dashboard`, `outputs/model_results`, `outputs/preprocessors`, `outputs/model_contract`, dan `outputs/reports`.
- Helper seperti `safe_read_csv`, `safe_to_csv`, `safe_savefig`, dan formatter rupiah.

### BAGIAN 1 — Problem Discovery

Bagian ini menjelaskan latar belakang masalah: pekerja gig memiliki pendapatan mingguan yang fluktuatif, sehingga perlu sistem prediksi pendapatan agar aplikasi Fingo dapat membantu budgeting dan perencanaan keuangan.

### BAGIAN 2 — Business Questions

Notebook mendefinisikan business questions seperti:
- rata-rata pendapatan mingguan per jenis pekerjaan gig;
- jenis pekerjaan paling fluktuatif;
- pola pendapatan per minggu;
- pengaruh seasonal event;
- performa model prediksi;
- potensi simulasi A/B testing.

### BAGIAN 3 — Data Gathering

Notebook memuat beberapa sumber data:
1. `form_responses.csv` sebagai data survei utama.
2. File BPS pekerja bebas/informal tahun 2023–2025 sebagai benchmark pendapatan regional.

Data survei diload dari kandidat path:
- `data/raw/form_responses.csv`
- `form_responses.csv`

Data BPS diload secara robust berdasarkan keyword nama file.

### BAGIAN 3.5 — Form Response Mapping

Mapping form dilakukan berdasarkan posisi kolom agar lebih robust terhadap perubahan nama kolom Google Form. Notebook mengubah kolom mentah menjadi nama teknis seperti:

- `timestamp`
- `consent`
- `usia`
- `domisili`
- `pekerjaan`
- `sumber_pekerjaan`
- `status_penghasilan`
- `lama_kerja_bulan`
- `hari_kerja_per_minggu`
- `jam_kerja_per_hari`
- `income_w1`
- `income_w2`
- `income_w3`
- `income_w4`
- `waktu_ramai`
- `faktor_fluktuasi`
- `fitur_dibutuhkan`
- `kontak_gopay`

Output:
- `outputs/reports/form_column_mapping.json`

### BAGIAN 4 — Data Assessing

Notebook melakukan pengecekan awal terhadap data mentah:
- shape dataset;
- tipe data;
- missing values;
- potensi PII;
- nilai tidak realistis;
- kategori yang perlu distandardisasi.

Output:
- `outputs/reports/data_assessing_summary.csv`

### BAGIAN 5 — Data Cleaning

Tahapan cleaning utama:

1. Rename kolom sesuai mapping.
2. Drop PII:
   - `consent`
   - `kontak_gopay`
3. Drop duplikasi.
4. Buat `respondent_id`.
5. Konversi kolom numerik.
6. Clip nilai tidak realistis:
   - usia dibatasi 17–65;
   - hari kerja dibatasi 0–7;
   - jam kerja per hari dibatasi 0–16;
   - income diclip minimal 0.
7. Standardisasi kategori:
   - `gig_type` dari 8 kategori pekerjaan;
   - `domisili_code` dari kategori wilayah.
8. Multi-hot encoding untuk:
   - sumber pekerjaan/platform;
   - waktu ramai;
   - faktor fluktuasi;
   - fitur yang dibutuhkan.
9. Calendar features dari timestamp.
10. Feature engineering dasar:
    - `total_jam_seminggu`
    - `experience_months_log`
    - `avg_weekly_income`
    - `monthly_income`
    - `income_std_4w`
    - `income_cv_4w`
    - `income_range_4w`
    - preference features (`pref_*`)
11. Merge benchmark BPS menjadi `bps_jasa_weekly`.

Output:
- `data/processed/cleaned_survey_data.csv`

### BAGIAN 6 — EDA Survey Asli

EDA dilakukan untuk memahami:
- distribusi `gig_type`;
- distribusi `domisili_code`;
- ringkasan income per `gig_type`;
- tren pendapatan kronologis `income_w4 → income_w3 → income_w2 → income_w1`.

Output:
- `outputs/charts/gig_type_distribution.png`
- `outputs/charts/income_by_gig_type.png`
- `outputs/charts/weekly_income_trend_w4_to_w1.png`
- `outputs/dashboard/gig_type_distribution.csv`
- `outputs/dashboard/real_4w_income_summary.csv`

### BAGIAN 7 — Survey Distribution Profiling

Survey real diprofilkan agar bisa dipakai sebagai dasar synthetic generation. Bagian ini membuat:
- klasifikasi arah income (`Up`, `Stable`, `Down`);
- distribusi income per `gig_type`;
- statistik seperti median, mean, std, CV;
- cap realistis income per jenis pekerjaan.

Aturan penting:
- `DIRECTION_THRESHOLD = 0.10`
- `Up` jika perubahan `>= 10%`
- `Down` jika perubahan `<= -10%`
- `Stable` jika selain itu

### BAGIAN 8 — Real 4-Week Sanity Dataset

Notebook membuat dataset forecasting dari real survey 4 minggu. Dataset ini **bukan training utama** karena histori terlalu pendek. Fungsinya hanya untuk benchmark/sanity check.

Urutan income:
- `income_w4` = terlama / 4 minggu lalu
- `income_w3`
- `income_w2`
- `income_w1` = terbaru / minggu lalu

Output:
- `data/processed/weekly_forecasting_dataset_real_4w.csv`
- `outputs/preprocessors/gig_label_encoder.pkl`
- `outputs/preprocessors/dom_label_encoder.pkl`
- `outputs/preprocessors/direction_label_encoder.pkl`

### BAGIAN 9 — Generate 3.000 Synthetic Users

Notebook membuat synthetic longitudinal dataset dengan cara:
1. Sampling 3.000 user dari distribusi survey real.
2. Membuat profil synthetic berdasarkan user asli sebagai template.
3. Menambahkan variasi usia, jam kerja, hari kerja, baseline income, dan volatility.
4. Generate pendapatan 52 minggu menggunakan pendekatan autoregressive dengan shock/noise.
5. Menambahkan fitur kalender dan seasonal event.

Output:
- `data/synthetic/synthetic_52week_user_income.csv`

Ukuran output:
- 3.000 users
- 52 minggu per user
- total 156.000 baris raw synthetic

### BAGIAN 10 — Generate Synthetic Weekly Forecasting Dataset

Dari data synthetic 52 minggu, notebook membuat sliding window forecasting dataset:

- Input history: 4 minggu sebelumnya (`lag_1_income` sampai `lag_4_income`)
- Target: income minggu berikutnya (`next_week_income`)
- Target direction: `next_week_direction`

Setiap user menghasilkan 48 forecast windows.

Output:
- `data/synthetic/synthetic_52week_weekly_forecasting_dataset.csv`

Ukuran estimasi:
- 3.000 users × 48 rows = 144.000 rows

### BAGIAN 11 — Split Train/Test by User

Split dilakukan berdasarkan `synthetic_user_id`, bukan random row. Ini penting agar data user yang sama tidak bocor ke train dan test.

Output:
- `data/synthetic/synthetic_52w_train.csv`
- `data/synthetic/synthetic_52w_test.csv`
- `data/processed/real_4w_train.csv`
- `data/processed/real_4w_test.csv`

Aturan:
- test size = 20%
- random state = 42
- split by user ID

### BAGIAN 12 — Feature Engineering + Anti-Leakage

Notebook menentukan `FEATURE_COLS_SYNTH` sebagai fitur final untuk training synthetic.

Target dan kolom raw income yang dilarang masuk fitur:
- `next_week_income`
- `next_week_income_norm`
- `next_week_direction`
- `monthly_income`
- `avg_weekly_income`
- `income_std_4w`
- `income_cv_4w`
- `income_range_4w`
- `income_w1`
- `income_w2`
- `income_w3`
- `income_w4`
- `synthetic_weekly_income`

Normalisasi:
- Target: `log1p → MinMaxScaler`, fit hanya pada train.
- Feature scaler: `RobustScaler`, fit hanya pada train.

Output:
- `outputs/preprocessors/weekly_target_scaler.pkl`
- `outputs/preprocessors/weekly_feature_scaler.pkl`

### BAGIAN 13 — Evaluasi Helper Functions

Notebook membuat helper evaluasi:
- regresi: MAE, RMSE, MAPE, R2, Within30%;
- klasifikasi: Accuracy, Macro-F1, precision/recall per kelas;
- rule-based momentum baseline.

### BAGIAN 14 — Model Training

Training utama dilakukan pada synthetic 52w.

Model regresi:
- Baseline Last Week
- Baseline Rolling Mean
- Ridge
- Random Forest
- XGBoost jika tersedia

Model klasifikasi:
- Baseline Majority
- Rule-based Momentum
- Random Forest
- XGBoost jika tersedia

Output:
- `outputs/model_results/synthetic_52w_regression_results.csv`
- `outputs/model_results/synthetic_52w_classification_results.csv`
- `outputs/model_results/feature_importance_weekly.csv`
- `outputs/charts/actual_vs_predicted.png`
- `outputs/model_results/real_4w_regression_results.csv`

### BAGIAN 15 — Synthetic Quality Validation

Notebook membandingkan distribusi real survey vs synthetic:
- mean;
- median;
- std;
- CV;
- min;
- max;
- autocorrelation lag-1;
- median income per `gig_type`;
- proporsi `Up`, `Stable`, `Down`.

Output:
- `outputs/dashboard/synthetic_quality_summary.csv`
- `outputs/charts/synthetic_vs_real_income_distribution.png`
- `outputs/charts/synthetic_gig_type_monthly_trend.png`

### BAGIAN 16 — A/B Testing Simulasi

Notebook membuat simulasi offline A/B testing untuk melihat efek treatment terhadap `budget_readiness_score`.

Output:
- `outputs/dashboard/ab_testing_summary.csv`
- `outputs/charts/ab_testing_result.png`

Catatan:
- Ini simulasi offline karena aplikasi Fingo belum live.
- Tidak boleh diklaim sebagai hasil eksperimen real user.

### BAGIAN 17 — Dashboard CSV Files

Notebook menghasilkan file dashboard untuk Streamlit.

| File | Isi |
| --- | --- |
| outputs/dashboard/gig_type_distribution.csv | Distribusi 8 jenis pekerjaan dari real survey. |
| outputs/dashboard/real_4w_income_summary.csv | Ringkasan pendapatan real 4w per gig_type. |
| outputs/dashboard/synthetic_52w_income_summary.csv | Ringkasan pendapatan synthetic 52w per gig_type. |
| outputs/dashboard/synthetic_monthly_trend_summary.csv | Tren pendapatan synthetic per bulan dan gig_type. |
| outputs/dashboard/synthetic_seasonal_event_summary.csv | Ringkasan pendapatan synthetic berdasarkan seasonal event. |
| outputs/dashboard/dataset_comparison_summary.csv | Perbandingan dataset real survey vs synthetic training. |
| outputs/dashboard/model_performance_summary.csv | Gabungan hasil performa model. |
| outputs/dashboard/direction_threshold_summary.csv | Perbandingan distribusi Up/Stable/Down untuk beberapa threshold. |
| outputs/dashboard/seasonal_event_income_summary.csv | Rata-rata preferensi seasonal event per gig_type dari real survey. |
| outputs/dashboard/synthetic_quality_summary.csv | Metrik quality check synthetic vs real survey. |
| outputs/dashboard/ab_testing_summary.csv | Hasil simulasi offline A/B testing. |
| outputs/dashboard/streamlit_data_readme.md | README untuk data dashboard Streamlit. |

### BAGIAN 18 — Data Dictionary

Notebook menghasilkan data dictionary dalam format CSV.

Output:
- `outputs/reports/data_dictionary.csv`
- `outputs/dashboard/data_dictionary.csv`

### BAGIAN 19 — Model Contract untuk AI Engineer

Notebook menghasilkan kontrak model agar AI Engineer tahu:
- urutan fitur final;
- target regresi dan klasifikasi;
- forbidden leakage columns;
- aturan split;
- aturan normalisasi;
- aturan threshold direction;
- file scaler yang harus dipakai.

Output wajib:
- `outputs/model_contract/final_weekly_features.json`
- `outputs/model_contract/target_contract.json`
- `outputs/model_contract/leakage_rules.md`

### BAGIAN 20 — Technical Report

Notebook membuat laporan teknis final berisi:
- narasi dataset;
- key design decisions;
- data sources;
- best model;
- kualitas synthetic;
- disclaimer.

Output:
- `outputs/reports/technical_report.md`

### BAGIAN 21 — Final Validation Checklist

Notebook melakukan checklist akhir seperti:
- file penting berhasil dibuat;
- anti-leakage aman;
- split benar;
- synthetic rows sesuai;
- kontrak model tersedia;
- output dashboard tersedia.

### BAGIAN 22 — Ringkasan Output & Push ke GitHub

Notebook menampilkan ringkasan semua output file, lalu melakukan commit dan push ke GitHub branch yang ditentukan.

## 4. Ringkasan Output Utama

| File | Deskripsi | Dipakai Untuk |
| --- | --- | --- |
| data/processed/cleaned_survey_data.csv | Dataset survei bersih 384 responden setelah rename, drop PII, encoding, feature engineering dasar, dan merge benchmark BPS. | DS / Dashboard / referensi synthetic |
| data/processed/weekly_forecasting_dataset_real_4w.csv | Dataset real 4 minggu dari survei. Dipakai sebagai sanity check/benchmark, bukan training utama. | Sanity check |
| data/processed/real_4w_train.csv | Split train real 4w berbasis respondent_id. | Sanity check |
| data/processed/real_4w_test.csv | Split test real 4w berbasis respondent_id. | Sanity check |
| data/synthetic/synthetic_52week_user_income.csv | Raw synthetic longitudinal dataset: 3.000 synthetic users × 52 minggu. | Sumber sliding window |
| data/synthetic/synthetic_52week_weekly_forecasting_dataset.csv | Dataset forecasting synthetic hasil sliding window 4-lag untuk prediksi next_week_income dan next_week_direction. | Training utama AI Engineer |
| data/synthetic/synthetic_52w_train.csv | Train set synthetic, split by synthetic_user_id. | Training utama AI Engineer |
| data/synthetic/synthetic_52w_test.csv | Test set synthetic, split by synthetic_user_id. | Evaluasi utama AI Engineer |
| outputs/preprocessors/weekly_target_scaler.pkl | MinMaxScaler untuk target setelah transformasi log1p; fit hanya pada train. | Inference / inverse transform |
| outputs/preprocessors/weekly_feature_scaler.pkl | RobustScaler untuk fitur; fit hanya pada train. | Inference preprocessing |
| outputs/preprocessors/gig_label_encoder.pkl | LabelEncoder untuk gig_type. | Encoding pendukung |
| outputs/preprocessors/dom_label_encoder.pkl | LabelEncoder untuk domisili_code. | Encoding pendukung |
| outputs/preprocessors/direction_label_encoder.pkl | LabelEncoder untuk previous_direction pada real sanity dataset. | Encoding pendukung |
| outputs/model_results/synthetic_52w_regression_results.csv | Hasil benchmark model regresi pada synthetic 52w. | Referensi performa |
| outputs/model_results/synthetic_52w_classification_results.csv | Hasil benchmark model klasifikasi arah pendapatan. | Referensi performa |
| outputs/model_results/real_4w_regression_results.csv | Hasil sanity check model pada real 4w. | Referensi sanity check |
| outputs/model_results/feature_importance_weekly.csv | Feature importance model terbaik untuk weekly forecasting. | Interpretasi model |
| outputs/dashboard/synthetic_quality_summary.csv | Validasi distribusi synthetic vs real survey. | Dashboard / validasi |
| outputs/dashboard/model_performance_summary.csv | Ringkasan performa model dari synthetic dan real sanity check. | Dashboard |
| outputs/dashboard/ab_testing_summary.csv | Ringkasan simulasi A/B testing offline. | Dashboard / experiment simulation |
| outputs/model_contract/final_weekly_features.json | Kontrak fitur final: feature order, forbidden leakage, split rule, dan metadata training. | Wajib untuk AI Engineer |
| outputs/model_contract/target_contract.json | Kontrak target regresi dan klasifikasi, threshold direction, scaler target, dan target performa. | Wajib untuk AI Engineer |
| outputs/model_contract/leakage_rules.md | Aturan anti-leakage dan urutan income. | Wajib untuk AI Engineer |
| outputs/reports/technical_report.md | Laporan teknis final v13. | Dokumentasi |
| outputs/reports/data_dictionary.csv | Data dictionary versi CSV. | Dokumentasi |
| outputs/dashboard/data_dictionary.csv | Data dictionary yang dapat dibaca dashboard. | Dashboard |

## 5. Aturan Teknis Paling Penting

### 5.1 Income Ordering

Urutan income wajib dipahami seperti ini:

```text
income_w4 = pendapatan 4 minggu lalu / terlama
income_w3 = pendapatan 3 minggu lalu
income_w2 = pendapatan 2 minggu lalu
income_w1 = pendapatan minggu lalu / terbaru
```

Urutan kronologis:

```text
income_w4 → income_w3 → income_w2 → income_w1
```

### 5.2 Target

| Target | Tipe | Deskripsi |
|---|---|---|
| `next_week_income` | Regresi | Pendapatan minggu berikutnya. |
| `next_week_direction` | Klasifikasi | Arah pendapatan minggu berikutnya: `Up`, `Stable`, atau `Down`. |

### 5.3 Direction Threshold

```text
Up     = jika pct_change >= 0.10
Down   = jika pct_change <= -0.10
Stable = selain itu
```

### 5.4 Split Rule

Split wajib berdasarkan user:

```text
split by synthetic_user_id
```

Jangan split random row karena akan membuat data leakage antar window milik user yang sama.

### 5.5 Normalisasi

Target menggunakan:

```text
log1p(next_week_income) → MinMaxScaler
```

Scaler hanya fit pada train set.

### 5.6 Disclaimer Dataset

- Survey real 384 responden bukan training utama.
- Synthetic 52w adalah training utama.
- Real 4w hanya sanity check.
- Performa synthetic tidak boleh langsung diklaim sebagai performa dunia nyata sebelum ada validasi live.
