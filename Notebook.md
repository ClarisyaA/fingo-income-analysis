# Dokumentasi Menyeluruh — Fingo DS2: Income Predictor Data Pipeline
**Tim:** CC26-PSU217 | **Role:** Data Scientist 2 — Clarisya Adeline  
**Versi Notebook:**  | **Tujuan:** End-to-end Data Wrangling untuk Fitur 3 Fingo (Income Predictor)

---

## Gambaran Besar

Notebook ini membangun **dataset time-series pendapatan mingguan gig worker Indonesia** yang siap dipakai untuk melatih model prediksi (target: LSTM). Karena tidak ada dataset publik yang spesifik untuk gig worker Indonesia dengan time-series 52 minggu, pendekatan yang dipakai adalah:

1. **Kalibrasi benchmark** dari publikasi resmi Indonesia (BPS, IDinsight, Sakernas)
2. **Ekstraksi statistik (mu, sigma, CoV)** dari 4 dataset Kaggle global sebagai referensi distribusi
3. **Generate data sintetis** 300 user × 52 minggu dengan distribusi Log-Normal + AR(1) yang sudah disesuaikan ke konteks Indonesia
4. **Merge data survei primer** (form_responses.csv) jika tersedia
5. **Validasi 6 bias test** sebelum data dianggap layak

Output akhir adalah `income_clean.csv` (± 15.600 baris) beserta train/val/test split kronologis.

---

## Bagian 0 — Setup & Clone GitHub

### Yang Dilakukan
- Clone atau pull repo `fingo-income-analysis` dari GitHub milik `ClarisyaA`
- Sinkronisasi working tree dengan `git reset --hard origin/main` untuk memastikan tidak ada file stale
- Install library tambahan: `faker`, `scipy`
- Import semua library (stdlib → 3rd-party, urutan PEP 8)
- Definisikan **konstanta global** yang dipakai di seluruh notebook

### Konstanta Kunci & Penjelasannya

| Konstanta | Nilai | Penjelasan |
|---|---|---|
| `USD_TO_IDR` | 17.252 | Kurs tengah Bank Indonesia (USD → IDR). Dipakai untuk mengkonversi income USD dari dataset Kaggle ke Rupiah |
| `INR_TO_IDR` | 183 | Kurs INR (Rupee India) → IDR. Dipakai untuk dataset delivery_boy_salary.csv yang bersumber dari India |
| `INDIA_ADAPT` | 0.55 | Faktor adaptasi Purchasing Power Parity (PPP) India → Indonesia. Income India dikalikan 0.55 karena biaya hidup Indonesia ≈ 55% dari India di sektor gig |
| `SANITY_MIN_MONTHLY_IDR` | 500.000 | Batas bawah wajar income bulanan pekerja informal Indonesia (dari BPS). Di bawah ini dianggap parsing error |
| `SANITY_MAX_MONTHLY_IDR` | 10.000.000 | Batas atas wajar income bulanan pekerja informal Indonesia. Di atas ini dianggap outlier atau error parsing |
| `RIBUAN_THRESHOLD_IDR` | 100.000 | Threshold untuk deteksi otomatis apakah nilai BPS dalam ribu rupiah atau rupiah penuh |
| `RANDOM_SEED` | 42 | Seed untuk reproducibility di semua proses random |

---

## Bagian 1 — Gathering Data

### Sumber Data yang Digunakan

#### 4 Dataset Kaggle (Data Global)
Dataset Kaggle **tidak dipakai langsung sebagai income** untuk data sintetis. Fungsinya adalah **mengekstrak statistik distribusi (CoV = std/mean)** untuk mengkalibrasi volatilitas income per gig type.

| Dataset | File | Mata Uang | Relevansi |
|---|---|---|---|
| Freelancer Work Patterns | `Freelancer_Work_Patterns_Income_Prediction_Dataset.csv` | USD | CoV untuk freelancer_it, freelancer_desain, content_creator |
| Freelancer Earnings BD | `freelancer_earnings_bd.csv` | USD | CoV tambahan + rasio experience (Beginner vs Expert) |
| Delivery Boy Salary | `delivery_boy_salary.csv` | INR (India) | CoV untuk ojek_online dan kurir, dikonversi + adaptasi PPP |
| Freelancer Earnings vs Skillstack | `freelancer_earnings_vs_skillstack_dataset.csv` | USD/annual | Skill premium ratio (senior vs junior), CoV per kategori skill |

#### 4 Dataset BPS (Data Indonesia)
Dataset BPS digunakan sebagai **ground truth benchmark nasional** untuk memvalidasi apakah income sintetis yang dihasilkan sesuai kenyataan Indonesia.

| Dataset | File | Fungsi |
|---|---|---|
| BPS Pekerja Bebas 2025 | `Rata-Rata Pendapatan Bersih Sebulan Pekerja Informal...2025.csv` | Benchmark terbaru nasional + per provinsi |
| BPS Pekerja Bebas 2024 (CLEAN) | `bps_pekerja_bebas_2024_clean.csv` | Benchmark utama (format sudah dibersihkan di v8) |
| BPS Pekerja Informal 2025 | Sama dengan file 2025 | Validasi silang |
| BPS Pekerja Informal 2023 | `...2023.csv` | Baseline historis |

#### Data Survei Primer
- `form_responses.csv` — hasil Google Form survei lapangan dari gig worker. Dimuat otomatis jika tersedia. Jika tidak ada, 100% data sintetis.

### Utility Baru v8: `clean_bps_csv()`
Fungsi untuk membersihkan CSV BPS mentah (multi-row header, format ribuan rupiah) menjadi format bersih dengan kolom snake_case dan nilai dalam rupiah penuh. Disediakan sebagai alat bantu untuk penggunaan di masa depan.

---

## Bagian 2 — Assessing Data

### Yang Dilakukan
- Evaluasi kualitas setiap dataset: shape, tipe data, missing values, duplikat
- Identifikasi isu utama secara otomatis:
  - Dataset Kaggle: income dalam USD/global (bukan time-series Indonesia)
  - Delivery: data India (INR), ada outlier ekstrem
  - BPS: format tabel multi-header, perlu parsing khusus

### Output Assessing
Tabel ringkasan `df_summary` yang menampilkan Missing Values, Duplikat, dan Isu Utama per dataset — memudahkan keputusan cleaning berikutnya.

---

## Bagian 3 — Cleaning & Domain Adaptation

Ini adalah langkah paling kritis. Setiap dataset dibersihkan dan diadaptasi ke konteks Indonesia.

### CELL 3.1 — Cleaning Dataset 1: Freelancer Work Patterns (USD → IDR)

**Sumber:** Dataset Kaggle global dengan income dalam USD.

**Yang Dilakukan:**
- Konversi `monthly_income_usd` × `USD_TO_IDR` → `monthly_income_idr`
- Turunkan ke mingguan: `monthly_income_idr / 4.345`
- Map `primary_skill` ke `gig_type` Indonesia (contoh: "Graphic Design" → `freelancer_desain`)
- Buat `experience_tier` (junior/mid/senior) dari `years_experience`
- Hitung CoV (std/mean) per gig_type → masuk ke kalibrasi volatilitas

**Mengapa dibagi 4.345?** Rata-rata minggu per bulan = 365.25/12/7 ≈ 4.345. Ini lebih akurat dari 4.333 karena memperhitungkan tahun kabisat.

### CELL 3.2 — Cleaning Dataset 2: Freelancer Earnings BD (USD → IDR)

**Sumber:** Dataset Kaggle global, kolom `Earnings_USD`.

**Yang Dilakukan:**
- Konversi USD → IDR → weekly
- Map `Job_Category` ke `gig_type` Indonesia
- Hitung rasio Expert/Beginner income (dipakai untuk validasi experience multiplier)
- Hitung CoV per gig_type

### CELL 3.3 — Cleaning Dataset 3: Delivery Boy Salary (INR India → IDR Indonesia)

**Sumber:** Dataset India dengan salary dalam Rupee (INR).

**Pipeline konversi berlapis:**
```
Salary (INR) × INR_TO_IDR (183) × INDIA_ADAPT (0.55) = Monthly Gross IDR
Monthly Gross IDR × NET_GROSS_RATIO (0.584) = Monthly Net IDR
Monthly Net IDR / 4.345 = Weekly Net IDR
```

**NET_GROSS_RATIO = 2.668.261 / 4.564.083 = 0.584** berasal dari perbandingan data IDinsight 2025 (net income ojek online Indonesia) vs estimasi gross income rata-rata. Ini dipakai karena dataset India adalah gross salary, bukan net income.

**Penghapusan outlier:** IQR method dengan batas atas Q3 + 3×IQR (lebih longgar dari 1.5×IQR biasa karena distribusi income gig worker sangat skewed).

**Map platform India → Indonesia:** Zomato → GoFood, Swiggy → ShopeeFood, DoorDash → GoFood, dst.

**Deteksi ojek_online vs kurir:** dari kolom `peak_hours` — jika ada jam puncak = ojek_online, lainnya = kurir.

### CELL 3.4 — Cleaning Dataset 4: Freelancer Earnings vs Skillstack (USD → IDR)

**Sumber:** Dataset Kaggle dengan income dalam berbagai unit (hourly/monthly/annual USD).

**Deteksi otomatis unit income:**
- Median < 1.000 → hourly rate → weekly = rate × 40 jam
- Median 1.000–10.000 → monthly → weekly = / 4.345
- Median > 10.000 → annual → weekly = / 52

**Fungsi utama dataset ini:** menghitung **Skill Premium Ratio** (income tertinggi / terendah per experience level) dan CoV per kategori skill.

### CELL 3.5 — Cleaning & Parsing Dataset BPS

**Dua jalur eksekusi (v8):**

**Fast Path** (CSV sudah bersih): Deteksi otomatis jika CSV punya kolom `provinsi` (snake_case) tanpa `Unnamed:N`. Langsung pilih kolom `jumlah_agustus` atau setara.

**Slow Path** (CSV masih messy): Parser lama yang robust — skip baris header bertingkat, deteksi format angka English vs Indonesia (titik vs koma), deteksi unit ribu rupiah vs rupiah penuh.

**Output:** Nilai rata-rata income per bulan untuk provinsi: Indonesia (nasional), DKI Jakarta, Jawa Barat — dipakai sebagai anchor validasi.

---

## Bagian 4 — Kalibrasi Parameter & Benchmark Indonesia

### CELL 4.1 — Tabel Benchmark Final

Inilah jantung dari seluruh notebook. **Benchmark ini adalah nilai yang menjadi target distribusi data sintetis.**

#### Asal-Usul Benchmark India (INR) — Penjelasan Lengkap

Dataset `delivery_boy_salary.csv` berasal dari India dengan income dalam INR. Pipeline adaptasinya:

1. **INR_TO_IDR = 183**: Kurs pasar INR ke IDR (referensi Bank Indonesia/XE.com)
2. **INDIA_ADAPT = 0.55**: Faktor PPP (Purchasing Power Parity). India dan Indonesia memiliki struktur biaya hidup berbeda. Berdasarkan data World Bank PPP 2023, daya beli Rp 1 di Indonesia setara ≈ 55% dari 1 Rupee di India untuk sektor jasa informal. Faktor ini memastikan income yang dikonversi mencerminkan daya beli nyata gig worker Indonesia, bukan sekedar konversi kurs langsung.

#### Asal-Usul Benchmark USD — Penjelasan Lengkap

Dataset Kaggle 1, 2, 4 menggunakan USD. Konversi langsung dengan kurs: **USD_TO_IDR = 17.252** (kurs tengah BI pada saat pengembangan). Income USD dari Kaggle **tidak dipakai sebagai target benchmark** langsung karena terlalu tinggi untuk konteks Indonesia. Income USD Kaggle hanya dipakai untuk:
- Menghitung CoV (proporsi volatilitas, bukan nilai absolut)
- Menghitung skill premium ratio (perbandingan level, bukan nilai absolut)

#### Benchmark Indonesia per Gig Type (Mingguan, IDR)

| Gig Type | Mu (Rp/minggu) | Sigma | Min | Max | Sumber Utama |
|---|---|---|---|---|---|
| ojek_online | 700.000 | 220.000 | 250.000 | 1.800.000 | IDinsight DERII 2025 + Sakernas Jakarta transport |
| kurir | 730.000 | 200.000 | 250.000 | 1.800.000 | IDinsight DERII 2025 + CELIOS 2024 |
| freelancer_it | 1.550.000 | 700.000 | 300.000 | 5.500.000 | Sakernas Jakarta 2023 — sektor informasi & komunikasi |
| freelancer_desain | 1.250.000 | 600.000 | 200.000 | 4.500.000 | Sakernas Jakarta 2023 — sektor jasa perusahaan |
| content_creator | 1.100.000 | 900.000 | 50.000 | 6.000.000 | Estimasi midpoint transport & skilled |
| jualan_online | 900.000 | 450.000 | 100.000 | 4.000.000 | IDinsight 2025 casual + self-employed average |

#### Referensi Benchmark yang Digunakan

| Sumber | Tahun | Yang Diambil |
|---|---|---|
| **IDinsight DERII Gig Worker Survey** | 2025 | Net income ojek_online (Rp 700rb/minggu) dan kurir (Rp 730rb/minggu). Survei langsung pada 1.000+ gig worker Indonesia. |
| **Arafat et al. — Sakernas Jakarta** | 2023 | Income freelancer IT (sektor informasi & komunikasi Rp 1,55jt/minggu) dan desain (sektor jasa perusahaan Rp 1,25jt/minggu). Sakernas = Survei Angkatan Kerja Nasional BPS. |
| **Katadata/CELIOS** | 2024 | Validasi range keseluruhan dan income kurir/ojek. CELIOS = Center of Economic and Law Studies. |
| **BPS Pekerja Bebas & Informal** | 2023-2025 | Validasi benchmark per provinsi. BPS Nasional Bebas ≈ Rp 2,4jt/bulan → ≈ Rp 552rb/minggu (± wajar dengan benchmark ojek_online Rp 700rb karena DKI lebih tinggi dari nasional). |
| **Kaggle Freelancer vs Skillstack** | 2024 | Skill premium ratio: berapa kali lipat income senior vs junior. |

#### Validasi Benchmark vs BPS
Benchmark mingguan divalidasi terhadap BPS bulanan (/4.345):
- Ratio yang wajar: 0.5x – 3.0x dari BPS nasional per minggu
- Income ojek_online Rp 700rb/minggu vs BPS nasional ≈ Rp 552rb/minggu → rasio 1.27x ✓ (masuk akal, ojek lebih tinggi dari rata-rata pekerja bebas karena efisiensi platform)

### CELL 4.2 — Kalibrasi CoV (Volatilitas)

CoV (Coefficient of Variation = std/mean) dari 4 dataset Kaggle digabungkan menjadi `VOLATILITY_MAP`. Ini menentukan **seberapa fluktuatif income** setiap gig_type dalam data sintetis.

**VOLATILITY_MAP diclip ke [0.15, 0.65]** untuk menghindari distribusi terlalu datar atau terlalu ekstrem.

### CELL 4.3 — Parameter Kalibrasi Lainnya

| Parameter | Nilai | Penjelasan |
|---|---|---|
| `EXPERIENCE_MULTIPLIER` | junior=0.65, mid=1.00, senior=1.45 | Multiplier terhadap mu benchmark. Senior mendapat 1.45× income mid. Dari skill premium ratio dataset Kaggle Skillstack. |
| `AR1_COEF` | 0.45 | Koefisien autokorelasi AR(1) dalam log-space. Menghasilkan lag-1 AC ≈ 0.35-0.40 (target 0.20-0.60). Nilai 0.45 dipilih setelah iterasi untuk melewati Bias Test 5. |
| `SEASONAL_MULT` | dict per gig_type per periode | Multiplier musiman. Contoh: kurir naik 20% saat Ramadan (lebih banyak pesanan makanan), turun 35% saat Lebaran (orang libur). |
| `PAYDAY_MULT` | dict per gig_type | Efek gajian di minggu ke-4 bulan. Ojek_online naik 18% karena lebih banyak orang keluar setelah gajian. |

**Seasonal Label Assignment:**
- Minggu 1-6: low_season (awal tahun sepi)
- Minggu 7-9: normal
- Minggu 10-13: ramadan
- Minggu 14-15: lebaran
- Minggu 16-44: normal
- Minggu 45-46: harbolnas (11.11, 12.12)
- Minggu 47-48: normal
- Minggu 49-52: yearend

---

## Bagian 5 — EDA Dataset Kaggle

### CELL 5.1 — Kaggle Raw vs Benchmark Indonesia
Bar chart membandingkan income Kaggle sebelum override (terlalu tinggi untuk Indonesia) vs benchmark Indonesia final. Ini memvisualisasikan mengapa income Kaggle tidak bisa dipakai langsung.

### CELL 5.2 — Boxplot Delivery Dataset
Visualisasi distribusi income dataset delivery yang sudah diadaptasi ke Indonesia. Pola Log-Normal terlihat dari distribusi histogram yang right-skewed.

### CELL 5.3 — EDA Skillstack
3 panel:
1. KDE distribusi income per experience level
2. Bar chart skill premium (rata-rata income per experience tier)
3. CoV per kategori skill (ada fallback ke histogram jika cov_df4 kosong)

### CELL 5.4 — Visualisasi Benchmark BPS per Provinsi
Bar chart horizontal income rata-rata per provinsi dari dataset BPS. DKI Jakarta dihighlight merah sebagai referensi. Ada fallback manual jika parsing BPS gagal.

---

## Bagian 6 — Generate Data Sintetis Time-Series

**Target:** 300 user × 52 minggu = 15.600 baris.

### CELL 6.1 — Konfigurasi Distribusi

**Distribusi gig_type:**
- ojek_online: 30%, kurir: 20%, jualan_online: 20%, freelancer_it: 10%, freelancer_desain: 10%, content_creator: 10%

**Distribusi experience:**
- junior: 35%, mid: 45%, senior: 20%

**Region multiplier:** jabodetabek (1.10×) sampai lainnya (0.82×) — mencerminkan perbedaan upah antar wilayah.

### CELL 6.2 — Generate User Profiles

Untuk setiap user dibuat:
- `mu_user` = `bench['mu']` × `exp_mult` × `region_mult` × `personal_mu_factor`
- `personal_mu_factor` ~ LogNormal(0, 0.10) → variasi heterogeneitas antar user
- `sigma_ln`, `mu_ln` → parameter distribusi Log-Normal dalam log-space

### CELL 6.3 — Generate Time-Series (AR(1) di Log-Space) 

**Persamaan AR(1) proper dalam log-space:**
```
sigma_innov = sigma_ln × sqrt(1 - AR1_COEF²)     # variance stationary
log_inc[0]  ~ N(mu_ln, sigma_ln²)
log_inc[w]  = mu_ln + AR1_COEF × (log_inc[w-1] - mu_ln) + N(0, sigma_innov²)
income      = exp(log_inc) × seasonal_mult × payday_mult
```

**Mengapa di log-space?** AR(1) dalam log-space menjaga distribusi log-normal tetap stationary (mean-reverting). Jika AR(1) diterapkan pada income langsung (linear), income bisa drift ke nilai negatif atau tak terbatas. Dengan log-space, autokorelasi lag-1 mendekati AR1_COEF yang diinginkan (0.20-0.60 untuk Bias Test 5 PASS).

---

## Bagian 7 — Feature Engineering

Fitur-fitur yang dibangun dari time-series income:

| Fitur | Formula | Fungsi untuk Model |
|---|---|---|
| `rolling_mean_4w` | rolling(4).mean() per user | Baseline income 4 minggu terakhir (trend jangka pendek) |
| `rolling_std_4w` | rolling(4).std() | Volatilitas jangka pendek |
| `rolling_cov_8w` | rolling(8).std() / rolling(8).mean() | Volatilitas jangka menengah |
| `income_volatility` | std/mean seluruh 52 minggu | Karakteristik volatilitas user (konstan per user) |
| `lag_1w`, `lag_2w`, `lag_4w` | shift(1), shift(2), shift(4) | History income — input kunci LSTM |
| `income_vs_rolling` | (income - rolling_mean) / rolling_mean | Deviasi dari baseline |
| `income_growth_1w` | (income - prev) / prev | Persentase pertumbuhan minggu ke minggu |
| `seasonal_income_pattern` | map dari seasonal_label | Versi numerik periode musiman |
| `is_payday_week` | 1 jika week_of_month == 4 | Flag minggu gajian |
| Dummy gig_type | gig_ojek_online, dll. | One-hot encoding gig type |
| Dummy experience | exp_junior, dll. | One-hot encoding experience |

---

## Bagian 8 — Merge Data Survei

### CELL 8.1 — Mapping Survei

Setiap kolom Google Form dimapping ke nilai numerik/kategori yang konsisten dengan data sintetis.
- Menggunakan **en-dash (U+2013)** bukan hyphen biasa untuk range income (sesuai output Google Forms)
- Tambahan opsi gig_type: "Pekerja harian" → jualan_online, "Tutor" → freelancer_desain
- Region tambahan: Jatinangor, Sumedang → jawa_barat_lainnya; Lampung → sumatera

### CELL 8.2 — Fuzzy Column Matching & Merge

**Masalah:** Header CSV dari Google Forms mengandung pertanyaan panjang dengan newline ganda. Matching exact string sering gagal.

**Solusi:** Fungsi `find_col_by_keywords()` yang mencari kolom berdasarkan keyword (case-insensitive, normalized whitespace).

**Strategi 4-minggu real data:** Jika responden mengisi data W1-W4 (income 4 minggu terakhir), data real ini dipakai untuk minggu 1-4 dalam series 52 minggu. Sisanya diproyeksikan dengan seasonal multiplier.

### CELL 8.3 — Gabungkan Sintetis + Survei

Data survei diberi prefix `SRV_XXXX`, sintetis `SYN_XXXX`. Keduanya digabung dengan `pd.concat`. Feature engineering dasar (rolling, lag) di-set ke 0 untuk data survei karena tidak ada history sebelumnya.

---

## Bagian 9 — EDA Data Final

6 visualisasi utama:
1. **Bar chart mean income per gig_type** — validasi visual benchmark
2. **Bar chart income per gig × experience** — membuktikan senior > mid > junior (BQ5)
3. **Time-series 52 minggu per gig_type** — pola musiman terlihat jelas (BQ4)
4. **Heatmap gig × minggu dalam bulan** — efek gajian minggu ke-4 (BQ4)
5. **Boxplot volatilitas income per gig** — content_creator paling volatil (BQ5)
6. **Correlation heatmap fitur** — lag_1w, rolling_mean_4w berkorelasi tinggi dengan income (input model LSTM)

---

## Bagian 10 — Bias Testing & Validasi

Target minimum: 5/6 test PASS PENUH.

### Test 1 — Mean vs Benchmark (threshold ±15%)
Memastikan mean income sintetis per gig_type tidak drift jauh dari benchmark IDinsight/Sakernas. Kegagalan → ada bug di parameter mu atau experience multiplier.

### Test 2 — KS Test vs Log-Normal Teoritis (p-value > 0.01)
Kolmogorov-Smirnov test: apakah distribusi income sintetis benar-benar Log-Normal? Catatan: p-value rendah masih wajar karena seasonal multiplier menggeser distribusi — bukan berarti data salah.

### Test 3 — Seasonal Direction
Apakah arah efek musiman benar? (Ramadan → kurir naik, bukan turun). Tidak mengecek magnitudo, hanya arah.

### Test 4 — Experience Multiplier (tolerance ±25%)
Rasio senior/junior aktual harus mendekati 1.45/0.65 = 2.23×. Toleransi 25% karena ada noise dari region multiplier dan personal_mu_factor.

### Test 5 — Autocorrelation AR(1) (target 0.20–0.60)
Lag-1 autocorrelation income series harus dalam range 0.20–0.60. Ini membuktikan AR(1) berfungsi dengan benar dalam log-space. Fix kritis v8 (AR1_COEF = 0.45 + proper log-space).

### Test 6 — BPS Range Validation
Monthly mean income per gig_type harus dalam range Rp 500rb – Rp 8jt/bulan. Range ini diambil dari threshold absolut BPS pekerja informal Indonesia (tidak tergantung hasil parsing BPS yang mungkin gagal).

---

## Bagian 11 — Normalisasi & Target

- **MinMaxScaler per user**: normalisasi income 0–1 per user (bukan global) karena income antar user sangat bervariasi. Scaler disimpan di `income_scalers.pkl` untuk inverse transform saat inference.
- **target_next_week**: `shift(-1)` dari income_amount → nilai yang diprediksi model. Baris terakhir setiap user bernilai NaN (tidak ada minggu berikutnya).

---

## Bagian 12 — Export & Chronological Split

**Chronological split** (bukan random split) wajib untuk time-series agar tidak ada data leakage:

| Set | Minggu | Proporsi |
|---|---|---|
| Train | 1–36 | 69% |
| Validation | 37–44 | 15% |
| Test | 45–52 | 15% |

File yang diexport:
- `income_clean.csv` — dataset final lengkap
- `income_train/val/test.csv` — split siap training
- `income_scalers.pkl` — scaler per user
- `synthetic_params.json` — parameter lengkap untuk reproducibility
- `synthetic_proportion_report.md` — laporan proporsi sintetis vs survei

---

## Bagian 13 — Data Dictionary

Dokumentasi 23 kolom dataset dalam format CSV dan Markdown, dibagi per kategori:
- **Identitas Pengguna:** user_id, gig_type, region, experience_tier, platform
- **Informasi Waktu:** week_number, week_of_month, seasonal_label, seasonal_income_pattern, is_payday_week
- **Pendapatan:** income_amount, income_normalized, income_growth_1w, income_vs_rolling
- **Feature Engineering:** rolling_mean_4w, rolling_std_4w, rolling_cov_8w, income_volatility, lag_1w, lag_2w, lag_4w
- **Target Model:** target_next_week
- **Metadata:** data_source

---

## Bagian 14 — Push ke GitHub

Strategi push dengan `--force-with-lease` (lebih aman dari `--force`):
1. Fetch origin untuk sync
2. Hapus file lama dari git index (`git rm --cached`)
3. Add file baru
4. Commit hanya jika ada perubahan
5. Verifikasi 22 file output tersedia sebelum push

---
