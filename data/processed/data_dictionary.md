# Data Dictionary — income_clean.csv (v9 — FINAL)

Dokumen ini menjelaskan arti setiap kolom pada dataset `income_clean.csv`.

> Versi v9: Tambah lag_8w, lag_12w, week_sin, week_cos. Fix data leakage pada MinMaxScaler.


## Identitas Pengguna

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan untuk AI Engineer |
|---|---|---|---|---|
| `user_id` | string | SYN_0001, SRV_0001 | Kode unik tiap pengguna. | Gunakan untuk group-by saat membuat sequence LSTM. |
| `gig_type` | string | ojek_online | kurir | jualan_online | freelancer_desain | freelancer_it | content_creator | Kategori pekerjaan pengguna. | Tersedia sebagai one-hot di kolom gig_*. Jangan pakai raw string. |
| `region` | string | jabodetabek | bandung | jawa_tengah | ... | Lokasi tempat pengguna bekerja. | Bukan one-hot — encode sendiri jika dipakai sebagai fitur. |
| `experience_tier` | string | junior | mid | senior | Pemula, menengah, atau berpengalaman. | Tersedia sebagai one-hot di kolom exp_*. Jangan pakai raw string. |
| `platform` | string | Gojek | Grab | Shopee | Fiverr | Upwork | Aplikasi tempat pengguna bekerja. | Optional — encode jika ingin menangkap perbedaan platform. |

## Informasi Waktu

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan untuk AI Engineer |
|---|---|---|---|---|
| `week_number` | int | 1–52 | Minggu keberapa data ini. | train=1-36, val=37-44, test=45-52. Gunakan untuk kronologis split. |
| `week_of_month` | int | 1–4 | Dipakai untuk melihat efek gajian. | Sudah tersedia is_payday_week sebagai flag biner. |
| `seasonal_label` | string | low_season | normal | ramadan | lebaran | harbolnas | yearend | Kondisi periode. | Tersedia sebagai int di seasonal_income_pattern dan float di week_sin/week_cos. |
| `seasonal_income_pattern` | int | 1–6 | Versi angka dari label musim. | Alternatif gunakan week_sin/week_cos untuk encoding kontinu. |
| `week_sin` | float | -1.0 sampai 1.0 | Representasi kontinu posisi minggu dalam siklus tahunan (komponen sinus). | v9 BARU. Pakai bersama week_cos agar model memahami siklus musiman secara kontinu. |
| `week_cos` | float | -1.0 sampai 1.0 | Representasi kontinu posisi minggu dalam siklus tahunan (komponen kosinus). | v9 BARU. Pakai bersama week_sin. |
| `is_payday_week` | int | 0 atau 1 | Flag minggu gajian. | Efek gajian meningkatkan income gig worker, terutama jualan_online. |

## Pendapatan

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan untuk AI Engineer |
|---|---|---|---|---|
| `income_amount` | float | > 0, dalam Rupiah | Penghasilan pengguna per minggu. | JANGAN masukkan ke fitur training (gunakan income_normalized). Hanya untuk referensi. |
| `income_normalized` | float | 0.0–1.0 (train), bisa > 1.0 di val/test | Pendapatan dalam skala 0–1 (berdasarkan train set). | Gunakan sebagai INPUT utama LSTM. Nilai > 1 di val/test normal karena scaler fit di train saja. |
| `income_growth_1w` | float | -1.0 sampai 5.0 | Income naik atau turun dari minggu lalu. | v9: dihitung per minggu untuk data survei juga (bukan 0 semua). |
| `income_vs_rolling` | float | bisa negatif atau positif | Income minggu ini lebih tinggi/rendah dari rata-rata 4 minggu terakhir. | Positif = above average. Berguna sebagai fitur momentum. |

## Feature Engineering

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan untuk AI Engineer |
|---|---|---|---|---|
| `rolling_mean_4w` | float | > 0 | Baseline income jangka pendek. | Fitur paling prediktif (r ≈ 0.9 dengan income_amount). |
| `rolling_std_4w` | float | ≥ 0 | Fluktuasi income jangka pendek. | Gunakan sebagai proxy volatilitas jangka pendek. |
| `rolling_cov_8w` | float | ≥ 0 | Ketidakstabilan income 8 minggu terakhir. | Volatilitas jangka menengah (2 bulan). |
| `income_volatility` | float | ≥ 0 | Karakteristik volatilitas user selama setahun. | Bersifat statis per user. Berguna sebagai fitur konteks user-level. |
| `lag_1w` | float | ≥ 0 | Penghasilan minggu lalu. | Input kunci LSTM untuk pola temporal jangka pendek. |
| `lag_2w` | float | ≥ 0 | Penghasilan 2 minggu lalu. | Pola jangka pendek. |
| `lag_4w` | float | ≥ 0 | Penghasilan sebulan lalu. | Membantu model menangkap pola bulanan (efek payday). |
| `lag_8w` | float | ≥ 0 | Penghasilan 2 bulan lalu. | v9 BARU. Pola bi-monthly. Berguna jika ada siklus 2 bulanan. |
| `lag_12w` | float | ≥ 0 | Penghasilan 3 bulan lalu. | v9 BARU. Pola kuartalan. Berguna untuk musim yang berulang setiap kuartal. |

## One-Hot Encoding

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan untuk AI Engineer |
|---|---|---|---|---|
| `gig_ojek_online` | int | 0 atau 1 | Flag jenis pekerjaan. | Gunakan semua kolom gig_* sebagai fitur kategorikal. |
| `gig_kurir (dan gig_* lainnya)` | int | 0 atau 1 | Flag masing-masing jenis pekerjaan. | Kolom: gig_ojek_online, gig_kurir, gig_jualan_online, gig_freelancer_desain, gig_freelancer_it, gig_content_creator. |
| `exp_junior (dan exp_* lainnya)` | int | 0 atau 1 | Flag tingkat pengalaman. | Kolom: exp_junior, exp_mid, exp_senior. |

## Target Model

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan untuk AI Engineer |
|---|---|---|---|---|
| `target_next_week` | float | > 0 (atau NaN) | Nilai yang diprediksi model (income minggu depan). | ⚠ DROP baris dengan target_next_week == NaN sebelum training. Baris terakhir tiap user adalah NaN. |

## Metadata

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan untuk AI Engineer |
|---|---|---|---|---|
| `data_source` | string | synthetic | survey | Apakah data dari sintesis atau survei asli. | Bisa dipakai untuk analisis performa model per sumber data. |

## Ringkasan Input LSTM yang Disarankan untuk AI Engineer

**Target:** `target_next_week`

**Fitur utama (disarankan dimasukkan ke LSTM):**
- Temporal: `income_normalized`, `lag_1w`, `lag_2w`, `lag_4w`, `lag_8w`, `lag_12w`
- Rolling: `rolling_mean_4w`, `rolling_std_4w`, `rolling_cov_8w`
- Musiman: `week_sin`, `week_cos`, `seasonal_income_pattern`, `is_payday_week`
- Volatilitas: `income_volatility`, `income_vs_rolling`, `income_growth_1w`
- Kategori: `gig_*` (6 kolom), `exp_*` (3 kolom)

**Yang TIDAK boleh masuk fitur training:**
- `income_amount` — raw income, sudah diwakili oleh `income_normalized`
- `target_next_week` — ini adalah label, bukan fitur

**Catatan normalisasi:**
- `income_normalized` bisa > 1.0 di val/test (karena scaler fit di train saja) — ini benar dan diharapkan
- Gunakan `income_scalers.pkl` untuk inverse transform hasil prediksi ke Rupiah asli
