# Technical Report — Fingo v13-FINAL
**Tim:** CC26-PSU217 | **Versi:** v13-FINAL | **Tanggal:** Mei 2026

## Narasi Dataset
Dataset survei asli sebanyak **384 responden** digunakan sebagai empirical baseline untuk
membentuk distribusi karakteristik pekerja gig — seperti jenis pekerjaan, domisili, pola
pendapatan, jam kerja, dan preferensi musiman. Karena data survei hanya mencakup empat
minggu historis, dataset tersebut tidak dijadikan sumber utama pelatihan forecasting.
Sebagai gantinya, dibangun synthetic longitudinal dataset sebanyak **3,000 pengguna**
dengan riwayat pendapatan selama **52 minggu** (156,000 rows raw synthetic).
Model difokuskan untuk memprediksi pendapatan minggu berikutnya (next_week_income),
sedangkan estimasi bulanan diperoleh melalui agregasi prediksi mingguan.

## Key Design Decisions
1. **Urutan income**: income_w4 (terlama) → income_w1 (terbaru) — sesuai pertanyaan form
2. **Winsorize global DIHAPUS** — clip lower=0 saja untuk real; cap per gig_type untuk synthetic
3. **Direction threshold**: >= 10% = Up, <= -10% = Down (fix dari > / <)
4. **3.000 synthetic users** di-sample dari distribusi survey 384 responden
5. **Noise/shock per gig_type**: content_creator & freelance punya "zero-income week" 6%
6. **Split by user_id** — bukan random rows — mencegah leakage
7. **Survey = distribusi acuan**, bukan training utama

## Data Sources
- Survey real: 384 responden (Google Form Mei 2026)
- BPS 2023-2025: regional income benchmarks
- Synthetic: 3,000 users x 52 weeks (AR1 + noise)

## Best Model (Synthetic 52w — Dataset Utama)
- Regression: Ridge (MAE=55218, MAPE=88.3%)
- Classification: Random Forest (Accuracy=79.0%, F1=63.2%)

## Synthetic Data Quality
- Mean autocorrelation lag-1: 0.5844
- Total synthetic rows: 156,000

## Disclaimer
Real 4-week dataset (384 resp) digunakan sebagai sanity check saja.
Synthetic 52w adalah dataset training utama.
