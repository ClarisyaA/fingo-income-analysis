# Data Dictionary — income_clean.csv

Dokumen ini menjelaskan arti setiap kolom pada dataset `income_clean.csv`.


## Identitas Pengguna

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan |
|---|---|---|---|---|
| `user_id` | string | SYN_0001, SRV_0001 | Kode unik untuk membedakan setiap pengguna. | Tidak boleh duplikat untuk user yang sama. |
| `gig_type` | string | ojek_online, kurir, freelancer_it, freelancer_desain, content_creator, jualan_online | Menunjukkan jenis pekerjaan pengguna. | Dikalibrasi dari benchmark Indonesia. |
| `region` | string | jabodetabek, bandung, jawa_tengah, ... | Lokasi tempat pengguna bekerja. | jabodetabek memiliki multiplier 1.10x. |
| `experience_tier` | string | junior, mid, senior | Pemula, menengah, atau berpengalaman. | junior=0.65x, mid=1.0x, senior=1.45x. |
| `platform` | string | Gojek, Grab, Shopee, Fiverr, Upwork | Aplikasi tempat pengguna bekerja. | Disesuaikan dengan jenis pekerjaan. |

## Informasi Waktu

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan |
|---|---|---|---|---|
| `week_number` | int | 1-52 | Minggu keberapa data ini berasal. | train=1-36, val=37-44, test=45-52. |
| `week_of_month` | int | 1-4 | Dipakai untuk melihat efek payday. | Minggu ke-4 = payday week. |
| `seasonal_label` | string | low_season, normal, ramadan, lebaran, harbolnas, yearend | Kondisi periode (misal Ramadan, akhir tahun). | Digunakan untuk menangkap pola musiman. |
| `seasonal_income_pattern` | int | 1-6 | Versi angka dari label musim. | Mapping dari SEASONAL_INT_MAP. |
| `is_payday_week` | int | 0 atau 1 | Flag minggu gajian. | Efek gajian meningkatkan income gig worker. |

## Pendapatan

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan |
|---|---|---|---|---|
| `income_amount` | float | >= 0 | Kolom utama: penghasilan pengguna per minggu. | Log-Normal AR(1), dibulatkan ke ribuan. |
| `income_normalized` | float | 0.0-1.0 | Pendapatan dalam skala 0-1 per user. | Scaler disimpan di income_scalers.pkl. |
| `income_growth_1w` | float | -1.0 sampai 5.0 | Income naik atau turun dari minggu lalu. | Dihitung dari income vs lag_1w. |
| `income_vs_rolling` | float | bisa negatif atau positif | Income minggu ini lebih tinggi/rendah dari rata-rata 4 minggu terakhir. | Positif = lebih tinggi. |

## Feature Engineering

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan |
|---|---|---|---|---|
| `rolling_mean_4w` | float | >= 0 | Baseline income jangka pendek. | Fitur penting untuk LSTM. |
| `rolling_std_4w` | float | >= 0 | Seberapa fluktuatif income 4 minggu terakhir. | Volatilitas jangka pendek. |
| `rolling_cov_8w` | float | >= 0 | Ketidakstabilan income 8 minggu terakhir. | Volatilitas jangka menengah. |
| `income_volatility` | float | >= 0 | Karakteristik volatilitas user selama setahun. | Konstan untuk user yang sama. |
| `lag_1w` | float | >= 0 | Penghasilan minggu lalu. | Input kunci LSTM untuk pola temporal. |
| `lag_2w` | float | >= 0 | Penghasilan 2 minggu lalu. | Pola jangka pendek. |
| `lag_4w` | float | >= 0 | Penghasilan 4 minggu lalu. | Membantu membaca pola bulanan. |

## Target Model

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan |
|---|---|---|---|---|
| `target_next_week` | float | >= 0 | Nilai yang diprediksi model. | Baris terakhir tiap user = NaN, harus di-drop sebelum training. |

## Metadata

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan |
|---|---|---|---|---|
| `data_source` | string | synthetic atau survey | Apakah data dari sintesis atau survei asli. | Berguna untuk validasi proporsi. |

## Catatan untuk AI Engineer

- Kolom target: `target_next_week`
- Input utama LSTM: `income_amount`, `lag_1w`, `lag_2w`, `lag_4w`, `rolling_mean_4w`, `rolling_std_4w`, `seasonal_income_pattern`
- Gunakan `income_normalized` untuk training agar skala stabil antar user
- Drop baris dengan `target_next_week = NaN` sebelum training
