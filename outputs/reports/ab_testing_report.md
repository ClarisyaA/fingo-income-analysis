# Laporan A/B Testing — Fingo Income Predictor
**Tim CC26-PSU217** | Notebook 10

---

## Disclaimer
> Notebook ini menggunakan **synthetic dataset** untuk mensimulasikan pipeline evaluasi
> fitur notifikasi pengingat tabungan. Seluruh hasil harus diinterpretasikan sebagai
> **proof-of-concept**, bukan sebagai bukti kausalitas real-world.

## 1. Latar Belakang
Fingo ingin menguji apakah fitur **notifikasi pengingat tabungan** berpotensi meningkatkan
pendapatan mingguan pengguna gig economy. Pengguna disimulasikan dibagi menjadi dua grup:
- **Control**: tidak menerima notifikasi
- **Treatment**: menerima notifikasi pengingat tabungan harian

> **Catatan Metrik:** `avg_weekly_income` digunakan sebagai proxy metric karena tersedia
> di synthetic dataset. Untuk eksperimen live, metrik yang lebih relevan meliputi:
> `saving_rate`, `budget_adherence`, `impulsive_transaction_count`,
> `app_engagement`, dan `notification_response_rate`.

## 2. Hipotesis
- **H₀**: μ_treatment = μ_control (tidak ada perbedaan)
- **H₁**: μ_treatment > μ_control (treatment lebih tinggi)
- **Significance level**: α = 0.05

## 3. Desain Eksperimen
- Sumber data: Synthetic dataset (52 minggu, ±3.000 user simulasi)
- Metode assignment: Stratified random assignment per gig_type
- Total sampel: 3,000 pengguna
- Control: 1,502 pengguna | Treatment: 1,498 pengguna
- Metrik proxy: avg_weekly_income (secondary; behavioral metrics lebih relevan)

## 4. Statistik Deskriptif
| Metrik | Control | Treatment |
|--------|---------|-----------|
| N | 1,502 | 1,498 |
| Mean | Rp 423rb | Rp 442rb |
| Median | Rp 344rb | Rp 369rb |
| Std Dev | Rp 292rb | Rp 311rb |
| Relative Lift | — | +4.63% |

## 5. Uji Asumsi
| Uji | Statistic | p-value | Hasil |
|-----|-----------|---------|-------|
| Shapiro-Wilk (Control) | 0.8676 | 0.0000 | Tidak Normal |
| Shapiro-Wilk (Treatment) | 0.8808 | 0.0000 | Tidak Normal |
| Levene (homogenitas var.) | 1.7960 | 0.1803 | Homogen |
> Data tidak berdistribusi normal → **Mann-Whitney U digunakan sebagai uji utama**.

## 6. Hasil Uji Hipotesis
| Uji | Statistic | p-value | Keputusan | Peran |
|-----|-----------|---------|-----------|-------|
| Mann-Whitney U (one-tailed) | 1160944 | 0.064843 | Gagal Tolak H₀ ✗ | **Uji Utama** |
| Welch t-test (one-tailed) | 1.7781 | 0.037747 | Tolak H₀ ✓ | Pendukung |

## 7. Effect Size & Lift
- **Cohen's d** = 0.0650 → Efek Kecil (sangat kecil, belum substansial secara praktis)
- **Absolute Lift** = Rp 20rb per minggu
- **Relative Lift** = 4.63% (arah positif, namun belum konklusif secara statistik)
- **95% CI (diff mean)**: [Rp -2rb, Rp 41rb]
- **CI melewati nol**: Ya — perbedaan tidak dapat dikonfirmasi secara statistik.
- **Bootstrap 95% CI**: [Rp -4rb, Rp 41rb]

## 8. Power Analysis
- Power yang dicapai: **0.5526** (Kurang < 0.80 ✗ — eksperimen belum memiliki kekuatan statistik yang memadai)

## 9. Subgroup Analysis
> ⚠️ Hasil subgroup bersifat **eksploratorif**. Jangan dijadikan klaim utama.
> Setiap subgroup yang menunjukkan indikasi positif perlu divalidasi melalui
> eksperimen terpisah dengan sample size yang cukup per segmen.

## 10. Kesimpulan
Berdasarkan **Mann-Whitney U Test** (uji utama, p=0.064843 ≥ α=0.05),
belum terdapat bukti statistik yang cukup bahwa fitur notifikasi tabungan
secara signifikan meningkatkan pendapatan mingguan pengguna.

Meskipun demikian, Treatment menunjukkan **arah positif** (+4.63%),
dengan effect size yang masih sangat kecil (Cohen's d = 0.0650).
Confidence interval yang melewati nol dan power yang belum memadai (0.5526)
memperkuat bahwa hasil ini belum konklusif.

## 11. Rekomendasi
Berdasarkan hasil simulasi proof-of-concept ini:

1. **Lanjutkan dengan eksperimen live** — Implementasikan A/B test nyata dengan pengguna aktual
   untuk mendapatkan bukti kausal yang valid.
2. **Tambah sample size** — Untuk mendeteksi effect size kecil (d ≈ 0.065) dengan power ≥ 0.80,
   diperlukan sample size yang jauh lebih besar per grup.
3. **Gunakan metrik yang lebih relevan** — Ganti atau tambahkan proxy metric dengan behavioral
   finance metrics: `saving_rate`, `budget_adherence`, `impulsive_transaction_count`,
   `app_engagement`, dan `notification_response_rate`.
4. **Validasi subgroup secara terpisah** — Segmen yang menunjukkan indikasi positif perlu
   diuji dalam eksperimen dedicated sebelum ditargetkan secara spesifik.
5. **Jangan rollout ke semua pengguna** berdasarkan hasil synthetic ini — Hasil ini hanya
   merupakan simulasi proof-of-concept, bukan bukti efektivitas fitur di dunia nyata.

> *"Treatment shows a positive directional effect, but is not yet statistically conclusive.
>  Further validation through a live experiment with behavioral metrics is required
>  before any product decision can be made."*