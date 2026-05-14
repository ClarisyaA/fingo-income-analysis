# Laporan Proporsi Data, Split & Validasi Bias (v9)

## Ringkasan Dataset
| Informasi | Nilai |
| --- | --- |
| Versi pipeline | v9-FINAL |
| Total baris | 28,600 |
| Total user | 550 |
| Minggu per user | 52 |
| N_YEAR referensi | 2025 |
| Ramadan minggu | 9–12 |
| Distribusi | Log-Normal AR(1) log-space |
| Kaggle sources | 4 dataset |
| BPS sources | 4 dataset, 9 provinsi diparse |
| Skillstack premium ratio | 2.17x |
| BPS Nasional Bebas | Rp 1,652,500/bulan |
| BPS DKI Bebas | Rp 2,663,600/bulan |
| Data leakage fix | Scaler fit hanya di minggu 1–36 |
| Feature baru v9 | lag_8w, lag_12w, week_sin, week_cos |

## Proporsi Data
| Kategori | Baris | Persentase |
| --- | --- | --- |
| Sintetis | 26,000 | 90.9% |
| Survei (real) | 2,600 | 9.1% |
| Total | 28,600 | 100.0% |

## Chronological Split (v9: + metadata musiman)
| Set | Minggu | Baris | Persentase | Musim yang Tercakup |
| --- | --- | --- | --- | --- |
| Train | 1–36 | 19,800 | 69.2% | Low Season, Normal, Ramadan, Lebaran |
| Validation | 37–44 | 4,400 | 15.4% | Normal |
| Test | 45–52 | 4,400 | 15.4% | Harbolnas, Year-end |

## Benchmark per Gig Type (BPS Dynamically Corrected)
| Gig Type | Mean/Minggu | BPS Correction | Sumber |
| --- | --- | --- | --- |
| ojek_online | Rp 380rb | 0.619x | IDinsight 2025 net income ojek online Indonesia |
| kurir | Rp 342rb | 0.619x | IDinsight 2025 kurir + CELIOS 2024 |
| jualan_online | Rp 257rb | 0.619x | CELIOS 2024 pedagang online Indonesia |
| freelancer_desain | Rp 456rb | 0.619x | Sakernas Jakarta 2023 + Fastwork.id rate card |
| freelancer_it | Rp 599rb | 0.619x | Sakernas Jakarta 2023 IT freelancer + Glints 2024 |
| content_creator | Rp 413rb | 0.619x | CELIOS 2024 + Creator Economy Indonesia 2024 |