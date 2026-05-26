# Data Dictionary — Fingo Weekly Income Forecasting

Dokumen ini menjelaskan isian output data yang dipakai oleh AI Engineer dari `Notebook_Income.ipynb`.

## 1. Output yang Wajib Digunakan AI Engineer

| File | Kegunaan |
| --- | --- |
| data/synthetic/synthetic_52week_weekly_forecasting_dataset.csv | Dataset full synthetic untuk eksperimen tambahan atau retraining ulang. |
| data/synthetic/synthetic_52w_train.csv | Train set utama. Pakai untuk fitting model. |
| data/synthetic/synthetic_52w_test.csv | Test set utama. Pakai untuk evaluasi final. |
| outputs/model_contract/final_weekly_features.json | Sumber paling penting untuk urutan fitur final `feature_order_synthetic`. |
| outputs/model_contract/target_contract.json | Kontrak target, kelas direction, threshold, scaler target, dan ekspektasi metrik. |
| outputs/model_contract/leakage_rules.md | Aturan kolom yang tidak boleh masuk fitur. |
| outputs/preprocessors/weekly_target_scaler.pkl | Scaler target untuk transformasi log1p + MinMaxScaler. |
| outputs/preprocessors/weekly_feature_scaler.pkl | Feature scaler jika inference pipeline ingin mengikuti preprocessing notebook. |
| outputs/preprocessors/gig_label_encoder.pkl | Encoder pendukung untuk `gig_type`. |
| outputs/preprocessors/dom_label_encoder.pkl | Encoder pendukung untuk `domisili_code`. |
| outputs/model_results/synthetic_52w_regression_results.csv | Benchmark model regresi dari notebook. |
| outputs/model_results/synthetic_52w_classification_results.csv | Benchmark model klasifikasi dari notebook. |
| outputs/model_results/feature_importance_weekly.csv | Referensi fitur paling berpengaruh. |

## 2. Dataset Utama untuk AI Engineer

Dataset utama untuk training adalah:

```text
data/synthetic/synthetic_52w_train.csv
data/synthetic/synthetic_52w_test.csv
```

Dataset full untuk eksplorasi/retraining:

```text
data/synthetic/synthetic_52week_weekly_forecasting_dataset.csv
```

Dataset ini berasal dari synthetic longitudinal data 52 minggu yang diubah menjadi supervised forecasting dataset dengan sliding window 4 minggu.

Skema dasarnya:

```text
lag_4_income, lag_3_income, lag_2_income, lag_1_income + fitur profil/kalendar/preferensi
→ next_week_income
→ next_week_direction
```

## 3. Target yang Diprediksi

| Kolom | Tipe | Role | Deskripsi | Catatan |
| --- | --- | --- | --- | --- |
| next_week_income | float64 | Target regresi utama | Pendapatan minggu berikutnya yang diprediksi dari 4 minggu history sebelumnya. | Jangan masuk fitur. |
| next_week_direction | string | Target klasifikasi utama | Kelas arah pendapatan minggu berikutnya: `Up`, `Stable`, `Down`. | Jangan masuk fitur. |

Aturan `next_week_direction`:

```text
Up     = jika perubahan income >= +10%
Down   = jika perubahan income <= -10%
Stable = selain itu
```

## 4. Final Feature Columns untuk Synthetic Training

Jumlah fitur final synthetic berdasarkan notebook adalah **54 fitur** sebelum filtering berdasarkan keberadaan kolom di dataframe.

### Lag features

- `lag_1_income`
- `lag_2_income`
- `lag_3_income`
- `lag_4_income`
### Rolling statistics

- `rolling_mean_4w`
- `rolling_std_4w`
- `rolling_min_4w`
- `rolling_max_4w`
- `rolling_range_4w`
- `rolling_cv_4w`
- `rolling_median_4w`
- `rolling_last_vs_median_pct`
### Trend & change features

- `income_trend_4w_abs`
- `income_trend_4w_pct`
- `last_income_change_abs`
- `last_income_change_pct`
- `trend_slope_4w`
### Previous direction features

- `is_previous_week_up`
- `is_previous_week_down`
- `is_previous_week_stable`
### Ratio/volatility features

- `lag_ratio_1_to_mean`
- `volatility_ratio`
### Calendar/seasonal target-week features

- `target_month`
- `target_week_of_month`
- `target_quarter`
- `target_is_month_start`
- `target_is_month_end`
- `target_is_payday_period`
- `target_is_weekend`
- `target_is_ramadan_lebaran`
- `target_is_harbolnas`
- `target_is_christmas_year_end`
- `target_is_new_year`
### Profile features

- `usia`
- `experience_months_log`
- `hari_kerja_per_minggu`
- `jam_kerja_per_hari`
- `total_jam_seminggu`
- `bps_jasa_weekly`
### Preference features

- `pref_awal_bulan`
- `pref_payday`
- `pref_weekend`
- `pref_ramadan_lebaran`
- `pref_natal_tahun_baru`
- `pref_harbolnas`
- `pref_promo_aplikasi`
### Gig type one-hot features

- `gig_ojek_online`
- `gig_kurir`
- `gig_jualan_online`
- `gig_freelance_desain`
- `gig_freelance_it`
- `gig_content_creator`
- `gig_tutor`
- `gig_pekerja_harian`

## 5. Feature Order Wajib

AI Engineer sebaiknya tidak menulis ulang daftar fitur secara manual. Gunakan:

```text
outputs/model_contract/final_weekly_features.json
```

Field yang wajib dibaca:

```json
{
  "feature_order_synthetic": [...],
  "forbidden_leakage_cols": [...],
  "split_rule": "Split by synthetic_user_id (not random rows)",
  "normalization": "log1p -> MinMaxScaler (fit on train only)"
}
```

## 6. Kolom yang Dilarang Masuk Fitur

Kolom berikut tidak boleh dimasukkan ke `X` karena berisiko leakage atau merupakan target langsung.

| Kolom | Alasan |
| --- | --- |
| next_week_income | Target regresi |
| next_week_income_norm | Target hasil normalisasi |
| next_week_direction | Target klasifikasi |
| monthly_income | Agregasi income aktual, berpotensi bocor |
| avg_weekly_income | Statistik dari income aktual survei |
| income_std_4w | Statistik dari income aktual survei |
| income_cv_4w | Statistik dari income aktual survei |
| income_range_4w | Statistik dari income aktual survei |
| income_w1 | Raw survey income, harus diubah menjadi lag feature |
| income_w2 | Raw survey income, harus diubah menjadi lag feature |
| income_w3 | Raw survey income, harus diubah menjadi lag feature |
| income_w4 | Raw survey income, harus diubah menjadi lag feature |
| synthetic_weekly_income | Observed synthetic income raw, bukan input langsung |

## 7. Data Dictionary Kolom Penting

| column_name | data_type | description | source | example_value | used_for_eda | used_for_modeling | leakage_risk | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| synthetic_user_id | string | ID unik synthetic user | Generated | SYN_000001 | No | Yes | Low | 3.000 unique users |
| source_respondent_id | string | ID responden survey asli yang jadi template | Generated | R0000 | No | No | Low | Reference saja |
| dataset_type | string | real_4w atau synthetic_52w | Generated | synthetic_52w | Yes | Yes | Low |  |
| usia | int64 | Usia responden/user | Survei col 2 | 17–65 | Yes | Yes | Low | Clipped [17,65], dengan variasi +/-3 untuk synthetic |
| gig_type | string | 8 kategori jenis pekerjaan gig | Survei col 4 | ojek_online... | Yes | Yes | Low | 8 kategori dari GIG_MAP |
| domisili_code | string | Kode domisili | Survei col 3 | jabodetabek... | Yes | Yes | Low | Map DOMISILI_MAP |
| income_w1 | float64 | Pendapatan MINGGU LALU (terbaru) | Survei col 10 | 0–2jt | Yes | Lag source only | High | Jangan langsung masuk X |
| income_w2 | float64 | Pendapatan DUA MINGGU LALU | Survei col 11 | 0–2jt | Yes | Lag source only | High | Jangan langsung masuk X |
| income_w3 | float64 | Pendapatan TIGA MINGGU LALU | Survei col 12 | 0–2jt | Yes | Lag source only | High | Jangan langsung masuk X |
| income_w4 | float64 | Pendapatan EMPAT MINGGU LALU (terlama) | Survei col 13 | 0–2jt | Yes | Lag source only | High | Jangan langsung masuk X — urutan: w4(terlama)→w1(terbaru) |
| next_week_income | float64 | TARGET: pendapatan minggu depan | Engineered | 0–2jt | No | Target only | High | JANGAN masuk X |
| next_week_direction | string | TARGET: Up/Stable/Down (threshold 10%, >= <=) | Engineered | Up/Stable/Down | No | Target only | High | JANGAN masuk X |
| lag_1_income | float64 | Income lag 1 minggu (dari sequence kronologis) | Engineered | 0–2jt | No | Yes | Low | Fitur utama |
| lag_2_income | float64 | Income lag 2 minggu | Engineered | 0–2jt | No | Yes | Low |  |
| lag_3_income | float64 | Income lag 3 minggu | Engineered | 0–2jt | No | Yes | Low |  |
| lag_4_income | float64 | Income lag 4 minggu (synthetic saja) | Engineered | 0–2jt | No | Yes | Low | Hanya synthetic |
| rolling_mean_4w | float64 | Rata-rata 4 lag minggu | Engineered | 0–2jt | No | Yes | Low |  |
| rolling_std_4w | float64 | Std 4 lag minggu | Engineered | 0–2jt | No | Yes | Low |  |
| trend_slope_4w | float64 | Slope linear trend 4 minggu | Engineered | varies | No | Yes | Low |  |
| synthetic_weekly_income | float64 | Observed income synthetic (BUKAN target langsung) | Synthetic | 0–2jt | No | Lag source/target | High | Hanya synthetic_52w — JANGAN masuk X |
| pref_payday | int | Pref: penghasilan ramai di tanggal gajian | Form col 15 | 0/1 | Yes | Yes | Low | Dari multi-hot ramai_akhir_bulan \| ramai_awal_bulan |
| pref_weekend | int | Pref: penghasilan ramai di akhir pekan | Form col 15 | 0/1 | Yes | Yes | Low | Dari ramai_weekend |
| pref_ramadan_lebaran | int | Pref: penghasilan ramai di Ramadan/Lebaran | Form col 15 | 0/1 | Yes | Yes | Low | Dari ramai_ramadan |
| pref_harbolnas | int | Pref: penghasilan ramai di Harbolnas | Form col 15 | 0/1 | Yes | Yes | Low | Dari ramai_harbolnas |
| pref_natal_tahun_baru | int | Pref: penghasilan ramai di Natal/Tahun Baru | Form col 15 | 0/1 | Yes | Yes | Low | Dari ramai_natal |
| bps_jasa_weekly | float64 | Benchmark BPS jasa per minggu per domisili | BPS | 125rb–175rb | Yes | Yes | Low | Bulanan/4 |
| is_synthetic | int | 1 jika synthetic, 0 jika real | Generated | 1 | No | No | Low |  |

## 8. Penjelasan File Output untuk AI Engineer

### 8.1 `synthetic_52week_weekly_forecasting_dataset.csv`

File full supervised dataset untuk prediksi weekly income. Cocok untuk eksperimen model tambahan, feature selection, atau retraining.

Kolom penting:
- `synthetic_user_id`
- `target_week_index`
- `target_date`
- `next_week_income`
- `next_week_direction`
- lag features
- rolling features
- trend features
- calendar features
- profile features
- preference features
- one-hot gig type

### 8.2 `synthetic_52w_train.csv`

Train set utama. Model harus fit pada file ini.

Aturan:
- Gunakan hanya fitur dari `final_weekly_features.json`.
- Jangan memasukkan target atau forbidden columns.
- Scaler hanya fit pada train.

### 8.3 `synthetic_52w_test.csv`

Test set utama. Dipakai untuk evaluasi final model.

Aturan:
- Jangan fit scaler ulang di test.
- Gunakan scaler dari train.
- Gunakan feature order yang sama persis.

### 8.4 `final_weekly_features.json`

Kontrak fitur utama. File ini wajib dipakai untuk menjaga konsistensi antara DS dan AI Engineer.

Isi penting:
- versi pipeline;
- jumlah synthetic users;
- jumlah minggu;
- feature order;
- one-hot gig type;
- forbidden leakage columns;
- split rule;
- normalization rule;
- role survey;
- catatan monthly estimation.

### 8.5 `target_contract.json`

Kontrak target model.

Isi penting:
- target regresi: `next_week_income`;
- target klasifikasi: `next_week_direction`;
- kelas direction: `Down`, `Stable`, `Up`;
- threshold direction: 10%;
- scaler target: `weekly_target_scaler.pkl`;
- target metrik realistis.

### 8.6 `leakage_rules.md`

Dokumentasi anti-leakage. AI Engineer wajib mengikuti file ini saat membangun training/inference pipeline.

### 8.7 `weekly_target_scaler.pkl`

Scaler target untuk transformasi:

```text
log1p(next_week_income) → MinMaxScaler
```

Catatan:
- scaler fit hanya pada train;
- untuk mengembalikan prediksi ke rupiah, lakukan inverse transform lalu `expm1`.

### 8.8 `weekly_feature_scaler.pkl`

Feature scaler berbasis `RobustScaler`. Bisa dipakai jika model AI Engineer membutuhkan scaling fitur.

Catatan:
- tree-based model seperti Random Forest/XGBoost tidak selalu wajib memakai feature scaler;
- model linear/neural network lebih membutuhkan scaler.

### 8.9 `feature_importance_weekly.csv`

File interpretasi fitur dari model terbaik. Dipakai untuk:
- melihat fitur paling dominan;
- debugging model;
- menjelaskan hasil ke stakeholder;
- menyederhanakan fitur jika diperlukan.

## 9. Inference Contract Sederhana

Untuk inference mingguan, input minimal harus bisa membentuk fitur berikut:

1. Riwayat pendapatan 4 minggu terakhir.
2. Profil user:
   - usia;
   - pengalaman kerja;
   - hari kerja per minggu;
   - jam kerja per hari;
   - domisili;
   - jenis gig.
3. Preferensi seasonal:
   - payday;
   - weekend;
   - Ramadan/Lebaran;
   - Natal/Tahun Baru;
   - Harbolnas;
   - promo aplikasi.
4. Informasi target week:
   - bulan;
   - week of month;
   - quarter;
   - apakah payday period;
   - apakah weekend/seasonal event.

Output model yang diharapkan:

| Output | Bentuk |
|---|---|
| Weekly income prediction | angka rupiah |
| Direction prediction | `Up`, `Stable`, atau `Down` |
| Monthly estimation | agregasi 4 prediksi mingguan |
| Risk/readiness score | optional, bisa dikembangkan dari volatility dan hasil prediksi |

## 10. Catatan Penting untuk AI Engineer

1. Jangan training dari `cleaned_survey_data.csv` sebagai dataset utama karena hanya punya 4 minggu income.
2. Gunakan synthetic 52w sebagai dataset training utama.
3. Real 4w hanya sanity check.
4. Split harus berdasarkan `synthetic_user_id`, bukan random row.
5. Jangan memasukkan `next_week_income`, `next_week_direction`, atau raw income `income_w1-w4` ke fitur.
6. Gunakan feature order dari `final_weekly_features.json`.
7. Direction threshold wajib 10% dengan operator `>=` dan `<=`.
8. Prediksi bulanan bukan target langsung, tetapi dihitung dari akumulasi 4 prediksi mingguan.
