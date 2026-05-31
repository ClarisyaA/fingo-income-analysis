# Bias Validation Report — Fingo Income Predictor

## Test Results
0. **Income Floor Sanity Check**: min=75,000, rows<50k=0 (PASS),
1. **Mean vs BPS**: ratio synthetic/BPS = 3.20 (FAIL)
2. **Distribution (KS)**: stat=0.1028, p=0.0000 (toleransi: synthetic 52w vs real 4w snapshot)
3. **Seasonal direction**: Ramadan > Normal = PASS
4. **Autocorrelation lag-1**: 0.5796 (PASS, expected 0.30-0.90)
5. **BPS range per domisili**: lihat `outputs/reports/bps_range_validation.csv`
6. **Income per gig_type**: lihat `outputs/reports/gig_type_income_validation.csv`

## Catatan
- Survey real 384 resp = acuan distribusi, bukan training utama.
- Synthetic 3000 users = dataset training utama.
- income_w4 (terlama) → income_w1 (terbaru) = urutan kronologis benar.
- Perbedaan distribusi KS bisa muncul karena survey hanya snapshot 4 minggu, sedangkan synthetic adalah 52 minggu longitudinal.