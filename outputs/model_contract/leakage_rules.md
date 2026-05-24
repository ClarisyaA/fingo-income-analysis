# Leakage Rules — Fingo Weekly Forecasting

## Kolom DILARANG masuk FEATURE_COLS
| Kolom | Alasan |
|-------|--------|
| next_week_income | Target regresi |
| next_week_income_norm | Target normalized |
| next_week_direction | Target klasifikasi |
| monthly_income | Menggunakan semua W1-W4 (leakage) |
| avg_weekly_income | Menggunakan semua W1-W4 (leakage) |
| income_std_4w | Menggunakan semua W1-W4 (leakage) |
| income_w1, income_w2, income_w3, income_w4 | Harus dikonversi ke lag features, bukan langsung masuk X |
| synthetic_weekly_income | Target/lag source untuk synthetic, jangan masuk sebagai fitur langsung |

## Split Rules
- Split HARUS berbasis respondent_id (bukan random row split)
- Scaler fit HANYA pada train set
- Jangan fit scaler pada full dataset

## Gig Type Rules
- 8 kategori gig_type wajib dipertahankan
- Jangan gabungkan kategori ke "lainnya" kecuali ada nilai di luar GIG_MAP
- OHE 8 kolom: gig_jualan_online, gig_pekerja_harian, gig_freelance_desain, gig_ojek_online, gig_kurir, gig_freelance_it, gig_tutor, gig_content_creator

## Seasonal Notes
- pref_* = dari jawaban form (valid)
- target_is_christmas_year_end, target_is_new_year = calendar-based (bukan dari form)
- Natal/Tahun Baru bernilai 0 untuk data Mei 2026 (expected)

## Synthetic Data Rules
- Synthetic 52w hanya untuk prototyping dan simulasi
- Performa model pada synthetic TIDAK boleh diklaim sebagai real-world performance final
- Evaluasi utama harus pada real_4w test set
