# Dokumentasi Notebook — Fingo DS2: Income Predictor Data Pipeline
**Tim:** CC26-PSU217 | **Role:** Data Scientist 2 — Clarisya Adeline  
**File Notebook:** `notebook.ipynb`  
**Judul Notebook:** Fingo DS2 - Kaggle Calibration + Synthetic Income Generator (FIXED)

---

## Gambaran Besar

Notebook ini membangun **dataset time-series pendapatan mingguan gig worker Indonesia** yang siap dipakai untuk melatih model prediksi LSTM (target: Fitur 3 Fingo — Income Predictor). Karena tidak ada dataset publik yang spesifik untuk gig worker Indonesia dengan time-series 52 minggu, pendekatan yang dipakai adalah:

1. **Kalibrasi benchmark** dari publikasi resmi Indonesia (BPS, IDinsight, Sakernas Jakarta)
2. **Ekstraksi statistik (CoV = std/mean)** dari 4 dataset Kaggle global sebagai referensi volatilitas distribusi
3. **Generate data sintetis** 300 user × 52 minggu dengan distribusi Log-Normal + AR(1) proper di log-space
4. **Merge data survei primer** (`form_responses.csv`) jika tersedia
5. **Validasi 6 bias test** sebelum data dianggap layak untuk modeling

Output akhir adalah `income_clean.csv` (±15.600 baris) beserta train/val/test split kronologis.

### Daftar Bagian Notebook

| Bagian | Isi |
|---|---|
| 0 | Setup & clone GitHub |
| 1 | Gathering Data — load 4 dataset Kaggle + 4 dataset BPS + form_responses.csv |
| 2 | Assessing Data — evaluasi kualitas & struktur |
| 3 | Cleaning & Domain Adaptation ke konteks Indonesia |
| 4 | Kalibrasi parameter benchmark (mu, sigma, CoV per gig_type) |
| 5 | EDA dataset Kaggle — Bar chart, Boxplot, Skill premium, BPS provinsi |
| 6 | Generate data sintetis 300 user × 52 minggu (Log-Normal AR(1) proper log-space) |
| 7 | Feature engineering (rolling, lag, volatility) |
| 8 | Mapping & merge form_responses.csv (FIXED — fuzzy column matching + exhaustive) |
| 9 | EDA data final + jawaban BQ4 & BQ5 |
| 10 | Bias testing (6 test — target 5/6 PASS PENUH) |
| 11 | MinMax scaling per user + kolom target_next_week |
| 12 | Export CSV (train/val/test split kronologis) |
| 13 | Data Dictionary (23 kolom) |
| 14 | Push ke GitHub (branch management + force-with-lease) |

---

## Bagian 0 — Setup & Clone GitHub

### CELL 0.1 — Clone/Pull Repo GitHub

Notebook di-setup untuk berjalan di Google Colab. Proses clone/pull dilakukan dengan logika branch management yang robust:

- `GITHUB_USERNAME = 'ClarisyaA'`
- `REPO_NAME = 'fingo-income-analysis'`
- `BRANCH_NAME = 'feature/income-predictor-base'`
- `LOCAL_DIR = '/content/fingo-income-analysis'`

**Logika branch (3 skenario):**
1. Branch sudah ada di local → `git checkout {BRANCH_NAME}` + `git pull`
2. Branch ada di remote tapi belum di local → `git checkout -b {BRANCH_NAME} origin/{BRANCH_NAME}`
3. Branch belum ada di mana-mana → checkout main, pull, buat branch baru

Token GitHub dibaca dari Colab Secrets (`userdata.get('GITHUB_TOKEN')`). Jika tidak ada, repo diasumsikan public.

### CELL 0.2 — Install Library Tambahan

```python
!pip install faker scipy --quiet
```

### CELL 0.3 — Import Library + Konstanta Global

**Library yang digunakan:**

| Library | Fungsi |
|---|---|
| `pandas` | Manipulasi DataFrame |
| `numpy` | Komputasi numerik dan generate distribusi |
| `matplotlib`, `seaborn` | Visualisasi data |
| `faker` (id_ID) | Generate nama/data palsu Indonesia |
| `sklearn.preprocessing.MinMaxScaler` | Normalisasi income per user |
| `scipy.stats` | Uji statistik (KS Test) |
| `json`, `pickle` | Export parameter dan scaler |

**Konstanta global yang didefinisikan:**

| Konstanta | Nilai Aktual | Penjelasan |
|---|---|---|
| `USD_TO_IDR` | `17_252` | Kurs tengah Bank Indonesia (USD → IDR) |
| `INR_TO_IDR` | `183` | Kurs INR (Rupee India) → IDR |
| `INDIA_ADAPT` | `0.23` | Faktor adaptasi PPP India → Indonesia |
| `RANDOM_SEED` | `42` | Seed numpy untuk reproducibility |

> **Catatan penting:** Nilai `INDIA_ADAPT = 0.23` berbeda dengan dokumentasi draft (`0.55`). Nilai yang aktual dipakai di notebook adalah **0.23**.

**Helper functions:**
- `fmt_idr(val)` — format angka ke string rupiah ringkas (`Rp 1.5jt`, `Rp 250rb`)
- `IDR_FORMATTER` — matplotlib ticker formatter untuk sumbu Y grafik

**Direktori output yang dibuat:**
- `data/raw/`, `data/processed/`, `data/synthetic/`, `outputs/charts/`

---

## Bagian 1 — Gathering Data

### Sumber Data

#### 4 Dataset Kaggle (sumber statistik distribusi — bukan income langsung)

Dataset Kaggle **tidak dipakai sebagai nilai income** untuk data sintetis. Fungsinya hanya **mengekstrak CoV (std/mean)** sebagai kalibrasi volatilitas per gig_type.

| Variabel | File | Mata Uang | Kegunaan |
|---|---|---|---|
| `df_freelancer` | `Freelancer_Work_Patterns_Income_Prediction_Dataset.csv` | USD | CoV untuk freelancer_it, freelancer_desain, content_creator |
| `df_earnings` | `freelancer_earnings_bd.csv` | USD | CoV + rasio Expert/Beginner |
| `df_delivery` | `delivery_boy_salary.csv` | INR (India) | CoV ojek_online & kurir, setelah adaptasi PPP |
| `df_skillstack` | `freelancer_earnings_vs_skillstack_dataset.csv` | USD/annual | Skill premium ratio (senior vs junior) + CoV per skill |

### CELL 1.1 — Load Dataset Kaggle

```python
PATH_RAW = 'data/raw/'
df_freelancer  = pd.read_csv(PATH_RAW + 'Freelancer_Work_Patterns_Income_Prediction_Dataset.csv')
df_earnings    = pd.read_csv(PATH_RAW + 'freelancer_earnings_bd.csv')
df_delivery    = pd.read_csv(PATH_RAW + 'delivery_boy_salary.csv')
df_skillstack  = pd.read_csv(PATH_RAW + 'freelancer_earnings_vs_skillstack_dataset.csv')

SURVEY_PATH      = PATH_RAW + 'form_responses.csv'
SURVEY_AVAILABLE = os.path.exists(SURVEY_PATH)
```

#### 4 Dataset BPS (ground truth benchmark Indonesia per provinsi)

| Key | File | Fungsi |
|---|---|---|
| `bps_bebas_2025` | `Rata-Rata Pendapatan Bersih Sebulan Pekerja Informal...2025.csv` | Benchmark terbaru nasional + per provinsi |
| `bps_bebas_2024` | `Rata-Rata_Pendapatan_Bersih_Sebulan_Pekerja_Bebas...2024.csv` | Benchmark utama (prioritas 1) |
| `bps_informal_2025` | File sama dengan `bps_bebas_2025` | Validasi silang |
| `bps_informal_2023` | `...2023.csv` | Baseline historis |

### CELL 1.2 — Load Dataset BPS

BPS dimuat dengan encoding fallback (utf-8 → latin-1) dan separator fallback (`;` → `,`). Jika file tidak ditemukan, key disimpan sebagai `None` dan di-skip pada bagian berikutnya.

---

## Bagian 2 — Assessing Data

### CELL 2.1 — Fungsi `assess_dataset()` (Dataset Kaggle)

Fungsi reusable yang menampilkan:
- Shape, info tipe data
- Statistik deskriptif (`df.describe()`)
- Missing values (hanya yang > 0)
- Jumlah duplikat

Dipanggil untuk ke-4 dataset Kaggle.

### CELL 2.2 — Fungsi `assess_bps()` (Dataset BPS)

Menampilkan shape, daftar kolom, missing values, duplikat, dan preview 3 baris pertama. Skip otomatis jika dataframe `None`.

### CELL 2.3 — Tabel Ringkasan Assessing

Membuat `df_summary` yang berisi kolom `Dataset`, `Missing Values`, `Duplikat`, dan `Isu Utama`. Isu utama dideteksi otomatis:
- Kolom mengandung `usd` → `'Income USD (global), bukan time-series'`
- Kolom mengandung `salary` → `'Data India (INR), ada outlier ekstrem'`
- Dataset BPS → `'Format tabel BPS per provinsi, perlu parsing'`

---

## Bagian 3 — Cleaning & Domain Adaptation

### CELL 3.1 — Cleaning Dataset 1: Freelancer Work Patterns

**Konversi mata uang:**
```python
df1['monthly_income_idr'] = df1['monthly_income_usd'] * USD_TO_IDR
df1['weekly_income_idr']  = df1['monthly_income_idr'] / 4.345
df1['hourly_rate_idr']    = df1['hourly_rate_usd'] * USD_TO_IDR
```
> Pembagi `4.345` = rata-rata minggu per bulan (365.25 / 12 / 7), lebih akurat dari 4.333.

**Mapping skill ke gig_type Indonesia:**

| primary_skill | gig_type |
|---|---|
| Graphic Design, Video Editing, UI/UX Design | `freelancer_desain` |
| Content Writing, Digital Marketing | `content_creator` |
| Web Development, Mobile App Development, Data Analysis, Machine Learning, Cloud Computing | `freelancer_it` |

**Experience tier** dari `years_experience`: `bins=[0,1,3,100]` → `['junior','mid','senior']`

**Output:** `cov_df1` — CoV per gig_type dari dataset ini.

### CELL 3.2 — Cleaning Dataset 2: Freelancer Earnings BD

**Mapping Job_Category ke gig_type:**

| Job_Category | gig_type |
|---|---|
| Web Development, App Development | `freelancer_it` |
| SEO, Digital Marketing, Content Writing | `content_creator` |
| Graphic Design | `freelancer_desain` |

**Output tambahan:** Rasio Expert/Beginner per gig_type (dari kolom `Experience_Level`).

### CELL 3.3 — Cleaning Dataset 3: Delivery Boy Salary (INR India → IDR)

**Penghapusan outlier (IQR Method):**
```python
upper = Q3 + 3 * IQR   # batas 3x IQR, lebih longgar karena distribusi sangat skewed
```

**Pipeline konversi berlapis:**
```
Salary (INR) × INR_TO_IDR (183) × INDIA_ADAPT (0.23) = Monthly Gross IDR
Monthly Gross IDR × NET_GROSS_RATIO (2_668_261 / 4_564_083) = Monthly Net IDR
Monthly Net IDR / 4.345 = Weekly Net IDR
```

**Mapping platform India → Indonesia:**

| Platform India | Platform Indonesia |
|---|---|
| Zomato | GoFood |
| Swiggy | ShopeeFood |
| DoorDash | GoFood |
| Deliveroo, Grab | Grab |
| Blinkit, Dunzo | GoSend |
| Zepto | J&T |
| Talabat | SiCepat |
| (tidak ada mapping) | Gojek |

**Klasifikasi gig_type:** Dari kolom `peak_hours` — nilai `yes/1/true` → `ojek_online`, lainnya → `kurir`.

### CELL 3.4 — Cleaning Dataset 4: Freelancer Earnings vs Skillstack (FIX)

**Deteksi otomatis kolom income** (prioritas: `Earnings_USD`, `hourly_rate`, `Annual_Income`, dsb.) dengan fallback keyword search jika nama exact tidak ditemukan.

**Deteksi unit income berdasarkan median:**
- Median < 1.000 → hourly rate → weekly = `× 40 jam`
- Median 1.000–10.000 → monthly → weekly = `/ 4.345`
- Median > 10.000 → annual → weekly = `/ 52`

**Deteksi kolom skill (FIX):** Kandidat: `Job_Category`, `Skill`, `Primary_Skill`, `Category`, `Niche`, `Specialization`, `Field`, dst. Fallback: kolom kategorikal dengan 3–50 unique values.

**Output:**
- `SKILLSTACK_PREMIUM_RATIO` — rasio income tertinggi/terendah per experience (default `2.0` jika gagal)
- `cov_df4` — CoV per kategori skill (dikosongkan jika single observation)
- `overall_cov_sk` — CoV keseluruhan skillstack

### CELL 3.5 — Parsing Dataset BPS (FIX)

**Fungsi `parse_bps(df, label)`** — self-contained parser untuk semua format CSV BPS:

1. Strip whitespace dari semua string
2. Konversi format angka Indonesia (`.` sebagai pemisah ribuan, `,` sebagai desimal) ke float
3. Pilih kolom nilai: prioritas kolom `L+P`/`total`/`jumlah`, fallback kolom numerik terakhir
4. **Deteksi skala dari median** (bukan baris pertama):
   - Median < 100.000 → dalam ribuan rupiah → kalikan 1.000
   - Median ≥ 100.000 → sudah rupiah penuh
5. Cari baris provinsi kunci: `Indonesia` (nasional), `DKI Jakarta`, `Jawa Barat`

**Output per dataset BPS:** `dict` berisi `{'indonesia': float, 'dki_jakarta': float, 'jawa_barat': float}`

---

## Bagian 4 — Kalibrasi Parameter + Benchmark Indonesia

### Referensi Benchmark

| No | Sumber | Tahun | Digunakan untuk |
|---|---|---|---|
| 1 | IDinsight DERII Gig Worker Survey | 2025 | Net income ojek_online & kurir |
| 2 | Arafat et al. — Sakernas Jakarta | 2023 | Income freelancer_it & freelancer_desain |
| 3 | Katadata/CELIOS | 2024 | Validasi range keseluruhan |
| 4 | BPS Pekerja Bebas & Informal | 2023–2025 | Validasi benchmark per provinsi |
| 5 | Kaggle Freelancer Earnings vs Skillstack | 2024 | Skill premium ratio |

### CELL 4.1 — Tabel Benchmark Final + Parameter Log-Normal

**Fungsi `get_bps_ref()`** mengambil nilai BPS dengan sanity check (500.000 ≤ val ≤ 15.000.000). Fallback ke nilai default jika di luar range:

```python
BPS_NASIONAL_BEBAS = get_bps_ref(['bps_bebas_2024','bps_bebas_2025'], 'indonesia', 2_400_000)
BPS_DKI_BEBAS      = get_bps_ref(['bps_bebas_2024','bps_bebas_2025'], 'dki_jakarta', 3_200_000)
BPS_NASIONAL_INF   = get_bps_ref(['bps_informal_2023','bps_informal_2025'], 'indonesia', 2_100_000)
BPS_DKI_INF        = get_bps_ref(['bps_informal_2023','bps_informal_2025'], 'dki_jakarta', 2_900_000)
```

**`ID_BENCHMARK` — Dictionary benchmark per gig_type (mingguan, IDR):**

| gig_type | mu (Rp/minggu) | sigma | min | max | Sumber Utama |
|---|---|---|---|---|---|
| `ojek_online` | 700.000 | 220.000 | 250.000 | 1.800.000 | IDinsight 2025 + Sakernas Jakarta transport |
| `kurir` | 730.000 | 200.000 | 250.000 | 1.800.000 | IDinsight 2025 + CELIOS 2024 |
| `freelancer_it` | 1.550.000 | 700.000 | 300.000 | 5.500.000 | Sakernas Jakarta 2023 — sektor informasi & komunikasi |
| `freelancer_desain` | 1.250.000 | 600.000 | 200.000 | 4.500.000 | Sakernas Jakarta 2023 — sektor jasa perusahaan |
| `content_creator` | 1.100.000 | 900.000 | 50.000 | 6.000.000 | Estimasi midpoint transport & skilled |
| `jualan_online` | 900.000 | 450.000 | 100.000 | 4.000.000 | IDinsight 2025 casual + self-employed average |

**Validasi rasio benchmark vs BPS:** Rasio `mu_mingguan / (BPS_NASIONAL_BEBAS / 4.345)` harus dalam range 0.5×–3.0× (ditampilkan dengan tanda ✓ atau `! cek`).

**Konversi ke parameter Log-Normal** (dihitung otomatis dari mu & sigma):
```python
sigma_ln = sqrt(log(1 + (sigma/mu)²))
mu_ln    = log(mu) - 0.5 × sigma_ln²
```
Hasil disimpan kembali ke `ID_BENCHMARK[gig]['mu_ln']` dan `ID_BENCHMARK[gig]['sigma_ln']`.

### CELL 4.2 — Kalibrasi CoV + Visualisasi

CoV dari ke-4 dataset Kaggle digabungkan dalam `cov_combined`. Untuk `cov_df4` (skillstack), dilakukan mapping skill ke gig_type terlebih dahulu:

| Skill | gig_type |
|---|---|
| Web Development, App Development, Data Science, Machine Learning | `freelancer_it` |
| Graphic Design, Video Editing | `freelancer_desain` |
| Content Writing, Digital Marketing, SEO | `content_creator` |

**`VOLATILITY_MAP`** = `clip(cov_mean, 0.15, 0.65)` per gig_type. Nilai default jika CoV tidak tersedia:
- `ojek_online: 0.28`, `kurir: 0.25`, `jualan_online: 0.35`
- `freelancer_it: 0.40`, `freelancer_desain: 0.38`, `content_creator: 0.55`

**Visualisasi:** 2 panel — grouped bar CoV per sumber Kaggle + bar CoV mean final.  
Disimpan ke: `outputs/charts/00_cov_calibration.png`

### CELL 4.3 — Parameter Kalibrasi Lainnya

**`EXPERIENCE_MULTIPLIER`:**
```python
{'junior': 0.65, 'mid': 1.00, 'senior': 1.45}
```

**`AR1_COEF = 0.45`** — koefisien autokorelasi AR(1) di log-space. Dipilih setelah iterasi untuk menghasilkan lag-1 AC ≈ 0.35–0.40 (range target Bias Test 5: 0.20–0.60).

**`SEASONAL_MULT`** — multiplier per gig_type per periode musiman:

| Periode | ojek_online | kurir | jualan_online | freelancer_it | freelancer_desain | content_creator |
|---|---|---|---|---|---|---|
| normal | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| ramadan | 1.15 | 1.20 | 1.35 | 0.90 | 1.05 | 1.25 |
| lebaran | 0.60 | 0.65 | 0.70 | 0.70 | 0.75 | 0.80 |
| harbolnas | 1.05 | 1.35 | 1.50 | 1.00 | 1.10 | 1.20 |
| yearend | 1.10 | 1.15 | 1.20 | 0.85 | 0.90 | 1.15 |
| low_season | 0.90 | 0.92 | 0.88 | 0.95 | 0.93 | 0.88 |

**`SEASONAL_INT_MAP`:** `low_season=1, normal=2, ramadan=3, harbolnas=4, lebaran=5, yearend=6`

**`PAYDAY_MULT`** (efek gajian di minggu ke-4 bulan):
```python
{'ojek_online': 1.18, 'kurir': 1.15, 'jualan_online': 1.25,
 'freelancer_it': 1.10, 'freelancer_desain': 1.12, 'content_creator': 1.08}
```

**Fungsi `get_seasonal_label(week)`:**

| Minggu | Label |
|---|---|
| 1–6 | `low_season` |
| 7–9 | `normal` |
| 10–13 | `ramadan` |
| 14–15 | `lebaran` |
| 16–44 | `normal` |
| 45–46 | `harbolnas` |
| 47–48 | `normal` |
| 49–52 | `yearend` |

---

## Bagian 5 — EDA Dataset Kaggle

### CELL 5.1 — Bar Chart: Kaggle Raw vs Benchmark Indonesia

2 panel: income Kaggle sebelum override (terlalu tinggi) vs benchmark Indonesia final (IDinsight + Sakernas + BPS). Memvisualisasikan mengapa income Kaggle tidak bisa dipakai langsung untuk konteks Indonesia.  
Disimpan ke: `outputs/charts/01_kaggle_vs_benchmark.png`

### CELL 5.2 — Boxplot Delivery Dataset

2 panel:
1. Boxplot `monthly_income_idr` per gig_type (ojek_online vs kurir) — setelah adaptasi Indonesia
2. Histogram `weekly_income_idr` dengan KDE per gig_type — memperlihatkan pola Log-Normal

Disimpan ke: `outputs/charts/02_boxplot_delivery.png`

### CELL 5.3 — EDA Skillstack (FIX: ada fallback panel)

3 panel (hanya dieksekusi jika `income_col` dan `exp_col` terdeteksi):
1. KDE distribusi income per experience level (skip jika sample < 10)
2. Bar chart skill premium per experience tier dengan label rasio
3. **FIX:** Bar horizontal CoV per skill — jika `cov_df4` kosong, fallback ke histogram `weekly_income_idr` dengan garis median

Disimpan ke: `outputs/charts/02b_skillstack_eda.png`

### CELL 5.4 — Visualisasi BPS per Provinsi (FIX: ada fallback manual)

**Path utama:** Ambil dataset BPS yang sudah punya kolom `_val_idr` (hasil `parse_bps()`), filter baris ringkasan, ambil top 20 provinsi, bar chart horizontal dengan DKI Jakarta dihighlight merah.

**Fallback manual** jika semua BPS gagal di-parse: menggunakan daftar 15 provinsi referensi dengan nilai hardcoded dari publikasi BPS.

Disimpan ke: `outputs/charts/02c_bps_benchmark_provinsi.png`

---

## Bagian 6 — Generate Data Sintetis Time-Series

Target: **300 user × 52 minggu = 15.600 baris.**

### CELL 6.1 — Konstanta Distribusi

```python
N_USERS = 300
N_WEEKS = 52
```

**`GIG_DISTRIBUTION`** (proporsi user per gig_type):
```python
{'ojek_online': 0.30, 'kurir': 0.20, 'jualan_online': 0.20,
 'freelancer_it': 0.10, 'freelancer_desain': 0.10, 'content_creator': 0.10}
```

**`EXPERIENCE_DIST`:**
```python
{'junior': 0.35, 'mid': 0.45, 'senior': 0.20}
```

**`REGION_MULTIPLIER`** (efek wilayah terhadap mu):

| Region | Multiplier |
|---|---|
| jabodetabek | 1.10× |
| bandung | 0.95× |
| jawa_barat_lainnya | 0.88× |
| jawa_tengah | 0.85× |
| jawa_timur | 0.90× |
| sumatera | 0.85× |
| kalimantan | 0.88× |
| sulawesi | 0.83× |
| bali_nusa | 0.90× |
| lainnya | 0.82× |

**`REGION_DIST`** (proporsi user per region): jabodetabek 40%, bandung 12%, jawa_barat_lainnya 8%, jawa_tengah 10%, jawa_timur 10%, sumatera 8%, kalimantan 4%, sulawesi 3%, bali_nusa 3%, lainnya 2%.

**`GIG_PLATFORM_MAP`** (platform per gig_type):
- `ojek_online`: Gojek, Grab, Maxim
- `kurir`: Shopee Express, J&T, SiCepat, Anteraja
- `freelancer_it`: Upwork, Fiverr, Projects.co.id, Toptal
- `freelancer_desain`: Fiverr, Instagram, Canva, Freelancer.com
- `content_creator`: TikTok, Instagram, YouTube, Tokopedia Affiliate
- `jualan_online`: Shopee, Tokopedia, TikTok Shop, Lazada

### CELL 6.2 — Generate User Profiles

Menggunakan `np.random.default_rng(42)` untuk reproducibility. Per user dibuat:

```python
mu_user            = bench['mu'] × exp_mult × region_mult × personal_mu_factor
personal_mu_factor ~ LogNormal(0, 0.10)   # heterogeneitas antar user
sigma_ln           = VOLATILITY_MAP[gig]
mu_ln              = log(mu_user) - 0.5 × sigma_ln²
```

Output: `df_users` (DataFrame 300 baris) dengan kolom `user_id (SYN_0001–SYN_0300)`, `gig_type`, `experience_tier`, `region`, `platform`, `mu_user`, `mu_ln`, `sigma_ln`.

### CELL 6.3 — Generate Time-Series AR(1) di Log-Space (FIX)

**Persamaan AR(1) proper di log-space (stationary):**
```
sigma_innov = sigma_ln × sqrt(max(0, 1 - AR1_COEF²))
log_inc[0]  ~ N(mu_ln, sigma_ln)
log_inc[w]  = mu_ln + AR1_COEF × (log_inc[w-1] - mu_ln) + N(0, sigma_innov)
base_income = exp(log_inc)
income      = base_income × seasonal_mult × payday_mult
income      = clip(income, bench['min'], bench['max'] × 1.20)
income      = round(income / 1.000) × 1.000
```

> **Mengapa di log-space?** AR(1) pada log-income menjaga distribusi Log-Normal tetap stationary (mean-reverting). Jika AR(1) diterapkan pada nilai linear, income bisa drift ke negatif. Dengan log-space, lag-1 autocorrelation mendekati AR1_COEF (0.20–0.60 untuk Bias Test 5 PASS).

Setelah generate, dilakukan **quick AR(1) sanity check** pada 30 user sampling untuk memverifikasi lag-1 AC sebelum lanjut.

Output disimpan ke: `data/synthetic/synthetic_income_raw.csv`

---

## Bagian 7 — Feature Engineering

### CELL 7.1 — Fitur yang Dibangun

Dataset `df_syn` diurutkan per `user_id, week_number` kemudian ditambahkan fitur berikut:

| Fitur | Formula / Kode | Fungsi untuk Model |
|---|---|---|
| `rolling_mean_4w` | `rolling(4, min_periods=1).mean()` per user | Baseline income 4 minggu — input kunci LSTM |
| `rolling_std_4w` | `rolling(4, min_periods=2).std().fillna(0)` | Volatilitas jangka pendek |
| `rolling_cov_8w` | `rolling(8, min_p=3).std() / rolling(8, min_p=3).mean()` | Volatilitas jangka menengah |
| `income_volatility` | `std/mean` seluruh 52 minggu per user | Karakteristik volatilitas user (konstan) |
| `seasonal_income_pattern` | map dari `SEASONAL_INT_MAP` | Versi numerik seasonal label |
| `gig_{gig_type}` | one-hot encoding | Identitas gig type untuk model |
| `exp_{tier}` | one-hot encoding | Identitas experience tier untuk model |
| `lag_1w` | `shift(1).fillna(0)` per user | Income 1 minggu lalu — input kunci LSTM |
| `lag_2w` | `shift(2).fillna(0)` per user | Income 2 minggu lalu |
| `lag_4w` | `shift(4).fillna(0)` per user | Income 4 minggu lalu — pola bulanan |
| `income_vs_rolling` | `(income - rolling_mean_4w) / rolling_mean_4w` | Deviasi dari baseline (0 jika rolling_mean=0) |

---

## Bagian 8 — Merge Data Survei

Bagian ini hanya dieksekusi jika `SURVEY_AVAILABLE = True`.

### CELL 8.1 — Mapping Survei ke Nilai Numerik

**Masalah utama yang di-fix:** Google Form output menggunakan **en-dash (U+2013 `–`)** untuk range, bukan hyphen biasa (`-`). Mapping didefinisikan dengan kedua versi.

**`INCOME_MIDPOINT_MAP`** — 8 bucket income mingguan (dari `< Rp250.000` hingga `> Rp5.000.000`), masing-masing dipetakan ke nilai midpoint.

**`INCOME_COMPACT_MAP`** — format ringkas (`Rp250–500rb`, dst.) untuk kolom W1–W4.

**`SURVEY_GIG_MAP`** — mapping teks jawaban form ke gig_type internal:

| Jawaban Form | gig_type |
|---|---|
| `Ojek online / driver aplikasi` | `ojek_online` |
| `Kurir / pengantar barang atau makanan` | `kurir` |
| `Jualan online / reseller / toko online` | `jualan_online` |
| `Freelance desain / editing / ilustrasi` | `freelancer_desain` |
| `Freelance IT / website / programming / data` | `freelancer_it` |
| `Content creator / admin media sosial` | `content_creator` |
| `Pekerja harian / event / part-time` | `jualan_online` |
| `Tutor / guru les / pengajar lepas` | `freelancer_desain` |

**`SURVEY_EXP_MAP`** — mapping durasi pengalaman ke tier:

| Jawaban Form | experience_tier |
|---|---|
| Kurang dari 3 bulan, 3–6 bulan, 7–12 bulan | `junior` |
| 1–2 tahun, 2–3 tahun | `mid` |
| Lebih dari 3 tahun | `senior` |

**`SURVEY_REGION_MAP`** — tambahan region yang di-fix: Jatinangor/Sumedang → `jawa_barat_lainnya`, Lampung → `sumatera`, Jawa Tengah/Yogyakarta → `jawa_tengah`.

### CELL 8.2 — Fuzzy Column Matching + Merge (FIX)

**Fungsi `find_col_by_keywords(df, keywords, exclude)`** — mencari kolom berdasarkan keyword (case-insensitive, normalized whitespace), bukan exact string match. Ini mengatasi masalah header Google Form yang panjang dan berisi newline ganda.

**Kolom yang di-match dengan keyword:**

| Variabel Internal | Keywords |
|---|---|
| `col_consent` | `['bersedia']` |
| `col_region` | `['domisili']` |
| `col_gig` | `['pekerjaan', 'lakukan']` |
| `col_exp` | `['lama', 'menjalankan']` |
| `col_inc_norm` | `['penghasilan', 'satu', 'minggu']` |
| `col_inc_low` | `['sedang', 'sepi']` |
| `col_inc_high` | `['sedang', 'ramai']` |
| `col_w1`–`col_w4` | `['minggu lalu']`, `['dua minggu']`, `['tiga minggu']`, `['empat minggu']` |

**Strategi 4-minggu real data:** Jika responden mengisi W1–W4, data real dipakai untuk minggu 1–4 series. Minggu 5–52 diproyeksikan dengan `income_norm × seasonal_mult × payday_mult`.

**Fallback income:** Jika kolom income utama tidak match, coba rata-rata W1–W4, lalu midpoint antara `inc_low` dan `inc_high`.

**Filter consent:** Responden dengan jawaban `'tidak'` (exact, lowercase) di-skip.

Output: list `df_survey_rows` — setiap responden valid menghasilkan 52 baris (prefix `SRV_XXXX`).

### CELL 8.3 — Gabungkan Sintetis + Survei

```python
df_final = pd.concat([df, df_survey_fe], ignore_index=True)
```

Data survei diset `rolling/lag = 0` karena tidak ada history. `seasonal_income_pattern` di-map dari `seasonal_label`.

---

## Bagian 9 — EDA Data Final + Jawaban BQ4 & BQ5

### CELL 9.1 — Bar Chart Mean Income per Gig Type

Mean income per `gig_type` dengan label nilai di atas bar.  
Judul: *"Mean Income Mingguan per Gig Type (Kalibrasi Indonesia)"*  
Disimpan ke: `outputs/charts/03_mean_income_by_gig.png`

### CELL 9.2 — Bar Chart Income per Gig × Experience (BQ5)

Grouped bar chart `gig_type × experience_tier` dengan `mean().unstack()`.  
Judul: *"Mean Income per Gig Type x Experience Tier (BQ5) → Senior berpenghasilan lebih tinggi"*  
Disimpan ke: `outputs/charts/04_income_by_gig_experience.png`

### CELL 9.3 — Time-Series 52 Minggu per Gig Type (BQ4)

Line chart dengan shading untuk setiap periode musiman:
- Hijau (10–13): Ramadan
- Lime (14–14.5): Lebaran
- Orange (45–46): Harbolnas
- Ungu (49–52): Yearend
- Biru (1–6): Low Season

Judul: *"Pola Income Mingguan Setahun per Gig Type (BQ4) — Pola musiman ini yang perlu dipelajari model LSTM"*  
Disimpan ke: `outputs/charts/05_timeseries_by_gig.png`

### CELL 9.4 — Heatmap Gig × Minggu dalam Bulan (BQ4)

`pivot_table(index='gig_type', columns='week_of_month')` dengan annotasi label `fmt_idr`.  
Judul: *"Efek gajian: income naik di minggu ke-4"*  
Disimpan ke: `outputs/charts/06_heatmap_gig_week_of_month.png`

### CELL 9.5 — Boxplot + Bar Chart Volatilitas per Gig (BQ5)

2 panel: boxplot distribusi CoV per user per gig_type + bar chart mean CoV. Garis merah putus-putus di `CoV = 0.30` sebagai threshold referensi.  
Disimpan ke: `outputs/charts/07_volatility_by_gig.png`

### CELL 9.6 — Correlation Heatmap Fitur (BQ5)

Kolom yang dimasukkan: `income_amount`, `rolling_mean_4w`, `rolling_std_4w`, `rolling_cov_8w`, `income_volatility`, `income_growth_1w`, `lag_1w`, `lag_4w`, `week_of_month`, `seasonal_income_pattern`, `is_payday_week`.  
Judul: *"Fitur mana yang paling berkorelasi dengan income_amount?"*  
Disimpan ke: `outputs/charts/08_correlation_heatmap.png`

---

## Bagian 10 — Bias Testing & Validasi

Target minimum: **5/6 test PASS PENUH.**

### Bias Test 1 — Mean vs Benchmark (threshold ±15%)

Untuk setiap gig_type, cek apakah `mean(income_sintetis)` dalam ±15% dari `benchmark['mu']`.

```python
pct_diff  = (actual_mu - bench_mu) / bench_mu * 100
passed    = abs(pct_diff) <= 15.0
```

Visualisasi: grouped bar Benchmark vs Aktual per gig_type.  
Disimpan ke: `outputs/charts/09_bias_test_mean.png`

### Bias Test 2 — KS Test vs Log-Normal Teoritis (p-value > 0.01)

```python
ks_stat, p_val = stats.kstest(gig_data, 'lognorm', args=(sigma_ln, 0, np.exp(mu_ln)))
passed = p_val > 0.01
```

Catatan: p-value rendah masih wajar karena seasonal multiplier menggeser distribusi — bukan berarti data salah (diberi label `WARN` bukan `FAIL`).

### Bias Test 3 — Seasonal Direction

Untuk setiap kombinasi `seasonal_label × gig_type`, cek apakah **arah** (naik/turun) income seasonal vs normal sesuai dengan `SEASONAL_MULT`. Tidak mengecek besaran, hanya arah.

```python
direction_ok = (actual_ratio > 1) == (expected_mult > 1)
```

### Bias Test 4 — Experience Multiplier (tolerance ±25%)

Rasio `mean(senior) / mean(junior)` per gig_type vs target `1.45 / 0.65 = 2.23×`.

```python
pct_diff = abs(actual_ratio - target_ratio) / target_ratio * 100
passed   = pct_diff <= 25.0
```

### Bias Test 5 — Autocorrelation AR(1) (target 0.20–0.60)

Sampling 30 user, hitung lag-1 AC dari series income:
```python
ac = np.corrcoef(series[:-1], series[1:])[0, 1]
passed = 0.20 <= mean_ac <= 0.60
```

### Bias Test 6 — BPS Range Validation

Mean income bulanan (`× 4.345`) per gig_type harus dalam range `Rp 500.000 – Rp 8.000.000`:
```python
BPS_RANGE_MIN = 500_000
BPS_RANGE_MAX = 8_000_000
in_range = BPS_RANGE_MIN <= monthly_mean <= BPS_RANGE_MAX
```

### Ringkasan Bias Test

Semua hasil dirangkum dalam `df_bias_summary` dengan styling warna (hijau=PASS, kuning=PARTIAL/WARN, merah=FAIL). Interpretasi otomatis: ≥5 PASS = "Sangat baik", ≥3 PASS = "Cukup baik", < 3 = "Perlu perbaikan".

---

## Bagian 11 — Normalisasi per User + Kolom Target

### CELL 11.1 — MinMaxScaler per User + target_next_week

```python
# MinMaxScaler per user (bukan global)
scaler = MinMaxScaler()
df_final.loc[mask, 'income_normalized'] = scaler.fit_transform(values).flatten()
scalers[uid] = scaler

# Kolom target — nilai yang diprediksi model
df_final['target_next_week'] = df_final.groupby('user_id')['income_amount'].shift(-1)
```

Scaler disimpan ke `data/processed/income_scalers.pkl` untuk inverse transform saat inference.

> **Catatan anti-leakage:** Scaler di-fit hanya pada `income_amount` per user, bukan pada kolom target. Baris terakhir tiap user memiliki `target_next_week = NaN` — harus di-drop sebelum training.

---

## Bagian 12 — Export + Chronological Split

### CELL 12.1 — Export + Split

**Chronological split** (bukan random) wajib untuk time-series:

| Set | Minggu | Proporsi |
|---|---|---|
| Train | 1–36 | ~69% |
| Validation | 37–44 | ~15% |
| Test | 45–52 | ~15% |

```python
TRAIN_END = 36
VAL_END   = 44
```

**File yang diexport:**

| File | Deskripsi |
|---|---|
| `data/processed/income_clean.csv` | Dataset final lengkap |
| `data/processed/income_train.csv` | Train set (minggu 1–36) |
| `data/processed/income_val.csv` | Validation set (minggu 37–44) |
| `data/processed/income_test.csv` | Test set (minggu 45–52) |
| `data/processed/income_scalers.pkl` | MinMaxScaler per user |
| `data/synthetic/synthetic_params.json` | Semua parameter sintesis untuk reproducibility |

**`synthetic_params.json`** berisi: `n_users`, `n_weeks`, `random_seed`, `gig_distribution`, `experience_distribution`, `volatility_map`, `experience_multiplier`, `ar1_coefficient`, `distribution_type`, semua sumber Kaggle & BPS, `split_method`, range minggu per split, dan `survey_rows_merged`.

### CELL 12.2 — Laporan Proporsi Sintetis vs Survei

Menggunakan helper functions `make_md_table()` dan `safe_pct()` untuk membuat laporan Markdown yang berisi tabel ringkasan dataset, proporsi data, dan benchmark per gig_type.  
Disimpan ke: `outputs/synthetic_proportion_report.md`

---

## Bagian 13 — Data Dictionary

### CELL 13.1 — Data Dictionary Lengkap (23 Kolom)

Diekspor dalam 2 format: CSV dan Markdown.

#### Identitas Pengguna (5 kolom)

| Kolom | Tipe | Contoh/Range | Catatan |
|---|---|---|---|
| `user_id` | string | `SYN_0001`, `SRV_0001` | Prefix SYN_ = sintetis, SRV_ = survei |
| `gig_type` | string | ojek_online, kurir, freelancer_it, ... | 6 kategori, dikalibrasi dari benchmark Indonesia |
| `region` | string | jabodetabek, bandung, jawa_barat_lainnya, ... | jabodetabek = multiplier 1.10× |
| `experience_tier` | string | junior, mid, senior | junior=0.65×, mid=1.0×, senior=1.45× |
| `platform` | string | Gojek, Grab, Shopee, Fiverr, Upwork, ... | Disesuaikan per gig_type |

#### Informasi Waktu (5 kolom)

| Kolom | Tipe | Contoh/Range | Catatan |
|---|---|---|---|
| `week_number` | int | 1–52 | train=1-36, val=37-44, test=45-52 |
| `week_of_month` | int | 1–4 | Nilai 4 = minggu akhir bulan (payday) |
| `seasonal_label` | string | low_season, normal, ramadan, lebaran, harbolnas, yearend | 6 label musim |
| `seasonal_income_pattern` | int | 1–6 | Encoding numerik dari seasonal_label |
| `is_payday_week` | int | 0 atau 1 | 1 jika week_of_month == 4 |

#### Pendapatan (4 kolom)

| Kolom | Tipe | Contoh/Range | Catatan |
|---|---|---|---|
| `income_amount` | float | ≥ 0 | Income bersih mingguan IDR, dibulatkan ke ribuan |
| `income_normalized` | float | 0.0–1.0 | MinMaxScaler per user; scaler di income_scalers.pkl |
| `income_growth_1w` | float | -1.0 s/d 5.0 | Perubahan % vs minggu sebelumnya |
| `income_vs_rolling` | float | negatif atau positif | Deviasi dari rolling_mean_4w (relatif) |

#### Feature Engineering (7 kolom)

| Kolom | Tipe | Contoh/Range | Catatan |
|---|---|---|---|
| `rolling_mean_4w` | float | ≥ 0 | Rata-rata 4 minggu terakhir per user |
| `rolling_std_4w` | float | ≥ 0 | Std 4 minggu terakhir |
| `rolling_cov_8w` | float | ≥ 0 | CoV rolling 8 minggu |
| `income_volatility` | float | ≥ 0 | CoV global per user (konstan 52 minggu) |
| `lag_1w` | float | ≥ 0 | Income 1 minggu lalu |
| `lag_2w` | float | ≥ 0 | Income 2 minggu lalu |
| `lag_4w` | float | ≥ 0 | Income 4 minggu lalu |

#### Target Model (1 kolom)

| Kolom | Tipe | Contoh/Range | Catatan |
|---|---|---|---|
| `target_next_week` | float | ≥ 0 | `shift(-1)` dari income_amount; baris terakhir = NaN → drop sebelum training |

#### Metadata (1 kolom)

| Kolom | Tipe | Contoh/Range | Catatan |
|---|---|---|---|
| `data_source` | string | `synthetic` atau `survey` | Untuk validasi proporsi data |

#### Ringkasan untuk AI Engineer (dari data_dictionary.md)

- Kolom target utama: **`target_next_week`**
- Input penting LSTM: `income_amount`, `lag_1w`, `lag_2w`, `lag_4w`, `rolling_mean_4w`, `rolling_std_4w`, `seasonal_income_pattern`
- Gunakan `income_normalized` agar skala stabil antar user
- **Drop baris dengan `target_next_week = NaN` sebelum training**

---

## Bagian 14 — Push ke GitHub

### CELL 14A — Git Config + Branch Management

```python
BRANCH_NAME = "feature/income-predictor"
```

Konfigurasi git identity:
- `user.email = 'nayyafn2006@gmail.com'`
- `user.name = 'Clarisya Adeline'`

Logika branch sama dengan CELL 0.1: cek local branch → remote branch → buat baru.

### CELL 14B — Push ke Branch

Strategi push (5 langkah):
1. `git fetch origin`
2. `git rm -r --cached data/processed/ data/synthetic/ outputs/` — hapus tracking file lama
3. `git add -A data/processed/ data/synthetic/ outputs/`
4. `git diff --cached --quiet || git commit -m "{commit_message}"` — commit hanya jika ada perubahan
5. `git push -u origin {BRANCH_NAME}` — push ke branch (bukan `--force`, bukan ke main)

Commit message: `"feat: DS2 income pipeline v9-FINAL - AR1 survey, KS+AD, leakage fix, lag8/12, week_sin/cos, 500 users, BPS 8 provinsi"`

> Perbedaan dengan Notebook 2: menggunakan `git push -u origin {BRANCH_NAME}` (push ke branch spesifik), bukan `--force-with-lease` ke main.

### CELL 14.3 — Verifikasi File Output

Memeriksa keberadaan **22 file output** yang wajib ada sebelum dianggap selesai:

| Kategori | File |
|---|---|
| Dataset utama | `income_clean.csv`, `income_train/val/test.csv`, `income_scalers.pkl` |
| Data Dictionary | `data_dictionary.csv`, `data_dictionary.md` |
| Data sintetis | `synthetic_income_raw.csv`, `synthetic_params.json` |
| Laporan | `synthetic_proportion_report.md` |
| Charts (11 file) | `00_cov_calibration.png` s/d `09_bias_test_mean.png` |

Jika semua ada → `"Semua file tersedia dan siap di-push ke GitHub."`. Jika ada yang missing → ditampilkan dengan tanda `[x MISSING]`.

---

## Catatan Perbedaan vs Dokumentasi Draft

Beberapa nilai aktual di notebook berbeda dari dokumen draft yang diunggah:

| Parameter | Nilai di Draft | Nilai Aktual di Notebook |
|---|---|---|
| `INDIA_ADAPT` | 0.55 | **0.23** |
| `USD_TO_IDR` | 17.545 | **17.252** |
| `SANITY_MAX_MONTHLY_IDR` | 10.000.000 | **15.000.000** (di CELL 4.1) |
| Branch git | push ke `main` | **`feature/income-predictor`** |
| Commit message | versi 8 | **versi 9-FINAL** |
| Total file verify | 22 file | **22 file** (sama) |

---

## File Output Lengkap

```
data/
├── raw/
│   ├── Freelancer_Work_Patterns_Income_Prediction_Dataset.csv
│   ├── freelancer_earnings_bd.csv
│   ├── delivery_boy_salary.csv
│   ├── freelancer_earnings_vs_skillstack_dataset.csv
│   ├── Rata-Rata Pendapatan Bersih Sebulan ... 2025.csv  (×2)
│   ├── Rata-Rata_Pendapatan_Bersih...2024.csv
│   ├── Rata-rata Pendapatan Bersih...2023.csv
│   └── form_responses.csv  (opsional)
├── processed/
│   ├── income_clean.csv          ← FILE UTAMA
│   ├── income_train.csv
│   ├── income_val.csv
│   ├── income_test.csv
│   ├── income_scalers.pkl
│   ├── data_dictionary.csv
│   └── data_dictionary.md
└── synthetic/
    ├── synthetic_income_raw.csv
    └── synthetic_params.json

outputs/
├── synthetic_proportion_report.md
└── charts/
    ├── 00_cov_calibration.png
    ├── 01_kaggle_vs_benchmark.png
    ├── 02_boxplot_delivery.png
    ├── 02b_skillstack_eda.png
    ├── 02c_bps_benchmark_provinsi.png
    ├── 03_mean_income_by_gig.png
    ├── 04_income_by_gig_experience.png
    ├── 05_timeseries_by_gig.png
    ├── 06_heatmap_gig_week_of_month.png
    ├── 07_volatility_by_gig.png
    ├── 08_correlation_heatmap.png
    └── 09_bias_test_mean.png
```
