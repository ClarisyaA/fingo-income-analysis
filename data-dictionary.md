# Data Dictionary — income_clean.csv

| Kolom | Tipe | Deskripsi | Contoh |
|---|---|---|---|
| user_id | string | ID unik per pengguna | SYN_0001 |
| week_number | int | Minggu ke-N dalam setahun (1–52) | 14 |
| week_of_month | int | Minggu ke-N dalam bulan (1–4) | 4 |
| gig_type | string | Jenis pekerjaan gig | ojek_online |
| weekly_income_idr | float | Penghasilan minggu itu (Rupiah) | 750000 |
| is_ramadan | int | 1 jika minggu Ramadan | 0 |
| is_lebaran | int | 1 jika minggu Lebaran | 0 |
| is_yearend | int | 1 jika minggu akhir tahun | 0 |
| is_jan_feb | int | 1 jika Januari–Februari | 0 |
| is_payday_week | int | 1 jika minggu ke-4 (gajian) | 1 |
| rolling_mean_4w | float | Rata-rata 4 minggu sebelumnya | 720000 |
| rolling_std_4w | float | Std dev 4 minggu sebelumnya | 85000 |
| income_growth_1w | float | % perubahan dari minggu lalu | 0.05 |
| income_volatility | float | Coefficient of variation per user | 0.28 |
| seasonal_income_pattern | string | Label musim | normal |
| data_source | string | Asal data | synthetic |