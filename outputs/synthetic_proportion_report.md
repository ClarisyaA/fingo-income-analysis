# Laporan Proporsi Data — income_clean.csv

Dibuat: 2026-04-26 10:43
Dibuat oleh: Clarisya Adeline (DS2) — Tim CC26-PSU217

## Ringkasan
| Kategori | Baris | Persentase |
|---|---|---|
| Data Sintetis | 10,400 | 100.0% |
| Data Survei (real) | 0 | 0.0% |
| **Total** | **10,400** | **100%** |

## Metodologi Data Sintetis
- N user: 200
- N minggu per user: 52
- Parameter kalibrasi: dari 3 dataset Kaggle
  (Freelancer Work Patterns, Freelancer Earnings BD, Delivery Boy Salary)
- Pola musiman Indonesia: Ramadan, Lebaran, post-Lebaran,
  akhir tahun, Januari-Februari, akhir bulan/gajian
- Random seed: 42 (reproducible)

## Distribusi Gig Type
gig_type
ojek_online          51
kurir                48
freelancer_it        32
jualan_online        27
freelancer_desain    24
content_creator      18

## Statistik Income Mingguan per Gig Type
                         mean         std      min        max
gig_type                                                     
content_creator    49096653.0  29773068.0    41000  184325000
freelancer_desain  36937067.0  24496977.0    68000  145409000
freelancer_it      40227795.0  21192929.0  7556000  144335000
jualan_online      35581402.0  25005445.0    49000  170137000
kurir               1216618.0    367552.0   496000    2996000
ojek_online         1211176.0    374850.0   390000    3082000
