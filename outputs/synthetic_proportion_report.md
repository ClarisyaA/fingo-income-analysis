# Synthetic Proportion Report — Fingo Income Dataset

## Kalibrasi
Dataset ini menggunakan **Indonesia-validated calibration** berdasarkan:
- IDinsight 2025: net monthly income platform driver
- Sakernas Jakarta 2023 (Arafat et al.): upah per jam per sektor gig
- CELIOS 2024: rata-rata net income driver daring

## Distribusi gig_type
- content_creator: 18 user (9%), mean Rp1,025,281/minggu
- freelancer_desain: 19 user (10%), mean Rp1,332,099/minggu
- freelancer_it: 58 user (29%), mean Rp1,562,921/minggu
- jualan_online: 23 user (12%), mean Rp897,833/minggu
- kurir: 28 user (14%), mean Rp756,436/minggu
- ojek_online: 54 user (27%), mean Rp698,553/minggu

## Catatan kalibrasi income
| gig_type | mu (mean/minggu) | Sumber |
|---|---|---|
| ojek_online | Rp700,000 | IDinsight 2025 net + Sakernas Jakarta transport |
| kurir | Rp730,000 | IDinsight 2025 net + CELIOS 2024 |
| freelancer_it | Rp1,550,000 | Sakernas Jakarta 2023 — sektor informasi & komunikasi |
| freelancer_desain | Rp1,250,000 | Sakernas Jakarta 2023 — sektor jasa perusahaan |
| content_creator | Rp1,100,000 | Estimasi: midpoint skilled gig Jakarta, high volatility |
| jualan_online | Rp900,000 | IDinsight 2025: casual Rp2.515jt + self-employed Rp4.098jt/bln |
