# Laporan A/B Testing — Fingo Income Predictor
**Simulated A/B Testing: Impact of Income Prediction on Budget Planning Accuracy**
**Tim CC26-PSU217** | Notebook 10

---

## Disclaimer
> Notebook ini menggunakan **synthetic dataset** untuk mensimulasikan pipeline evaluasi fitur
> **Income Predictor** yang mendukung **Budget Planner adaptif** Fingo.
> Seluruh hasil harus diinterpretasikan sebagai **proof-of-concept**, bukan sebagai bukti
> kausalitas atau efektivitas fitur di dunia nyata.
> Validasi live experiment pada pengguna nyata tetap diperlukan.

---

## 1. Latar Belakang
Fingo Income Predictor menggunakan data synthetic income time-series 52 minggu untuk
memprediksi pendapatan pengguna gig worker. Output prediksi income digunakan untuk
membantu pengguna menyusun budget yang lebih realistis melalui **Budget Planner adaptif**.

A/B Testing ini dirancang untuk menguji apakah pengguna yang mendapatkan bantuan prediksi
income menghasilkan perencanaan anggaran yang **lebih akurat** dibandingkan pengguna yang
membuat budget manual berdasarkan rata-rata income historis.

> **Catatan penting**: Income Predictor tidak diuji untuk menaikkan pendapatan dan tidak
> langsung menjamin user tidak over-budget. Income Predictor diuji sebagai alat bantu
> budget planning. Dampak terhadap perilaku pengeluaran (budget adherence, over-budget rate)
> perlu divalidasi terpisah melalui eksperimen live.

## 2. Desain Eksperimen

| Elemen | Deskripsi |
|--------|-----------|
| Sumber data | synthetic_52week_user_income.csv (3,000 user, 52 minggu) |
| Metode assignment | Stratified random 50:50 per gig_type |
| Control Group | Budget manual berdasarkan rolling mean 4 minggu income historis |
| Treatment Group | Budget adaptif berdasarkan predicted income (Income Predictor) |
| N Control | 1,502 user |
| N Treatment | 1,498 user |
| **Primary Metric** | `mean_budget_error` — rata-rata selisih absolut antara planned budget dan ideal budget (actual_income × BUDGET_RATIO) |
| Secondary Metrics | `budget_adherence_rate`, `over_budget_rate`, `expense_to_income_ratio`, `saving_allocation_rate`, `budget_gap` |

## 3. Hipotesis

- **H0**: mean_budget_error Treatment = Control
- **H1**: mean_budget_error Treatment < Control (one-tailed)
- Significance level: alpha = 0.05
- Interpretasi: nilai lebih kecil = budget planning lebih akurat

## 4. Statistik Deskriptif — Primary Metric

| Metrik | Control | Treatment |
|--------|---------|-----------|
| N | 1,502 | 1,498 |
| Mean Budget Error | Rp 47rb | Rp 14rb |
| Median Budget Error | Rp 36rb | Rp 10rb |
| Std Dev Budget Error | Rp 36rb | Rp 13rb |
| Absolute Diff (T-C) | — | Rp -33rb |
| Relative Change | — | -70.14% |

## 5. Secondary Metric: budget_adherence_rate

| Metrik | Control | Treatment | Diff |
|--------|---------|-----------|------|
| Budget Adherence Rate | 46.17% | 43.19% | -2.98pp |
| Over-Budget Rate | 53.83% | 56.81% | — |

> **Interpretasi**: Jika budget adherence Treatment lebih rendah dari Control, hal ini tidak
> berarti Income Predictor gagal. Akurasi budget (mean_budget_error) tidak otomatis mengubah
> perilaku pengeluaran user. Budget adherence dipengaruhi oleh kepatuhan user terhadap
> rekomendasi, yang memerlukan validasi terpisah melalui eksperimen live.

## 6. Uji Asumsi

| Uji | Statistic | p-value | Hasil |
|-----|-----------|---------|-------|
| Shapiro-Wilk (Control) | 0.8603 | 0.000000 | Tidak Normal |
| Shapiro-Wilk (Treatment) | 0.6782 | 0.000000 | Tidak Normal |
| Levene | 538.1740 | 0.000000 | Tidak Homogen |

> Uji utama yang dipilih: **Mann-Whitney U** (berdasarkan hasil uji asumsi di atas)

## 7. Hasil Uji Hipotesis

| Uji | Statistic | p-value | Keputusan | Peran |
|-----|-----------|---------|-----------|-------|
| Mann-Whitney U (alternative=less) | 288517 | 0.000000 | Tolak H0 | **Utama** |
| Welch t-test (one-tailed: T < C) | -33.3843 | 0.000000 | Tolak H0 | Pendukung |

## 8. Effect Size & Confidence Interval

- **Cohen's d** = -1.2188 → Efek Besar (Treatment lebih baik (d negatif = budget error lebih rendah))
- **Absolute Difference** (T-C) = Rp -33rb
- **Relative Change** = -70.14%
- **95% CI (Welch)**: [Rp -35rb, Rp -31rb]
- **CI Interpretation**: Seluruh CI negatif → Treatment secara statistik memiliki budget error lebih rendah.

## 9. Power Analysis

- **Power yang dicapai** dengan n=1498: **1.0000** (Cukup >= 0.80)

## 10. Subgroup Analysis

> Hasil subgroup bersifat **eksploratorif**. Jangan dijadikan klaim utama.

| Gig Type | n_ctrl | n_treat | BE Control | BE Treatment | Rel Reduction | MW p | Indikasi |
|----------|--------|---------|------------|--------------|---------------|------|----------|
| content_creator | 139 | 138 | Rp 42rb | Rp 10rb | -75.3% | 0.0000 | positif |
| freelance_desain | 230 | 229 | Rp 64rb | Rp 19rb | -71.0% | 0.0000 | positif |
| freelance_it | 180 | 180 | Rp 84rb | Rp 23rb | -72.0% | 0.0000 | positif |
| jualan_online | 248 | 248 | Rp 33rb | Rp 10rb | -70.1% | 0.0000 | positif |
| kurir | 113 | 112 | Rp 32rb | Rp 11rb | -66.0% | 0.0000 | positif |
| ojek_online | 115 | 114 | Rp 33rb | Rp 11rb | -66.5% | 0.0000 | positif |
| pekerja_harian | 249 | 249 | Rp 40rb | Rp 13rb | -68.5% | 0.0000 | positif |
| tutor | 228 | 228 | Rp 40rb | Rp 13rb | -67.5% | 0.0000 | positif |

## 11. Kesimpulan

Simulasi A/B Testing menunjukkan bahwa penggunaan Income Predictor sebagai dasar Budget Planner adaptif dapat menurunkan budget error dibandingkan budgeting manual. Hal ini menunjukkan bahwa Income Predictor membantu menghasilkan rencana budget yang lebih akurat terhadap kondisi income aktual. Uji Mann-Whitney U menghasilkan p-value = 0.000000 (< alpha=0.05), sehingga H0 ditolak. Relative reduction budget error sebesar -70.14% mengindikasikan efek yang bermakna (Cohen's d = -1.2188, Besar).

Namun, peningkatan akurasi budget belum otomatis menurunkan over-budget rate atau meningkatkan budget adherence, karena perilaku pengeluaran pengguna tetap dipengaruhi oleh kepatuhan terhadap rekomendasi. Dampak terhadap budget adherence dan over-budget rate perlu divalidasi lebih lanjut melalui eksperimen live.

Karena data yang digunakan bersifat synthetic, hasil ini harus dipahami sebagai proof-of-concept dan masih memerlukan validasi dengan eksperimen live pada pengguna nyata.

## 12. Rekomendasi

1. **Lanjutkan dengan eksperimen live** pada pengguna nyata untuk validasi kausal.
2. **Perbesar sample size** agar power >= 0.80 dapat dicapai untuk effect size yang relevan.
3. **Gunakan metrik behavioral yang lebih lengkap**: notification_response_rate, app_engagement,
   impulsive_transaction_count, plan_revision_frequency.
4. **Validasi budget adherence secara dedicated** — uji terpisah dengan desain yang dirancang
   untuk mengukur perubahan perilaku pengeluaran, bukan hanya akurasi perencanaan.
5. **Jangan rollout berdasarkan data synthetic ini** — hasil ini adalah proof-of-concept,
   bukan bukti efektivitas fitur di dunia nyata.

---

> *"Income Predictor tidak terbukti langsung meningkatkan budget adherence, tetapi berpotensi*
> *meningkatkan akurasi budget planning karena Treatment menghasilkan budget error yang lebih*
> *rendah dibanding budgeting manual. Karena data synthetic, hasil tetap harus dianggap*
> *proof-of-concept dan perlu validasi live experiment."*