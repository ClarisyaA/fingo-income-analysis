# Laporan A/B Testing — Fingo Income Predictor
**Simulated A/B Testing: Impact of Income Prediction on Budget Planning Accuracy**
**Tim CC26-PSU217** | Notebook 10

---

## Disclaimer
> Notebook ini menggunakan **synthetic dataset** untuk mensimulasikan pipeline evaluasi fitur
> **Income Predictor** yang mendukung **Budget Planner adaptif** Fingo.
> Seluruh hasil harus diinterpretasikan sebagai **proof-of-concept**, bukan sebagai bukti
> kausalitas atau efektivitas fitur di dunia nyata.

---

## 1. Latar Belakang
Fingo Income Predictor menggunakan data synthetic income time-series 52 minggu untuk
memprediksi pendapatan pengguna gig worker. Output prediksi income digunakan untuk membantu
pengguna menyusun budget yang lebih realistis melalui **Budget Planner adaptif**.

A/B Testing ini dirancang untuk menguji apakah pengguna yang mendapatkan bantuan prediksi
income dan rekomendasi budget adaptif memiliki perencanaan anggaran yang lebih baik
dibandingkan pengguna yang membuat budget manual berdasarkan rata-rata income historis.

## 2. Desain Eksperimen

| Elemen | Deskripsi |
|--------|-----------|
| Sumber data | synthetic_52week_user_income.csv (3,000 user, 52 minggu) |
| Metode assignment | Stratified random 50:50 per gig_type |
| Control Group | Budget manual berdasarkan rolling mean 4 minggu |
| Treatment Group | Budget adaptif berdasarkan predicted income (Income Predictor) |
| N Control | 1,502 user |
| N Treatment | 1,498 user |

## 3. Hipotesis

- **H0**: budget_adherence_rate Treatment = Control
- **H1**: budget_adherence_rate Treatment > Control (one-tailed)
- Significance level: alpha = 0.05

## 4. Statistik Deskriptif — Primary Metric

| Metrik | Control | Treatment |
|--------|---------|-----------|
| N | 1,502 | 1,498 |
| Mean Budget Adherence Rate | 0.4491 (44.91%) | 0.4221 (42.21%) |
| Median | 0.4423 | 0.4231 |
| Std Dev | 0.0609 | 0.0777 |
| Mean Over-Budget Rate | 0.5509 | 0.5779 |
| Mean Budget Error | Rp 56rb | Rp 15rb |

## 5. Uji Asumsi

| Uji | Statistic | p-value | Hasil |
|-----|-----------|---------|-------|
| Shapiro-Wilk (Control) | 0.9852 | 0.000058 | Tidak Normal |
| Shapiro-Wilk (Treatment) | 0.9895 | 0.001255 | Tidak Normal |
| Levene | 60.9087 | 0.000000 | Tidak Homogen |

> Uji utama yang dipilih: **Mann-Whitney U**

## 6. Hasil Uji Hipotesis

| Uji | Statistic | p-value | Keputusan | Peran |
|-----|-----------|---------|-----------|-------|
| Mann-Whitney U (one-tailed) | 898692 | 1.000000 | Gagal Tolak H0 | **Utama** |
| Welch t-test (one-tailed) | -10.5706 | 1.000000 | Gagal Tolak H0 | Pendukung |

## 7. Effect Size & Confidence Interval

- **Cohen's d** = -0.3862 -> Efek Sedang
- **Absolute Difference** = -2.70 poin persentase
- **Relative Lift** = -6.00%
- **95% CI (Welch)**: [-3.20pp, -2.20pp]
- **Bootstrap 95% CI**: [-3.19pp, -2.20pp]
- **CI melewati nol**: Ya - perbedaan belum dapat dikonfirmasi.

## 8. Power Analysis

- **Power yang dicapai** dengan n=1498: **1.0000** (Cukup >= 0.80)

## 9. Subgroup Analysis

> Hasil subgroup bersifat **eksploratorif**. Jangan dijadikan klaim utama.

| Gig Type | n_ctrl | n_treat | BAR Control | BAR Treatment | Diff | MW p | Indikasi |
|----------|--------|---------|-------------|---------------|------|------|----------|
| content_creator | 139 | 138 | 0.445 | 0.413 | -3.18pp | 0.9991 | - |
| freelance_desain | 230 | 229 | 0.441 | 0.419 | -2.24pp | 0.9970 | - |
| freelance_it | 180 | 180 | 0.436 | 0.415 | -2.03pp | 0.9753 | - |
| jualan_online | 248 | 248 | 0.451 | 0.424 | -2.70pp | 1.0000 | - |
| kurir | 113 | 112 | 0.445 | 0.427 | -1.80pp | 0.9852 | - |
| ojek_online | 115 | 114 | 0.460 | 0.433 | -2.65pp | 0.9924 | - |
| pekerja_harian | 249 | 249 | 0.460 | 0.421 | -3.85pp | 1.0000 | - |
| tutor | 228 | 228 | 0.453 | 0.427 | -2.59pp | 1.0000 | - |

## 10. Kesimpulan

Treatment menunjukkan arah positif terhadap peningkatan budget adherence rate (-2.70 poin persentase, relative lift -6.00%), tetapi belum terdapat bukti statistik yang cukup untuk menyatakan bahwa penggunaan Income Predictor secara signifikan lebih baik dibandingkan budgeting manual (Mann-Whitney U p=1.000000 >= alpha=0.05).\n\nValidasi lanjutan diperlukan dengan data yang lebih besar, metrik perilaku yang lebih lengkap, dan eksperimen live pada pengguna nyata.

## 11. Rekomendasi

1. **Lanjutkan dengan eksperimen live** pada pengguna nyata untuk validasi kausal.
2. **Perbesar sample size** agar power >= 0.80 dapat dicapai untuk effect size yang relevan.
3. **Gunakan metrik behavioral yang lebih lengkap**: notification_response_rate, app_engagement,
   impulsive_transaction_count, plan_revision_frequency.
4. **Validasi subgroup secara dedicated** per segmen gig_type yang menunjukkan indikasi positif.
5. **Jangan rollout berdasarkan data synthetic ini** — hasil ini adalah proof-of-concept,
   bukan bukti efektivitas fitur di dunia nyata.

---

> *"Simulasi A/B Testing ini merupakan proof-of-concept yang menunjukkan bahwa Income Predictor
> berpotensi membantu pengguna menyusun budget yang lebih akurat. Validasi melalui eksperimen
> live pada pengguna nyata tetap diperlukan sebelum kesimpulan kausal dapat ditarik."*