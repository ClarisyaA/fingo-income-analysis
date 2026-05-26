# Fingo — Weekly Income Forecasting Pipeline

> End-to-end data science pipeline untuk fitur **Income Predictor** pada aplikasi Fingo. Pipeline ini membersihkan data survei gig worker, membangun synthetic longitudinal dataset 52 minggu, membuat dataset forecasting mingguan, melatih baseline model, memvalidasi kualitas data, dan menghasilkan **model contract** yang siap digunakan oleh AI Engineer.

**Program:** Coding Camp 2026 × DBS Foundation  
**Tim:** CC26-PSU217  
**Role:** Data Scientist 2 — Clarisya Adeline  
**Downstream consumer:** AI Engineer — Weekly Income Forecasting Model  
**Versi pipeline:** `v13-FINAL`

---

## Daftar Isi

1. [Konteks Proyek](#1-konteks-proyek)
2. [Tujuan Pipeline](#2-tujuan-pipeline)
3. [Ringkasan Hasil Akhir](#3-ringkasan-hasil-akhir)
4. [Sumber Data](#4-sumber-data)
5. [Struktur Repository](#5-struktur-repository)
6. [Alur Notebook](#6-alur-notebook)
7. [Output Utama untuk AI Engineer](#7-output-utama-untuk-ai-engineer)
8. [Kontrak Fitur dan Target](#8-kontrak-fitur-dan-target)
9. [Validasi Kualitas dan Anti-Leakage](#9-validasi-kualitas-dan-anti-leakage)
10. [Hasil Baseline Modeling](#10-hasil-baseline-modeling)
11. [Dashboard dan Report](#11-dashboard-dan-report)
12. [Setup dan Cara Menjalankan](#12-setup-dan-cara-menjalankan)
13. [Catatan Penting untuk Development Lanjutan](#13-catatan-penting-untuk-development-lanjutan)
14. [Dokumentasi Tambahan](#14-dokumentasi-tambahan)
15. [Tim dan Lisensi](#15-tim-dan-lisensi)

---

## 1. Konteks Proyek

**Fingo** adalah aplikasi finansial untuk membantu pekerja gig/informal Indonesia mengelola pendapatan yang tidak stabil. Salah satu fitur utamanya adalah **Income Predictor**, yaitu fitur yang memprediksi pendapatan minggu berikutnya berdasarkan pola pendapatan beberapa minggu terakhir, karakteristik pekerjaan, kalender, preferensi musiman, dan profil pengguna.

Masalah utama dalam pengembangan fitur ini adalah keterbatasan dataset publik yang secara spesifik memuat pendapatan mingguan pekerja gig Indonesia selama 1 tahun. Oleh karena itu, pipeline ini menggunakan pendekatan:

1. **Data survei real** sebagai baseline empiris.
2. **Data BPS** sebagai benchmark pendapatan regional.
3. **Synthetic longitudinal generation** untuk membentuk data 52 minggu per user.
4. **Forecasting dataset** berbasis sliding window 4 minggu.
5. **Model contract** agar output Data Scientist bisa langsung dipakai oleh AI Engineer.

---

## 2. Tujuan Pipeline

Pipeline pada `Notebook_Income.ipynb` dibuat untuk:

- Membersihkan dan menstandarkan data survei real gig worker.
- Menjaga mapping jawaban form agar konsisten dengan opsi Google Form.
- Menghasilkan dataset synthetic sebanyak **3.000 user × 52 minggu**.
- Membentuk dataset forecasting mingguan dengan input 4 minggu terakhir.
- Menyediakan train/test split yang aman dari data leakage.
- Melatih baseline model regresi dan klasifikasi.
- Menghasilkan file kontrak fitur, target, scaler, encoder, dan leakage rules.
- Menyediakan file dashboard/report untuk eksplorasi dan presentasi.

---

## 3. Ringkasan Hasil Akhir

| Komponen | Hasil |
|---|---:|
| Survey real bersih | 384 responden |
| Synthetic raw users | 3.000 user |
| Synthetic raw weekly rows | 156.000 rows |
| Synthetic forecasting rows | 144.000 rows |
| Train split | 2.400 users / 115.200 rows |
| Test split | 600 users / 28.800 rows |
| Forecasting window | 4 minggu historis → prediksi minggu berikutnya |
| Regression target | `next_week_income` |
| Classification target | `next_week_direction` |
| Direction classes | `Down`, `Stable`, `Up` |
| Direction threshold | 10% |
| Split strategy | By `synthetic_user_id`, bukan random rows |
| Normalisasi target | `log1p` → `MinMaxScaler`, fit on train only |
| Feature scaling | `RobustScaler`, fit on train only |
| Final validation checklist | 17/17 PASS |

---

## 4. Sumber Data

### 4.1 Data Primer

| File | Keterangan |
|---|---|
| `data/raw/form_responses.csv` | Data Google Form dari 384 responden setelah proses cleaning. Digunakan sebagai baseline distribusi karakteristik user. |

### 4.2 Data Sekunder

| Sumber | Kegunaan |
|---|---|
| BPS 2023–2025 | Benchmark pendapatan regional, terutama untuk fitur `bps_jasa_weekly`. |
| Data referensi pekerjaan gig/informal | Membantu sanity check terhadap range pendapatan dan pola pekerjaan. |

### 4.3 Peran Data Survey

Data survey **bukan dataset training utama** karena hanya memiliki histori 4 minggu. Perannya adalah sebagai:

- Distribusi acuan untuk sampling synthetic users.
- Baseline karakteristik gig type, domisili, umur, pengalaman, jam kerja, dan preferensi musiman.
- Sanity check terhadap synthetic data.
- Dataset validasi ringan untuk memastikan model tidak hanya masuk akal pada synthetic data.

---

## 5. Struktur Repository

```text
fingo-income-analysis/
├── Notebook_Income.ipynb
├── notebook.md
├── data_dictionary.md
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/
│   │   └── form_responses.csv
│   │
│   ├── processed/
│   │   ├── cleaned_survey_data.csv
│   │   ├── weekly_forecasting_dataset_real_4w.csv
│   │   ├── real_4w_train.csv
│   │   └── real_4w_test.csv
│   │
│   └── synthetic/
│       ├── synthetic_52week_user_income.csv
│       ├── synthetic_52week_weekly_forecasting_dataset.csv
│       ├── synthetic_52w_train.csv
│       └── synthetic_52w_test.csv
│
├── outputs/
│   ├── dashboard/
│   │   ├── synthetic_quality_summary.csv
│   │   ├── model_performance_summary.csv
│   │   ├── real_4w_income_summary.csv
│   │   ├── synthetic_52w_income_summary.csv
│   │   ├── synthetic_monthly_trend_summary.csv
│   │   ├── synthetic_seasonal_event_summary.csv
│   │   ├── dataset_comparison_summary.csv
│   │   ├── direction_threshold_summary.csv
│   │   ├── seasonal_event_income_summary.csv
│   │   ├── gig_type_distribution.csv
│   │   └── data_dictionary.csv
│   │
│   ├── model_contract/
│   │   ├── final_weekly_features.json
│   │   ├── target_contract.json
│   │   └── leakage_rules.md
│   │
│   ├── model_results/
│   │   ├── synthetic_52w_regression_results.csv
│   │   ├── synthetic_52w_classification_results.csv
│   │   ├── real_4w_regression_results.csv
│   │   └── feature_importance_weekly.csv
│   │
│   ├── preprocessors/
│   │   ├── weekly_target_scaler.pkl
│   │   ├── weekly_feature_scaler.pkl
│   │   ├── gig_label_encoder.pkl
│   │   ├── dom_label_encoder.pkl
│   │   └── direction_label_encoder.pkl
│   │
│   └── reports/
│       ├── data_assessing_summary.csv
│       ├── data_dictionary.csv
│       ├── form_column_mapping.json
│       └── technical_report.md
```

---

## 6. Alur Notebook

Detail lengkap tersedia di [`notebook.md`](notebook.md). Ringkasannya:

| Bagian | Proses | Output |
|---:|---|---|
| 0 | Setup repo, folder, library, helper functions | Struktur folder siap pakai |
| 1 | Problem discovery | Definisi masalah dan solusi |
| 2 | Business questions | Arah analisis dan validasi |
| 3 | Data gathering | Load survey dan BPS |
| 3.5 | Form response mapping | Mapping kolom dan opsi Google Form |
| 4 | Data assessing | Ringkasan kualitas data |
| 5 | Data cleaning | Survey bersih tanpa PII |
| 6 | EDA survey asli | Distribusi gig type, domisili, income |
| 7 | Survey distribution profiling | Baseline synthetic generation |
| 8 | Real 4-week sanity dataset | Dataset real 4 minggu |
| 9 | Generate synthetic users | 3.000 user × 52 minggu |
| 10 | Generate weekly forecasting dataset | 144.000 forecasting rows |
| 11 | Train/test split by user | Train 2.400 user, test 600 user |
| 12 | Feature engineering + anti-leakage | Final feature columns |
| 13 | Evaluation helper functions | Fungsi evaluasi regresi/klasifikasi |
| 14 | Baseline model training | Model results CSV |
| 15 | Synthetic quality validation | Validasi synthetic vs real |
| 16 | A/B testing simulation | Simulasi treatment impact |
| 17 | Dashboard CSV files | File ringkasan dashboard |
| 18 | Data dictionary | Schema output |
| 19 | Model contract | Kontrak AI Engineer |
| 20 | Technical report | Report akhir |
| 21 | Final validation checklist | 17/17 PASS |
| 22 | Output summary + GitHub push | Ringkasan file final |

---

## 7. Output Utama untuk AI Engineer

AI Engineer sebaiknya memulai dari file berikut.

| Prioritas | File | Fungsi |
|---|---|---|
| Wajib | `data/synthetic/synthetic_52w_train.csv` | Dataset training utama untuk model forecasting. |
| Wajib | `data/synthetic/synthetic_52w_test.csv` | Dataset evaluasi final. |
| Wajib | `outputs/model_contract/final_weekly_features.json` | Urutan fitur final yang harus dipakai model. |
| Wajib | `outputs/model_contract/target_contract.json` | Definisi target regresi, target klasifikasi, threshold, dan ekspektasi metrik. |
| Wajib | `outputs/model_contract/leakage_rules.md` | Aturan kolom yang tidak boleh masuk fitur. |
| Wajib | `outputs/preprocessors/weekly_target_scaler.pkl` | Scaler target untuk transformasi `log1p` → `MinMaxScaler`. |
| Wajib | `outputs/preprocessors/weekly_feature_scaler.pkl` | Scaler fitur untuk preprocessing inference/training lanjutan. |
| Opsional | `data/synthetic/synthetic_52week_weekly_forecasting_dataset.csv` | Full synthetic forecasting dataset sebelum split. |
| Opsional | `data/processed/weekly_forecasting_dataset_real_4w.csv` | Real 4-week dataset untuk sanity check, bukan training utama. |
| Opsional | `outputs/model_results/*.csv` | Referensi baseline model. |
| Opsional | `outputs/dashboard/*.csv` | Data ringkasan untuk dashboard dan presentasi. |

Detail kolom dan isi output tersedia di [`data_dictionary.md`](data_dictionary.md).

---

## 8. Kontrak Fitur dan Target

### 8.1 Target Regresi

```text
next_week_income
```

Target ini berisi nominal pendapatan minggu berikutnya dalam rupiah.

### 8.2 Target Klasifikasi

```text
next_week_direction
```

Kelas target:

| Class | Definisi |
|---|---|
| `Up` | Pendapatan naik minimal 10% dibanding minggu sebelumnya. |
| `Down` | Pendapatan turun minimal 10% dibanding minggu sebelumnya. |
| `Stable` | Perubahan berada di antara -10% sampai +10%. |

Aturan threshold:

```text
Up     jika pct_change >=  0.10
Down   jika pct_change <= -0.10
Stable otherwise
```

### 8.3 Urutan Income

Urutan historis income harus dibaca sebagai berikut:

```text
income_w4 → income_w3 → income_w2 → income_w1 → next_week_income
```

Keterangan:

- `income_w4` = pendapatan paling lama, 4 minggu lalu.
- `income_w1` = pendapatan terbaru, minggu lalu.
- `next_week_income` = pendapatan yang ingin diprediksi.

### 8.4 Fitur Final

Urutan fitur final **jangan ditulis manual di kode model**. AI Engineer harus membaca dari:

```text
outputs/model_contract/final_weekly_features.json
```

Gunakan key:

```json
feature_order_synthetic
```

### 8.5 Kolom yang Dilarang Masuk Feature

Kolom berikut tidak boleh masuk sebagai input model karena menyebabkan leakage:

```text
next_week_income
next_week_income_norm
next_week_direction
monthly_income
avg_weekly_income
income_std_4w
income_cv_4w
income_range_4w
income_w1
income_w2
income_w3
income_w4
synthetic_weekly_income
```

---

## 9. Validasi Kualitas dan Anti-Leakage

Pipeline ini memiliki checklist validasi akhir dengan hasil:

```text
17/17 PASSED
```

Validasi utama:

| Validasi | Status |
|---|---|
| Survey dimuat 384 responden | PASS |
| 8 gig type preserved | PASS |
| Direction threshold 10% | PASS |
| Income sequence w4 → w1 benar | PASS |
| Synthetic 3.000 users generated | PASS |
| 52 minggu per user | PASS |
| Synthetic autocorrelation > 0.3 | PASS |
| Anti-leakage synthetic | PASS |
| Anti-leakage real | PASS |
| Split by user, bukan random row | PASS |
| Scaler fit on train only | PASS |
| Feature contract saved | PASS |
| Technical report saved | PASS |

Catatan penting:

- Split dilakukan berdasarkan `synthetic_user_id`, bukan random rows.
- Scaler hanya di-fit pada train set.
- Survey real digunakan sebagai baseline/sanity check, bukan training utama.
- Synthetic data dibuat dengan AR(1), shock, seasonal effect, dan variasi per gig type agar tidak terlalu smooth.

---

## 10. Hasil Baseline Modeling

### 10.1 Regression — Synthetic 52w

| Model | MAE | RMSE | MAPE (%) | R² | Within 30% |
|---|---:|---:|---:|---:|---:|
| Baseline Last Week | 61,269.82 | 134,376.69 | 89.49 | 0.8033 | 83.04 |
| Baseline Rolling Mean | 75,421.62 | 146,231.32 | 91.97 | 0.7671 | 78.99 |
| Ridge | 55,217.82 | 123,803.89 | 88.28 | 0.8331 | 87.91 |
| Random Forest | 53,313.63 | 124,139.65 | 86.57 | 0.8322 | 89.15 |
| XGBoost | 53,050.14 | 124,097.90 | 82.64 | 0.8323 | 89.15 |

Interpretasi:

- **XGBoost** memiliki MAE terbaik.
- **Ridge** memiliki R² sedikit tertinggi.
- **Within30% sekitar 89%** menunjukkan mayoritas prediksi berada dalam toleransi ±30%.
- MAPE terlihat tinggi karena sebagian target mingguan bernilai sangat kecil/near-zero, sehingga persentase error menjadi sensitif. Untuk evaluasi lanjutan, gunakan kombinasi MAE, RMSE, R², Within30%, dan normalized MAE.

### 10.2 Classification — Synthetic 52w

| Model | Accuracy | Macro F1 | Precision | Recall |
|---|---:|---:|---:|---:|
| Baseline Majority | 63.21 | 25.82 | 21.07 | 33.33 |
| Rule-based Momentum | 65.24 | 48.80 | 48.83 | 48.78 |
| Random Forest | 79.04 | 63.23 | 75.63 | 60.67 |
| XGBoost | 79.02 | 63.34 | 74.97 | 60.73 |

Interpretasi:

- Model tree-based jauh lebih baik daripada baseline majority.
- Random Forest unggul tipis pada accuracy.
- XGBoost unggul tipis pada Macro F1.
- Target realistis untuk klasifikasi awal: **60–75% accuracy** sudah cukup baik; hasil baseline sudah melewati target tersebut.

---

## 11. Dashboard dan Report

Output dashboard tersedia di:

```text
outputs/dashboard/
```

File penting:

| File | Fungsi |
|---|---|
| `real_4w_income_summary.csv` | Ringkasan income dari survey real. |
| `synthetic_52w_income_summary.csv` | Ringkasan income synthetic 52 minggu. |
| `synthetic_monthly_trend_summary.csv` | Trend pendapatan bulanan. |
| `synthetic_seasonal_event_summary.csv` | Ringkasan income saat event musiman. |
| `dataset_comparison_summary.csv` | Perbandingan real vs synthetic. |
| `model_performance_summary.csv` | Ringkasan performa model. |
| `synthetic_quality_summary.csv` | Validasi kualitas synthetic data. |

Technical report tersedia di:

```text
outputs/reports/technical_report.md
```

---

## 12. Setup dan Cara Menjalankan

### 12.1 Clone Repository

```bash
git clone https://github.com/ClarisyaA/fingo-income-analysis.git
cd fingo-income-analysis
```

### 12.2 Buat Virtual Environment

```bash
python -m venv .venv
```

Aktivasi:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 12.3 Install Dependency

```bash
pip install -r requirements.txt
```

### 12.4 Jalankan Notebook

```bash
jupyter notebook Notebook_Income.ipynb
```

Jalankan seluruh cell dari awal sampai akhir.

Output akan tersimpan ke:

```text
data/processed/
data/synthetic/
outputs/dashboard/
outputs/model_results/
outputs/model_contract/
outputs/preprocessors/
outputs/reports/
```

---

## 13. Catatan Penting untuk Development Lanjutan

### Untuk AI Engineer

- Jangan hardcode urutan fitur. Ambil dari `final_weekly_features.json`.
- Jangan memasukkan kolom target atau income raw yang dilarang ke dalam input model.
- Gunakan split by user agar tidak ada user yang sama muncul di train dan test.
- Gunakan scaler yang sudah disimpan jika ingin menjaga konsistensi preprocessing.
- Gunakan `synthetic_52w_train.csv` dan `synthetic_52w_test.csv` sebagai dataset utama.
- Gunakan real 4-week dataset hanya untuk sanity check, bukan training utama.

### Untuk Data Scientist

- Jika menambah data survey baru, jalankan ulang cleaning dan distribution profiling.
- Jika mengubah threshold direction, update juga `target_contract.json` dan `leakage_rules.md`.
- Jika mengubah feature engineering, update `final_weekly_features.json` dan `data_dictionary.md`.
- Jika synthetic generation diubah, lakukan ulang validasi quality dan checklist akhir.

### Untuk Backend / Product

- Prediksi bulanan dapat dibuat dari akumulasi 4 prediksi mingguan.
- Output model bisa dipakai untuk menampilkan insight seperti:
  - estimasi pendapatan minggu depan;
  - arah pendapatan: naik/stabil/turun;
  - risiko volatilitas pendapatan;
  - rekomendasi budgeting adaptif.

---

## 14. Dokumentasi Tambahan

| Dokumen | Isi |
|---|---|
| [`notebook.md`](notebook.md) | Alur lengkap proses yang dilakukan di notebook. |
| [`data_dictionary.md`](data_dictionary.md) | Data dictionary dan daftar output untuk AI Engineer. |
| `outputs/reports/technical_report.md` | Technical report hasil pipeline. |
| `outputs/model_contract/leakage_rules.md` | Aturan anti-leakage. |
| `outputs/model_contract/target_contract.json` | Kontrak target regresi dan klasifikasi. |
| `outputs/model_contract/final_weekly_features.json` | Kontrak fitur final. |

---

## 15. Tim dan Lisensi

**Capstone:** Coding Camp 2026 × DBS Foundation  
**Tim:** CC26-PSU217  
**Data Scientist 2:** Clarisya Adeline  
**Repository:** `fingo-income-analysis`

Dataset real survey digunakan untuk kebutuhan akademik/capstone. Dataset synthetic dan kode pipeline digunakan untuk pengembangan fitur Fingo serta dokumentasi teknis tim.

---

## Status Akhir

Pipeline sudah menghasilkan seluruh output utama yang dibutuhkan AI Engineer:

- Dataset train/test synthetic.
- Dataset real 4-week untuk sanity check.
- Scaler dan encoder.
- Model results.
- Dashboard CSV.
- Technical report.
- Feature contract.
- Target contract.
- Leakage rules.
- Data dictionary.
- Notebook process documentation.

**Final validation:** `17/17 PASSED`.
