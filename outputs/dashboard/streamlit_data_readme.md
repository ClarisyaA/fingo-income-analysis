# Streamlit Dashboard Data README
*Fingo Weekly Income Forecasting — v13-FINAL*

## ⚠️ Peringatan Dataset
- **Data survey real 384 responden** = acuan distribusi + sanity check
- **Data sintetis 3.000 users × 52 minggu** = dataset training utama
- Jangan klaim performa synthetic sebagai performa dunia nyata tanpa validasi live

## Narasi Data
Dataset survei asli sebanyak 384 responden digunakan sebagai empirical baseline untuk
membentuk distribusi karakteristik pekerja gig (jenis pekerjaan, domisili, pola pendapatan,
jam kerja, preferensi musiman). Karena data survei hanya mencakup empat minggu historis,
dataset tersebut tidak dijadikan sumber utama pelatihan forecasting. Sebagai gantinya,
dibangun synthetic longitudinal dataset sebanyak 3.000 pengguna dengan riwayat pendapatan
selama 52 minggu. Model difokuskan untuk memprediksi pendapatan minggu berikutnya,
sedangkan estimasi bulanan diperoleh melalui agregasi prediksi mingguan.

## File Dashboard (outputs/dashboard/)
| File | Deskripsi | Sumber |
|------|-----------|--------|
| gig_type_distribution.csv | Distribusi 8 jenis pekerjaan | Real 384 resp |
| real_4w_income_summary.csv | Income summary per gig_type | Real 384 resp |
| synthetic_52w_income_summary.csv | Income summary 3000 users | Synthetic |
| synthetic_monthly_trend_summary.csv | Tren income per bulan | Synthetic |
| synthetic_seasonal_event_summary.csv | Income per seasonal event | Synthetic |
| dataset_comparison_summary.csv | Real vs synthetic | Mixed |
| model_performance_summary.csv | Semua model | Synthetic utama |
| ab_testing_summary.csv | A/B test summary | Synthetic |
| seasonal_event_income_summary.csv | Seasonal preferences | Real |
| direction_threshold_summary.csv | Threshold comparison | Real |
| synthetic_quality_summary.csv | Validasi kualitas synthetic | Mixed |
| data_dictionary.csv | Dokumentasi kolom | - |
