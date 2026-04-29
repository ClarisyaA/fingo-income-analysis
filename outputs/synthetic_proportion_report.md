# Synthetic Proportion Report - Fingo Income Dataset
Data Scientist 2: Clarisya Adeline | Tim CC26-PSU217

## Ringkasan Dataset

| Informasi        |        Nilai |
| :--------------- | -----------: |
| Total baris      |       15,600 |
| Total user       |          300 |
| Minggu per user  |           52 |
| Distribusi       | Log-Normal AR(1) |

## Proporsi Data

| Kategori       |      Baris | Persentase |
| :------------- | ---------: | ---------: |
| Sintetis       |     15,600 |     100.0% |
| Survei (real)  |          0 |       0.0% |
| Total          |     15,600 |     100.0% |

## Benchmark Income

| Gig Type            |  Mean/Minggu | Sumber                                                     |
| :------------------ | -----------: | :--------------------------------------------------------- |
| Ojek Online         |     Rp 700rb | IDinsight 2025 net + Sakernas Jakarta transport            |
| Kurir               |     Rp 730rb | IDinsight 2025 net + CELIOS 2024                           |
| Freelancer It       |     Rp 1.6jt | Sakernas Jakarta 2023 - sektor informasi & komunikasi      |
| Freelancer Desain   |     Rp 1.2jt | Sakernas Jakarta 2023 - sektor jasa perusahaan             |
| Content Creator     |     Rp 1.1jt | Estimasi - midpoint transport & skilled                    |
| Jualan Online       |     Rp 900rb | IDinsight 2025 casual + self-employed average              |

## Hasil Bias Test (Mean vs Benchmark)

| Gig Type               |    Benchmark |       Aktual |    Diff% | Status |
| :--------------------- | -----------: | -----------: | -------: | :----- |
| Ojek Online            |     Rp 700rb |     Rp 703rb |    +0.4% | PASS   |
| Kurir                  |     Rp 730rb |     Rp 749rb |    +2.6% | PASS   |
| Freelancer It          |     Rp 1.6jt |     Rp 1.5jt |    -1.7% | PASS   |
| Freelancer Desain      |     Rp 1.2jt |     Rp 1.2jt |    -8.0% | PASS   |
| Content Creator        |     Rp 1.1jt |     Rp 1.1jt |    +2.5% | PASS   |
| Jualan Online          |     Rp 900rb |     Rp 968rb |    +7.6% | PASS   |

## Sumber Benchmark

| Sumber             | Link                                                                           |
| :----------------- | :----------------------------------------------------------------------------- |
| IDinsight 2025     | https://www.idinsight.org/article/who-are-gig-workers-insights-from-indonesia/ |
| Sakernas 2023      | https://scholarhub.ui.ac.id/jekk/vol2/iss1/3/                                  |
| Katadata/CELIOS    | https://databoks.katadata.co.id/ketenagakerjaan/                               |
