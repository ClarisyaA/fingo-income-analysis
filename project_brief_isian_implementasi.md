# Isian Project Brief - CC26-PSU217

Dokumen ini dibuat untuk dicopy ke template `Project Brief - CC26-PSU217.docx`. Urutan bagian mengikuti template project brief, dengan isi yang sudah disesuaikan terhadap implementasi terbaru di repository `fingo-income-analysis`, Streamlit dashboard, dan artefak AI Engineer.

Catatan koreksi utama dari project plan lama:

- Income Predictor menggunakan input 4 minggu terakhir, bukan 12 minggu terakhir.
- Implementasi model saat ini bukan LSTM sebagai model produksi utama, melainkan tabular machine learning / ensemble model yang dipaketkan ke `.pkl` dan `.joblib`.
- Data survei 384 responden digunakan sebagai baseline distribusi, sedangkan dataset training utama untuk Income Predictor adalah synthetic longitudinal dataset 3.000 user x 52 minggu.
- A/B testing yang tersedia adalah proof-of-concept berbasis data sintetis, bukan live experiment pada pengguna nyata.

---

# Dokumen Project Brief

Coding Camp 2026 powered by DBS Foundation

## ID Tim Capstone Project

CC26-PSU217

## Judul Proyek

Fingo

## Tema yang Dipilih

The Financial Technology (Fintech) Revolution for the Younger Generation

## Nama Advisor Capstone

[DC26-206] - Syahrul Septian Zein

Catatan sesi mentoring:

- 15/05/2026
- 29/05/2026

## List Anggota

| ID | Nama | Role | Status |
|---|---|---|---|
| CFCC308D6X1847 | Tasria Sare | Full-Stack Web Developer | Aktif |
| CFCC308D6X2842 | Aisyah Septiani | Full-Stack Web Developer | Aktif |
| CDCC011D6X1678 | Clarisya Adeline | Data Scientist | Aktif |
| CDCC001D6X2492 | Nayyara Farhana Nisa | Data Scientist | Aktif |
| CACC011D6Y2585 | Muhammad Fachri | AI Engineer | Aktif |
| CACC011D6X0895 | Martha Meslina Florencia | AI Engineer | Aktif |

---

# Judul Proyek

## Fingo: AI-Powered Financial Assistant for Gig Workers and Gen Z

Fingo adalah platform keuangan berbasis kecerdasan buatan yang dirancang untuk membantu gig worker, freelancer, pekerja informal, dan Generasi Z dalam mengelola pendapatan yang tidak stabil. Platform ini mengintegrasikan Income Predictor berbasis machine learning, Impulsive Transaction Detector, Fingo AI Assistant berbasis Gemini API, dan Budget Planner adaptif dalam satu ekosistem digital.

Pada implementasi final, Income Predictor memprediksi pendapatan minggu berikutnya menggunakan input pendapatan 4 minggu terakhir, profil pekerjaan, pola kerja, fitur kalender, dan fitur statistik rolling. Impulsive Transaction Detector membantu mengidentifikasi transaksi dengan risiko impulsif berdasarkan nominal, kategori, waktu transaksi, metode pembayaran, dan sinyal perilaku transaksi. Dashboard Streamlit digunakan untuk menampilkan insight data, performa model, simulasi A/B testing, serta demo interaktif fitur utama.

## Filosofi Nama: Fingo

Nama Fingo berasal dari gabungan kata `Finance` dan `Go`. Nama ini mencerminkan aplikasi keuangan yang cepat, sederhana, mobile-friendly, dan relevan untuk pengguna muda dengan gaya hidup dinamis.

### Kecepatan dan Ketepatan (Agility)

Kata `Go` melambangkan pergerakan cepat. Bagi freelancer dan gig worker, waktu adalah aset penting. Fingo hadir untuk membantu pengguna mengelola keuangan tanpa proses administrasi yang rumit, mulai dari melihat prediksi pendapatan, menyusun budget, hingga mengambil keputusan finansial secara lebih cepat.

### Kendali di Tangan Pengguna (Forward Motion)

Fingo tidak hanya berfungsi sebagai pencatat keuangan masa lalu, tetapi juga sebagai alat bantu untuk merencanakan masa depan. Melalui fitur Income Predictor, pengguna dapat memperkirakan pendapatan minggu depan berdasarkan pendapatan 4 minggu terakhir sehingga dapat menyusun rencana keuangan dengan lebih realistis.

### Finger-on-the-Pulse: Keuangan di Ujung Jari

Secara fonetik, Fingo terdengar dekat dengan kata `finger`. Hal ini menggambarkan bahwa kondisi keuangan pengguna dapat dipantau hanya melalui beberapa ketukan. Dengan bantuan AI, Fingo dapat memberikan sinyal ketika pengguna berpotensi melakukan transaksi impulsif, sehingga pengguna dapat mengevaluasi keputusan finansial sebelum transaksi dilakukan.

### Simpel, Modern, dan Adaptif

Akhiran `-o` memberikan kesan modern, ramah, dan global. Hal ini mencerminkan antarmuka Fingo yang minimalis dan mudah digunakan oleh Generasi Z, namun tetap didukung teknologi machine learning, API deployment, dashboard analitik, dan AI Assistant.

---

# Ringkasan Eksekutif

## Latar Belakang

Pertumbuhan gig economy di Indonesia meningkat seiring perkembangan ekonomi digital, platform kerja fleksibel, dan preferensi Generasi Z terhadap pola kerja yang lebih mandiri. Berdasarkan data Badan Pusat Statistik (BPS), Indonesia memiliki sekitar 84,2 juta pekerja informal, dan sekitar 41,6 juta di antaranya dapat dikategorikan sebagai gig worker seperti driver ojek online, kurir, freelancer, pekerja kreatif digital, dan pekerja berbasis platform.

Kelompok pekerja ini menghadapi tantangan keuangan yang berbeda dari pekerja bergaji tetap. Pendapatan mereka cenderung fluktuatif dari minggu ke minggu karena dipengaruhi jumlah order, musim, event kalender, hari kerja, jam kerja, domisili, dan jenis pekerjaan. Ketidakpastian ini membuat perencanaan budget menjadi sulit. Pengguna sering kali membuat anggaran berdasarkan rata-rata historis sederhana, padahal kondisi pendapatan minggu depan dapat berubah cukup besar.

Di sisi lain, pertumbuhan e-commerce dan pembayaran digital memperbesar peluang transaksi impulsif. Indonesia e-Commerce Behavior Report 2023 menunjukkan nilai transaksi e-commerce meningkat dari Rp106 triliun pada 2018 menjadi Rp476,3 triliun pada 2022. Laporan yang sama juga menunjukkan 45,9% pengguna memanfaatkan PayLater. Kemudahan checkout, promo, BNPL, dan pembayaran digital dapat meningkatkan risiko belanja impulsif, terutama bagi pengguna muda dengan pendapatan tidak menentu.

Aplikasi keuangan yang ada umumnya berfokus pada pencatatan transaksi, budget statis, atau laporan pengeluaran setelah transaksi terjadi. Masih terdapat gap untuk solusi yang secara bersamaan membantu pengguna memprediksi pendapatan, menyesuaikan budget secara adaptif, dan memberi sinyal risiko transaksi sebelum pengguna mengambil keputusan finansial.

Fingo dibangun untuk menjawab gap tersebut. Platform ini menggabungkan Income Predictor, Budget Planner adaptif, Impulsive Transaction Detector, dan AI Assistant agar pekerja gig dan Gen Z dapat mengambil keputusan finansial dengan konteks yang lebih baik.

## Problem Statement

Bagaimana membangun platform keuangan berbasis AI yang mampu membantu gig worker dan Generasi Z dengan pendapatan tidak stabil melalui prediksi pendapatan mingguan, budget planning adaptif, dan deteksi transaksi impulsif untuk mengurangi risiko over-budget?

## Research Questions

1. Bagaimana pola pendapatan pekerja gig berdasarkan data survei, benchmark BPS, dan synthetic longitudinal dataset?
2. Seberapa akurat model machine learning dalam memprediksi pendapatan minggu berikutnya menggunakan input 4 minggu terakhir?
3. Fitur apa yang paling berpengaruh dalam prediksi pendapatan mingguan pekerja gig?
4. Apakah budget adaptif berbasis Income Predictor dapat menurunkan budget planning error dibanding budget manual berbasis rolling mean 4 minggu?
5. Pada kategori, waktu, dan kondisi transaksi apa risiko impulsif paling sering muncul?
6. Fitur apa yang paling berpengaruh dalam klasifikasi transaksi AMAN, PERTIMBANGAN, dan IMPULSIF?
7. Bagaimana dashboard dan API dapat mengintegrasikan model Income Predictor, Impulsive Detector, dan Fingo Assistant ke dalam alur produk yang dapat diuji?

## Alasan Pemilihan Proyek

Tim memilih proyek ini karena Fingo menyelesaikan dua masalah utama bagi gig worker dan Gen Z, yaitu pendapatan yang tidak stabil dan risiko belanja impulsif. Dengan jumlah pekerja informal dan gig worker yang besar di Indonesia, solusi ini memiliki potensi dampak sosial dan produk yang relevan.

Fingo juga sesuai dengan tema fintech karena menggabungkan data science, machine learning, dashboard analitik, API deployment, dan desain produk keuangan digital. Proyek ini tidak hanya membuat model prediksi, tetapi juga menunjukkan bagaimana prediksi tersebut dapat digunakan dalam konteks budget planning dan decision support.

## Status Penyelesaian Proyek

| Komponen | Status | Keterangan |
|---|---|---|
| Survei Primer | Selesai | 384 responden, Google Form, digunakan sebagai distribusi acuan |
| Synthetic Income Time-Series | Selesai | 3.000 user x 52 minggu = 156.000 rows, dataset training utama Income Predictor |
| Income Predictor - Data Pipeline | Selesai | 10 notebook dari data preparation sampai A/B testing |
| Income Predictor - Model | Selesai | Final summary: Ens(DL=0.15+GradientBoosting), MAE Rp 39.862, R2 0,9102 |
| Income Predictor - Baseline Evaluation | Selesai | XGBRegressor test MAE Rp 42.931, RMSE Rp 90.468, MAPE 11,96%, R2 0,9091 |
| Income Direction Classifier | Selesai | Final accuracy 79,09%, macro F1 0,6105 |
| Income Predictor API | Live | `https://mes1205-fingo.hf.space/predict/income` |
| Fingo Assistant API | Live | `https://mes1205-fingo.hf.space/chat` |
| Impulsive Detector - Data Pipeline | Selesai | Data gathering, assessing, cleaning, merging, feature engineering, labeling, EDA, split |
| Impulsive Detector - Model | Selesai | `fingo_label_classifier.joblib`, klasifikasi AMAN / PERTIMBANGAN / IMPULSIF |
| Impulsive Detector API | Live | `https://mfachri820-ai-fingo.hf.space` |
| A/B Testing Income Predictor Budgeting | Selesai | Proof-of-concept berbasis data sintetis; budget error turun 70,14% |
| Streamlit Dashboard | Live | `https://fingo-app.streamlit.app/` |
| Frontend React + Vite | Live | `https://fingo-frontend-ten.vercel.app/` |
| Backend Express + PostgreSQL | TBD | Pending verification, evidence final belum diterima |
| Video Presentasi YouTube | TBD | Diisi setelah upload |
| Slide Presentasi | TBD | Diisi setelah selesai |

---

# Tech Stack Checklist

Silakan tandai tech stack yang sudah terpenuhi, baik dari mandatory tech stack (Main Quest) maupun optional tech stack (Side Quest).

## Main Quest - Front End and Back End

| Kriteria | Status | Bukti / Catatan |
|---|---|---|
| Menggunakan networking calls untuk berinteraksi dengan API pada proyek | Terpenuhi | Frontend/Streamlit mengakses Income API, Chat API, dan Impulsive Detector API |
| Menggunakan module bundler seperti webpack, Vite, dan sejenisnya | Terpenuhi | Frontend React + Vite, deployed di Vercel |
| Membangun RESTful API untuk mendukung aplikasi Front-End | Sebagian / perlu verifikasi | Income API dan Chat API tersedia di HuggingFace; backend Express masih TBD |
| RESTful API dapat menyimpan data dengan atau tanpa database | Perlu verifikasi | Backend Express + PostgreSQL masih pending evidence |
| Membuat RESTful API dengan URL mengikuti standar konvensi RESTful | Sebagian / perlu verifikasi | Endpoint AI tersedia; backend utama masih pending verification |
| Mengintegrasikan kemampuan AI/ML sebagai fitur utama aplikasi | Terpenuhi | Income Predictor, Impulsive Detector, Fingo Assistant |
| Memastikan fitur utama berjalan tanpa crash | Terpenuhi pada dashboard dan API AI | Streamlit dashboard dan HuggingFace API sudah live |
| Tidak menggunakan Web Generator untuk membuat aplikasi FE/BE | Perlu konfirmasi tim FE/BE | Diisi oleh anggota FE/BE |

## Main Quest - Artificial Intelligence

| Kriteria | Status | Bukti / Catatan |
|---|---|---|
| Membangun model Deep Learning menggunakan TensorFlow Functional API atau Model Subclassing | Berubah dari plan awal | Implementasi final memakai tabular ML / ensemble, bukan LSTM production |
| Mengimplementasikan komponen custom lanjutan seperti custom layer/loss/callback | Berubah dari plan awal | Tidak menjadi implementasi final karena model produksi memakai scikit-learn / XGBoost / ensemble |
| Menyimpan dan mengekspor model TensorFlow siap produksi | Berubah dari plan awal | Artefak final berupa `.pkl` dan `.joblib`, bukan `.keras` |
| Membuat kode inference sederhana | Terpenuhi | Inference tersedia di API HuggingFace dan fallback model lokal Streamlit |
| Tidak menggunakan model dari TensorFlow Hub | Terpenuhi | Model diskriminatif dilatih sendiri dari dataset project |
| Tidak menggunakan model langsung dari layanan API untuk model diskriminatif | Terpenuhi | Gemini API hanya untuk Fingo Assistant, bukan model diskriminatif Income/Impulsive |
| Tidak menggunakan AutoML untuk model diskriminatif | Terpenuhi | Model dilatih melalui notebook/pipeline sendiri |

Catatan transparansi AI:

Project plan awal mengarah pada TensorFlow/LSTM, tetapi implementasi final berubah menjadi model tabular/ensemble karena dataset final berbentuk supervised tabular dengan 58 fitur. Pendekatan ini lebih stabil, interpretabel, dan mudah dideploy dalam batas waktu capstone. LSTM sebaiknya hanya ditulis sebagai future work jika data longitudinal pengguna nyata sudah cukup panjang.

## Main Quest - Data Science

| Kriteria | Status | Bukti / Catatan |
|---|---|---|
| Mengumpulkan dan menganalisis permasalahan, lalu menentukan solusi utama | Terpenuhi | Problem discovery: income fluktuatif + transaksi impulsif |
| Mendefinisikan pertanyaan bisnis yang dapat diukur | Terpenuhi | Research questions dan metrik model/A-B testing tersedia |
| Gathering data | Terpenuhi | Survey primer, BPS, dataset transaksi, synthetic data |
| Assessing data | Terpenuhi | Notebook impulsive data assessing dan pipeline income validation |
| Cleaning data | Terpenuhi | Survey cleaning, transaction cleaning, standardisasi kategori |
| Melakukan EDA | Terpenuhi | EDA survey, impulsive EDA, visualisasi dashboard |
| Membuat visualisasi dan explanatory analysis | Terpenuhi | Charts di `outputs/charts/` dan Streamlit dashboard |
| Mengembangkan dashboard interaktif Streamlit | Terpenuhi | `streamlit/app.py`, deployed di Streamlit Cloud |
| Memastikan data siap diproses model dan membuat data dictionary | Terpenuhi | `data_dictionary.md`, `model_contract.json`, split train/val/test |
| Tidak menggunakan dataset siap pakai tanpa cleaning manual | Terpenuhi | Dataset diproses melalui pipeline cleaning dan feature engineering |
| Tidak melakukan analisis tanpa markdown/teks | Terpenuhi | README, notebook.md, reports, technical report |
| Tidak menarik kesimpulan tanpa visualisasi | Terpenuhi | Kesimpulan didukung chart dan metrik |
| Tidak menghasilkan dataset akhir yang belum siap model | Terpenuhi | `income_train.csv`, `income_val.csv`, `income_test.csv`, model contract |
| Tidak menyertakan target ke fitur training | Terpenuhi | Anti-leakage check dan forbidden leakage columns tersedia |

## Side Quest - Front End and Back End

| Kriteria | Status | Bukti / Catatan |
|---|---|---|
| Membuat mockup aplikasi | Perlu dilengkapi | Isi dengan link Figma/mockup jika ada |
| Layout responsive | Terpenuhi pada frontend prototype | React + Vite deployed di Vercel |
| RESTful API menyimpan data ke database | TBD | Backend Express + PostgreSQL pending verification |
| RESTful API menggunakan Express | TBD | Pending evidence |
| Menggunakan Bootstrap / Tailwind / Axios | Perlu konfirmasi FE | Diisi oleh tim FE |
| Deployment aplikasi web ke server | Terpenuhi | Vercel untuk frontend, Streamlit Cloud untuk dashboard |

## Side Quest - Artificial Intelligence

| Kriteria | Status | Bukti / Catatan |
|---|---|---|
| Mengembangkan REST API mandiri menggunakan FastAPI/Flask | Sebagian | API AI live di HuggingFace Space |
| Custom training loop tf.GradientTape | Tidak diterapkan final | Model final bukan TensorFlow/LSTM |
| Menggunakan API Generative AI sebagai fitur tambahan | Terpenuhi | Fingo Assistant menggunakan Gemini API |
| Integrasi TensorBoard | Tidak diterapkan final | Tidak relevan untuk model final scikit-learn / ensemble |
| Performa model baik | Sebagian terpenuhi | Regression R2 0,9102 dan MAE Rp 39.862; MAE normalized final 0,0214, mendekati target 0,02; direction accuracy 79,09% |

## Side Quest - Data Science

| Kriteria | Status | Bukti / Catatan |
|---|---|---|
| Feature engineering informatif | Terpenuhi | 58 fitur: lag, rolling, trend, calendar, profile, gig type |
| Deployment dashboard ke Streamlit Cloud | Terpenuhi | `https://fingo-app.streamlit.app/` |
| Implementasi A/B Testing menggunakan Python | Terpenuhi | Notebook 10, proof-of-concept synthetic |
| Laporan teknis komprehensif dalam PDF | Sebagian | Markdown reports tersedia; PDF perlu disusun/diekspor |

---

# Tautan Dataset

## Tabel Dataset

| No | Dataset Name | Sumber | Digunakan untuk Fitur | Status & Catatan Penting |
|---:|---|---|---|---|
| 1 | Survei Primer Fingo | Google Form internal | Income Predictor, profil gig worker, validasi lokal | 384 responden, digunakan sebagai distribusi acuan, bukan training utama langsung |
| 2 | Synthetic 52-Week User Income | Dibuat tim Data Science dengan Python | Income Predictor, Budget Planner simulation | 3.000 user x 52 minggu = 156.000 rows, dataset training utama |
| 3 | BPS Pendapatan Pekerja Informal/Bebas 2023-2025 | BPS | Benchmark Income Predictor | Digunakan untuk validasi kewajaran distribusi income, bukan training langsung |
| 4 | Personal Finance Dataset | Kaggle / sumber publik | Impulsive Detector, transaksi personal finance | Dibersihkan, distandardisasi, dan digabung dengan dataset transaksi lain |
| 5 | Daily Household Transactions | Sumber publik | Impulsive Detector, pola transaksi rumah tangga | Digunakan untuk fitur kategori, waktu, nominal, dan perilaku transaksi |
| 6 | Indonesian E-Commerce Sales 2024-2025 | Kaggle / sumber publik | Impulsive Detector, pola e-commerce dan timestamp | Digunakan untuk analisis pola transaksi, kategori, metode pembayaran, dan waktu |

## Link Dataset Income Analysis

`https://github.com/ClarisyaA/fingo-income-analysis`

## Artefak Dataset Utama di Repository

| Path | Keterangan |
|---|---|
| `data/processed/survey_clean.csv` | Data survei yang sudah dibersihkan |
| `data/processed/survey_temporal_mapped.csv` | Data survei dengan mapping periode mingguan relatif |
| `data/processed/survey_weekly_income_long.csv` | Data survei format long untuk EDA mingguan |
| `data/synthetic/synthetic_52week_user_income.csv` | Synthetic longitudinal dataset utama |
| `data/processed/income_features.csv` | Supervised feature dataset |
| `outputs/model_contract/income_train.csv` | Training set |
| `outputs/model_contract/income_val.csv` | Validation set |
| `outputs/model_contract/income_test.csv` | Test set |
| `streamlit/data/impulsive/transactions_labeled.csv` | Dataset transaksi berlabel untuk dashboard impulsive |

---

# Tautan Deployment Produk

| Komponen | URL | Platform | Status |
|---|---|---|---|
| Streamlit Dashboard (DS) | `https://fingo-app.streamlit.app/` | Streamlit Cloud | Live |
| Frontend Prototype | `https://fingo-frontend-ten.vercel.app/` | Vercel | Live |
| Income Predictor API | `https://mes1205-fingo.hf.space/predict/income` | HuggingFace Space | Live |
| Fingo Assistant API | `https://mes1205-fingo.hf.space/chat` | HuggingFace Space | Live, membutuhkan `GEMINI_API_KEY` |
| Impulsive Detector API | `https://mfachri820-ai-fingo.hf.space/call/predict_json` | HuggingFace Gradio | Live |
| Impulsive Detector Bulk CSV | `https://mfachri820-ai-fingo.hf.space/call/predict_file` | HuggingFace Gradio | Live |
| Backend Express API | TBD | Render / platform backend | Pending verification |

---

# Tautan Repository Github

| Role | Anggota | Repository / Link | Status |
|---|---|---|---|
| Data Scientist 1 & 2 - Income Analysis | Clarisya Adeline | `https://github.com/ClarisyaA/fingo-income-analysis` | Ada |
| AI Engineer 1 - Impulsive Detector | Muhammad Fachri | `https://github.com/mfachri820/impulsive-money-detector` | Ada |
| AI Engineer 2 - Income API + Fingo Assistant | Martha Meslina Florencia | `https://github.com/Mes1205/Fingo` | Ada |
| Frontend - React + Vite | Aisyah Septiani | `https://fingo-frontend-ten.vercel.app/` dan repository GitHub perlu diisi | Deployed |
| Backend - Express + PostgreSQL | Tasria Sare | TBD | Pending verification |

---

# Screenshot Produk

Bagian ini perlu dilengkapi dengan screenshot final dari produk.

## UI Login Page

Isi dengan screenshot login page dari frontend.

## UI Dashboard

Isi dengan screenshot dashboard utama frontend atau Streamlit.

## Streamlit - Insight & Kesimpulan

Isi dengan screenshot modul insight dan kesimpulan.

## Streamlit - Income Predictor

Isi dengan screenshot form input Income Predictor dan hasil prediksi.

## Streamlit - A/B Testing

Isi dengan screenshot ringkasan A/B Testing Income Predictor Budgeting.

## Streamlit - Impulsive Detector

Isi dengan screenshot form transaksi dan hasil klasifikasi AMAN / PERTIMBANGAN / IMPULSIF.

---

# Tautan Video Presentasi (Pitching) 10 Menit

Masukkan tautan video presentasi proyek capstone yang sudah diunggah ke YouTube.

Status saat ini:

TBD - perlu diisi setelah video final diunggah.

Ketentuan:

- Video diunggah ke YouTube dengan status `Unlisted`.
- Video diunggah oleh salah satu anggota tim sebagai perwakilan.
- Durasi maksimal presentasi adalah 10 menit.

---

# Tautan Penggunaan Produk

Masukkan tautan penggunaan produk dalam bentuk video atau dokumen.

Status saat ini:

TBD - belum tersedia.

Opsi yang dapat dilampirkan:

- Video demo penggunaan aplikasi.
- Dokumen panduan penggunaan.
- README utama repository yang menjelaskan cara menjalankan semua komponen.

Panduan sementara tersedia di README masing-masing repository.

---

# Tautan Slide Presentasi

Masukkan tautan slide presentasi final di bagian ini. Pastikan akses diberikan sebagai `Anyone with the link can view`.

Status saat ini:

TBD - perlu diisi setelah slide final selesai.

Slide presentasi perlu memuat:

1. Latar belakang.
2. Alasan atau rumusan masalah.
3. Perbandingan dengan aplikasi/produk serupa.
4. Hasil pengembangan produk.
5. Mockup dan desain yang telah dibuat.
6. Alasan pemilihan implementasi.
7. Dokumentasi atau README.
8. Rencana implementasi lokal jika ada.
9. Analisis SWOT.

---

# Analisis SWOT

## Strengths

1. Tim multidisiplin dengan 2 Full-Stack Web Developer, 2 AI Engineer, dan 2 Data Scientist.
2. Fingo menyelesaikan dua masalah yang saling berkaitan: income gig worker yang fluktuatif dan risiko transaksi impulsif.
3. Income Predictor mencapai performa kuat pada test set: MAE Rp 42.931, RMSE Rp 90.468, MAPE 11,96%, dan R2 0,9091.
4. Final deployment summary menunjukkan MAE Rp 39.862, RMSE Rp 89.931, dan R2 0,9102.
5. A/B Testing proof-of-concept menunjukkan penurunan budget error sebesar 70,14% pada treatment berbasis predicted income.
6. Synthetic longitudinal dataset cukup besar untuk capstone: 3.000 user x 52 minggu = 156.000 rows.
7. Data survei primer 384 responden memberikan distribusi lokal pekerja gig Indonesia.
8. Dashboard Streamlit sudah live dan mengintegrasikan insight, Income Predictor, A/B testing, Impulsive Detector, dan Fingo Assistant.
9. API AI sudah live melalui HuggingFace Space.
10. Model contract, data dictionary, dan dokumentasi pipeline tersedia untuk handoff AI Engineer.

## Weaknesses

1. Implementasi final berubah dari rencana TensorFlow/LSTM ke model tabular/ensemble, sehingga perlu dijelaskan secara transparan di brief dan presentasi.
2. Dataset training utama Income Predictor masih sintetis, sehingga validasi dengan data real pengguna masih dibutuhkan.
3. Survey primer hanya 384 responden dan mencakup 4 minggu historis.
4. Bias validation menunjukkan mean synthetic terhadap benchmark BPS masih belum sepenuhnya pass.
5. A/B testing masih proof-of-concept berbasis data sintetis, belum live experiment.
6. Backend fullstack belum terverifikasi sepenuhnya pada saat penulisan brief.
7. Endpoint gratis seperti HuggingFace, Streamlit Cloud, dan Vercel dapat mengalami cold start atau rate limit.
8. Fingo Assistant membutuhkan konfigurasi `GEMINI_API_KEY` agar aktif.

## Opportunities

1. Pasar gig worker Indonesia besar dan terus berkembang.
2. Banyak aplikasi keuangan masih berfokus pada pencatatan historis, belum pada prediksi income dan deteksi impulsif secara terpadu.
3. Penetrasi smartphone dan pembayaran digital tinggi di kalangan Gen Z.
4. Fingo dapat dikembangkan menjadi fitur premium untuk fintech, e-wallet, atau platform gig.
5. Integrasi dengan e-wallet, QRIS, atau bank statement dapat meningkatkan kualitas data real.
6. Live A/B testing dapat membuka peluang validasi dampak perilaku pengguna.
7. Model dapat dikembangkan lebih lanjut dengan data longitudinal nyata.

## Threats

1. Data time-series pendapatan gig worker yang panjang sulit diperoleh secara nyata karena isu privasi dan konsistensi pencatatan.
2. Kompetitor fintech besar memiliki akses data transaksi dan pengguna yang jauh lebih besar.
3. Perubahan kebijakan platform free tier dapat mempengaruhi availability produk.
4. Rate limit Gemini API dapat mengganggu fitur AI Assistant saat trafik meningkat.
5. Model harus divalidasi ulang jika digunakan pada populasi berbeda dari data survei.
6. Produk keuangan membutuhkan perhatian khusus terhadap privasi, keamanan data, dan kepatuhan regulasi.

---

# Catatan Mentoring

Tuliskan catatan mentoring dari Advisor di bagian ini.

Catatan yang sudah tersedia:

- Advisor: Syahrul Septian Zein.
- Sesi mentoring: 15/05/2026 dan 29/05/2026.

Detail masukan advisor dapat ditambahkan oleh tim jika tersedia.

---

# Apakah Proyek Capstone yang Telah Selesai Berbeda dengan Rencana Awal?

Ya. Proyek final mengalami beberapa perubahan signifikan dari Project Plan awal. Perubahan ini tidak mengurangi keberhasilan proyek, tetapi mengubah pendekatan teknis agar lebih sesuai dengan data final, batas waktu capstone, kemudahan deployment, dan stabilitas demo.

## Tabel Perubahan dari Rencana Lama ke Implementasi Baru

| Bagian | Rencana Lama | Implementasi Baru | Alasan & Dampak |
|---|---|---|---|
| Income Predictor - Arsitektur Model | TensorFlow Model Subclassing, LSTM, custom layer/normalization, `tf.GradientTape`, ekspor `.keras` | Tabular ML / ensemble. Baseline XGBRegressor + RandomForestClassifier; final summary `Ens(DL=0.15+GradientBoosting)` dan `Ens_cls(DL=0.50)` | Dataset final berbentuk supervised tabular dengan 58 fitur, sehingga gradient boosting/ensemble lebih stabil dan cepat dideploy. Performa final MAE Rp 39.862 dan R2 0,9102 |
| Input Income Predictor | 12 minggu terakhir | 4 minggu terakhir | Data survei asli hanya memiliki 4 minggu historis. Pipeline final menjaga urutan `income_w4 -> income_w3 -> income_w2 -> income_w1 -> next_week_income` |
| Data Training Income Predictor | Survey sebagai sumber utama | Survey sebagai baseline distribusi; synthetic 3.000 user x 52 minggu sebagai training utama | Survey 384 responden tidak cukup panjang untuk model time-series, sehingga dibuat synthetic longitudinal dataset agar split by user representatif |
| Data Sintetis - Jumlah | 200 user x 52 minggu | 3.000 user x 52 minggu = 156.000 rows | Jumlah dinaikkan agar train/val/test by user lebih kuat: 2.100 / 450 / 450 users |
| Split Dataset | Berpotensi random row | Split by `synthetic_user_id` | Menghindari user-level leakage antara train, validation, dan test |
| Impulsive Detector - Arsitektur Model | TensorFlow Functional API dengan custom attention/loss | RandomForestClassifier dalam scikit-learn Pipeline, disimpan sebagai `fingo_label_classifier.joblib` | Dataset transaksi bersifat tabular dengan fitur kategorikal; Random Forest lebih stabil dan mudah dideploy |
| Label Impulsive Detector | Binary impulsive / non-impulsive | Multi-class: AMAN, PERTIMBANGAN, IMPULSIF | Output lebih mudah dipahami pengguna dan lebih cocok untuk decision support |
| Platform Deployment AI | FastAPI di Render / backend Express | Income Predictor + Fingo Assistant di HuggingFace Space; Impulsive Detector di HuggingFace Gradio | HuggingFace lebih praktis untuk Python ML deployment pada free tier |
| A/B Testing | Behavioral real-user testing untuk impulsive warning | Proof-of-concept Income Predictor Budgeting berbasis synthetic data | Real-user testing belum memungkinkan dalam timeframe capstone. Simulasi menunjukkan budget error turun 70,14% |
| Backend Fullstack | Express.js + PostgreSQL deployed di Render | Frontend prototype live di Vercel; backend masih pending verification | Evidence backend final belum diterima saat penulisan brief |
| Streamlit Dashboard | Modul terbatas untuk overview, EDA, prediction demo, A/B testing, data dictionary, technical summary | Dashboard diperluas menjadi modul Insight & Kesimpulan, Income Predictor, A/B Testing, dan Impulsive Detector dengan sub-tab evaluasi, visualisasi, demo prediksi, dan Fingo Assistant | Scope dashboard diperluas untuk demo end-to-end dan integrasi API |

## Dampak Perubahan terhadap Keberhasilan Proyek

Perubahan arsitektur dari LSTM ke tabular ML / ensemble membuat model lebih sesuai dengan bentuk data final dan lebih stabil untuk deployment. Walaupun tidak memenuhi rencana awal TensorFlow/LSTM secara literal, pendekatan final menghasilkan performa prediksi yang kuat, dokumentasi model contract yang jelas, dan demo yang dapat diakses melalui Streamlit serta HuggingFace.

Perubahan input dari 12 minggu ke 4 minggu juga membuat produk lebih selaras dengan data survei dan lebih ringan bagi pengguna. Pengguna cukup memasukkan pendapatan 4 minggu terakhir, sehingga friction input lebih rendah dan alur demo lebih realistis.

Dengan demikian, proyek tetap berhasil sebagai proof-of-concept end-to-end untuk financial intelligence platform, dengan catatan bahwa validasi pengguna nyata dan backend production masih perlu dilanjutkan pada tahap berikutnya.

---

# Lampiran Implementasi Data Science dan AI Engineer

Bagian ini dapat dipakai jika template menyediakan ruang tambahan untuk dokumentasi teknis.

## Income Predictor - Model Contract

Artefak handoff tersedia di:

```text
outputs/model_contract/
```

Isi utama:

- `income_train.csv`: training set, 100.800 rows.
- `income_val.csv`: validation set, 21.600 rows.
- `income_test.csv`: test set, 21.600 rows.
- `income_scalers.pkl`: scaler pipeline.
- `feature_columns.json`: daftar 58 fitur.
- `model_contract.json`: metadata fitur, target, split rule, normalization note, dan leakage rules.
- `target_contract.json`: kontrak target model.
- `final_weekly_features.json`: daftar fitur final.

## Income Predictor - Fitur Utama

Jumlah fitur pada model contract: 58 fitur.

Kelompok fitur:

- Lag income: `lag_1_income`, `lag_2_income`, `lag_3_income`, `lag_4_income`.
- Rolling statistics: mean, standard deviation, min, max, range, median, coefficient of variation.
- Trend features: income growth, absolute change, percentage change, trend slope.
- Calendar features: target month, week of month, quarter, payday, weekend, Ramadan/Lebaran, Harbolnas, Christmas/year-end, New Year.
- User profile: usia, pengalaman, hari kerja, jam kerja, total jam seminggu.
- Regional benchmark: BPS weekly income reference.
- Preference features: payday, weekend, Ramadan/Lebaran, Natal/Tahun Baru, Harbolnas, promo aplikasi.
- Gig type one-hot encoding.

Target:

- Regression target: `next_week_income`.
- Classification target: `next_week_direction`.

Direction threshold:

- Up: perubahan income >= 10%.
- Down: perubahan income <= -10%.
- Stable: perubahan antara -10% dan +10%.

## Income Predictor - Hasil Evaluasi

Baseline evaluation dari notebook 09:

| Metric | Value |
|---|---:|
| Best regression model | XGBRegressor |
| Test MAE | Rp 42.931 |
| Test RMSE | Rp 90.468 |
| Test MAPE | 11,96% |
| Test R2 | 0,9091 |
| Best classification model | RandomForestClassifier |
| Test Accuracy | 74,89% |
| Test Macro F1 | 0,6221 |

Final deployment summary:

| Metric | Value |
|---|---:|
| Final regression model | Ens(DL=0.15+GradientBoosting) |
| Final regression MAE | Rp 39.862 |
| Final regression RMSE | Rp 89.931 |
| Final regression R2 | 0,9102 |
| Final classification model | Ens_cls(DL=0.50) |
| Direction accuracy | 79,09% |
| Direction macro F1 | 0,6105 |
| Tolerance accuracy 2% | 77,02% |
| Tolerance accuracy 5% | 90,18% |
| Tolerance accuracy 10% | 94,96% |

## A/B Testing Income Predictor Budgeting

Desain:

- Control: budget manual = 70% dari rolling mean 4 minggu income historis.
- Treatment: budget adaptif = 70% dari predicted income.
- Assignment: stratified random 50:50 per `gig_type`.
- Primary metric: `mean_budget_error`.

Hasil:

| Metric | Control | Treatment |
|---|---:|---:|
| N user | 1.502 | 1.498 |
| Mean budget error | Rp 47 ribu | Rp 14 ribu |
| Median budget error | Rp 36 ribu | Rp 10 ribu |
| Relative change | - | -70,14% |

Statistical test:

- Mann-Whitney U p-value: 0,000000.
- Welch t-test one-tailed p-value: 0,000000.
- Cohen's d: -1,2188, efek besar.

Interpretasi:

Budget adaptif berbasis Income Predictor berpotensi menurunkan budget planning error dibanding budget manual. Namun, hasil ini masih proof-of-concept berbasis data sintetis dan belum membuktikan perubahan perilaku pengguna nyata.

## Impulsive Detector

Artefak model:

```text
streamlit/models/fingo_label_classifier.joblib
```

Input utama:

- Nominal transaksi.
- Kategori transaksi.
- Metode pembayaran.
- Tanggal transaksi.
- Jam transaksi.
- Budget mingguan opsional.

Fitur model:

- `amount`
- `amount_log`
- `amount_z`
- `amount_score`
- `impulsive_score`
- `hour`
- `day_of_week`
- `driver_count`
- `category`
- `metode_pembayaran`
- `source`
- `time_segment`
- `category_type`
- `is_hedonic_category`
- `is_night`
- `is_weekend`
- `signal_band`

Output:

- AMAN.
- PERTIMBANGAN.
- IMPULSIF.

## Streamlit Dashboard

File implementasi:

```text
streamlit/app.py
```

Modul utama:

- Insight & Kesimpulan.
- Income Predictor.
- A/B Testing.
- Impulsive Detector.

Integrasi API:

- Income API: `https://mes1205-fingo.hf.space/predict/income`
- Chat API: `https://mes1205-fingo.hf.space/chat`

Fallback lokal:

- Streamlit dapat menggunakan model deployment lokal dari `streamlit/models/` jika API tidak tersedia.

## Referensi File Implementasi

- `README.md`: overview pipeline dan dokumentasi repo.
- `notebook.md`: alur modular notebook.
- `data_dictionary.md`: definisi kolom dan temporal mapping.
- `outputs/model_contract/model_contract.json`: kontrak fitur, target, split, dan leakage rules.
- `outputs/model_results/model_evaluation_report.md`: metrik evaluasi model.
- `outputs/charts/income/final_metrics_summary.json`: ringkasan metrik final.
- `outputs/reports/bias_validation_report.md`: hasil validasi bias.
- `outputs/reports/ab_testing_income_predictor_budgeting_report.md`: hasil simulasi A/B testing.
- `streamlit/app.py`: implementasi dashboard.
- `streamlit/models/`: artefak model deployment.
