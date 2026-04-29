# Data Dictionary - income_clean.csv

Dokumen ini menjelaskan arti setiap kolom pada dataset `income_clean.csv`.

Data dictionary ini dibuat agar dataset lebih mudah dipahami oleh Data Scientist, AI Engineer, maupun pembaca non-teknis.


## Identitas Pengguna

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan |
|---|---|---|---|---|
| `user_id` | string | SYN_0001, SYN_0300, SRV_0001 | Kode unik untuk membedakan setiap pengguna. | Tidak boleh duplikat untuk user yang sama. |
| `gig_type` | string | ojek_online, kurir, freelancer_it, freelancer_desain, content_creator, jualan_online | Menunjukkan jenis pekerjaan pengguna. | Dikalibrasi dari benchmark Indonesia. |
| `region` | string | jabodetabek, bandung, jawa_barat_lainnya, jawa_tengah, dan lainnya | Lokasi tempat pengguna bekerja atau tinggal. | Contoh: jabodetabek memiliki multiplier 1.10x. |
| `experience_tier` | string | junior, mid, senior | Menunjukkan apakah pengguna masih pemula, menengah, atau sudah berpengalaman. | junior=0.65x, mid=1.0x, senior=1.45x. |
| `platform` | string | Gojek, Grab, Shopee, Tokopedia, Fiverr, Upwork | Aplikasi atau platform tempat pengguna bekerja. | Platform disesuaikan dengan jenis pekerjaan. |

## Informasi Waktu

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan |
|---|---|---|---|---|
| `week_number` | int | 1-52 | Menunjukkan data ini berasal dari minggu keberapa. | train=1-36, validation=37-44, test=45-52. |
| `week_of_month` | int | 1-4 | Dipakai untuk melihat efek akhir bulan atau payday week. | Minggu ke-4 diasumsikan sebagai minggu gajian. |
| `seasonal_label` | string | low_season, normal, ramadan, lebaran, harbolnas, yearend | Menunjukkan kondisi periode tertentu, misalnya Ramadan atau akhir tahun. | Digunakan untuk menangkap pola musiman. |
| `seasonal_income_pattern` | int | 1-6 | Versi angka dari label musim agar lebih mudah diproses model. | Mapping dari SEASONAL_INT_MAP. |
| `is_payday_week` | int | 0 atau 1 | Menandai apakah minggu tersebut adalah minggu akhir bulan. | Dipakai untuk melihat efek gajian terhadap pendapatan. |

## Pendapatan

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan |
|---|---|---|---|---|
| `income_amount` | float | >= 0 | Ini adalah kolom utama yang berisi penghasilan pengguna per minggu. | Dihasilkan menggunakan distribusi Log-Normal AR(1), dibulatkan ke ribuan. |
| `income_normalized` | float | 0.0-1.0 | Pendapatan yang sudah diubah ke skala 0 sampai 1 agar lebih mudah dipelajari model. | Scaler disimpan di income_scalers.pkl. |
| `income_growth_1w` | float | -1.0 sampai 5.0 | Menunjukkan apakah pendapatan naik atau turun dari minggu lalu. | Dihitung dari income minggu ini dibanding lag_1w. |
| `income_vs_rolling` | float | bisa negatif atau positif | Menunjukkan apakah pendapatan minggu ini lebih tinggi atau lebih rendah dari rata-rata 4 minggu terakhir. | Nilai positif berarti lebih tinggi dari rata-rata. |

## Feature Engineering

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan |
|---|---|---|---|---|
| `rolling_mean_4w` | float | >= 0 | Rata-rata penghasilan pengguna dalam 4 minggu terakhir. | Salah satu fitur penting untuk prediksi LSTM. |
| `rolling_std_4w` | float | >= 0 | Menunjukkan seberapa naik-turun pendapatan pengguna dalam 4 minggu terakhir. | Semakin tinggi nilainya, semakin tidak stabil pendapatannya. |
| `rolling_cov_8w` | float | >= 0 | Mengukur tingkat ketidakstabilan pendapatan dalam 8 minggu terakhir. | Volatilitas jangka menengah. |
| `income_volatility` | float | >= 0 | Mengukur seberapa tidak stabil pendapatan seorang pengguna selama setahun. | Nilainya konstan untuk user yang sama. |
| `lag_1w` | float | >= 0 | Penghasilan minggu lalu. | Dipakai agar model bisa belajar pola waktu. |
| `lag_2w` | float | >= 0 | Penghasilan 2 minggu lalu. | Dipakai untuk menangkap pola jangka pendek. |
| `lag_4w` | float | >= 0 | Penghasilan 4 minggu lalu. | Membantu membaca pola bulanan. |

## Target Model

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan |
|---|---|---|---|---|
| `target_next_week` | float | >= 0 | Nilai yang akan diprediksi oleh model. | Baris terakhir tiap user bernilai NaN karena tidak punya minggu berikutnya. |

## Metadata

| Kolom | Tipe Data | Contoh/Range | Penjelasan Sederhana | Catatan |
|---|---|---|---|---|
| `data_source` | string | synthetic atau survey | Menandai apakah data berasal dari hasil sintesis atau survei asli. | Berguna untuk validasi proporsi data. |

---

## Ringkasan Kolom Penting

| Jenis Kolom | Kolom | Fungsi Utama |
|---|---|---|
| Identitas | `user_id`, `gig_type`, `region`, `experience_tier`, `platform` | Menjelaskan profil pengguna |
| Waktu | `week_number`, `week_of_month`, `seasonal_label`, `is_payday_week` | Menjelaskan konteks waktu pendapatan |
| Pendapatan | `income_amount`, `income_normalized`, `income_growth_1w` | Menjelaskan nilai dan perubahan income |
| Fitur Prediksi | `rolling_mean_4w`, `rolling_std_4w`, `rolling_cov_8w`, `lag_1w`, `lag_2w`, `lag_4w` | Digunakan sebagai input model prediksi |
| Target | `target_next_week` | Nilai yang akan diprediksi model |
| Metadata | `data_source` | Menandai asal data |

## Catatan untuk AI Engineer

- Kolom utama yang diprediksi adalah `target_next_week`.
- Kolom input penting untuk model time-series adalah `income_amount`, `lag_1w`, `lag_2w`, `lag_4w`, `rolling_mean_4w`, `rolling_std_4w`, dan `seasonal_income_pattern`.
- Kolom `income_normalized` digunakan agar skala pendapatan antar-user lebih stabil untuk model.
- Baris terakhir setiap user memiliki `target_next_week = NaN`, sehingga perlu dihapus sebelum training supervised learning.
