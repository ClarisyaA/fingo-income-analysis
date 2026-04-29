# Data Dictionary - income_clean.csv

| Kolom | Tipe | Range | Deskripsi | Catatan |
|---|---|---|---|---|
| user_id | string | SYN_0001-SYN_0300 / SRV_0001+ | ID unik per pengguna. SYN_=sintetis, SRV_=survei. |  |
| gig_type | string | 6 kategori | ojek_online/kurir/freelancer_it/freelancer_desain/content_creator/jualan_online | Dikalibrasi dari benchmark Indonesia |
| region | string | 10 wilayah | Wilayah domisili. Mempengaruhi income via REGION_MULTIPLIER. | jabodetabek=1.10x |
| experience_tier | string | junior/mid/senior | Tier pengalaman kerja. | junior=0.65x, mid=1.0x, senior=1.45x |
| platform | string | nama platform | Platform utama yang digunakan user. | Disesuaikan dengan gig_type |
| week_number | int | 1-52 | Nomor minggu dalam setahun. | train=1-36, val=37-44, test=45-52 |
| week_of_month | int | 1-4 | Minggu ke-berapa dalam bulan. 4=akhir bulan (efek gajian). |  |
| seasonal_label | string | 6 label | low_season/normal/ramadan/lebaran/harbolnas/yearend |  |
| income_amount | float | >= 0 | KOLOM UTAMA. Pendapatan bersih mingguan IDR. | Log-Normal AR(1). Dibulatkan ke ribuan. |
| income_normalized | float | 0.0-1.0 | income_amount yang di-MinMaxScaler per user. | Scaler di income_scalers.pkl |
| target_next_week | float | >= 0 | KOLOM TARGET. Income minggu berikutnya (shift -1). | NaN di baris terakhir per user |
| rolling_mean_4w | float | >= 0 | Rata-rata income 4 minggu terakhir per user. | Feature LSTM paling penting |
| rolling_std_4w | float | >= 0 | Standar deviasi income 4 minggu terakhir per user. |  |
| rolling_cov_8w | float | >= 0 | CoV rolling 8 minggu (volatilitas jangka menengah). |  |
| income_volatility | float | >= 0 | CoV global per user (std/mean seluruh 52 minggu). | Konstan per user |
| lag_1w | float | >= 0 | Income minggu sebelumnya. |  |
| lag_2w | float | >= 0 | Income 2 minggu sebelumnya. |  |
| lag_4w | float | >= 0 | Income 4 minggu sebelumnya. |  |
| data_source | string | synthetic/survey | Asal data. |  |
| is_payday_week | int | 0/1 | 1 jika minggu ke-4 dalam bulan (efek gajian). |  |
