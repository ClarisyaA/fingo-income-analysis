# Fingo Streamlit Dashboard

Dashboard Streamlit ini digunakan untuk menampilkan insight data, evaluasi model, simulasi A/B testing, dan demo interaktif fitur AI pada proyek Fingo.

## Isi Dashboard

Dashboard memiliki 3 modul utama:

1. **Insight & Kesimpulan**
   - Ringkasan insight keseluruhan project.
   - Jawaban research question.
   - Highlight hasil Income Predictor, Impulsive Detector, dan A/B testing.

2. **Income Predictor**
   - EDA dataset pendapatan gig worker.
   - Ringkasan synthetic income time-series.
   - Performa model final Income Predictor.
   - Visualisasi evaluasi model.
   - Simulasi A/B testing Budget Planner adaptif.
   - Demo prediksi pendapatan via API atau fallback model lokal.

3. **Impulsive Detector**
   - EDA transaksi dan distribusi label.
   - Analisis impulsive rate berdasarkan kategori, waktu, weekend, dan nominal.
   - Performa model Impulsive Detector.
   - Feature importance.
   - Demo deteksi risiko transaksi impulsif.

## Struktur Folder Penting

```txt
streamlit/
|-- app.py                 # Entry point dashboard
|-- requirements.txt       # Dependency Streamlit
|-- models/                # Model deployment dan classifier
|   |-- fingo_deploy.pkl
|   |-- fingo_deploy_v1.pkl
|   `-- fingo_label_classifier.joblib
`-- data/                  # Data khusus dashboard
    |-- income/
    `-- impulsive/
```

Dashboard juga membaca beberapa artefak dari folder parent project:

```txt
data/processed/
data/synthetic/
outputs/charts/
outputs/charts/income/final_metrics_summary.json
outputs/model_results/
outputs/reports/
```

## Prasyarat

Pastikan sudah terinstall:

- Python 3.10 atau lebih baru
- pip
- Git

## 1. Clone Repository

```bash
git clone https://github.com/ClarisyaA/fingo-income-analysis.git
```

## 2. Masuk ke Folder Project

```bash
cd fingo-income-analysis
```

## 3. Install Dependencies

```bash
pip install -r streamlit/requirements.txt
```

Dependency penting:

- `streamlit` untuk dashboard
- `pandas`, `numpy` untuk data processing
- `matplotlib`, `seaborn`, `plotly` untuk visualisasi
- `scikit-learn==1.6.1` agar kompatibel dengan model `.pkl`

## 4. Jalankan Dashboard

```bash
streamlit run streamlit/app.py
```

Secara default dashboard akan berjalan di:

```txt
http://localhost:8501
```

## 5. Cek Dashboard

Setelah dashboard terbuka, cek modul berikut dari sidebar:

1. `Insight & Kesimpulan`
2. `Income Predictor`
3. `Impulsive Detector`

Jika semua data dan model tersedia, dashboard akan menampilkan metrik, chart, tabel, dan demo interaktif.

## Catatan Deployment / Cloud

Untuk Streamlit Cloud, pastikan:

- File `streamlit/requirements.txt` terbaca sebagai dependency.
- File model di `streamlit/models/` ikut terupload.
- File data dan output yang dibutuhkan ikut tersedia di repository.
- `outputs/charts/income/final_metrics_summary.json` tersedia agar metrik final tetap tampil meskipun pickle model gagal dibaca.

## Troubleshooting

### Dashboard menampilkan `N/A`

Kemungkinan penyebab:

- File model atau output belum tersedia di repository/deployment.
- Pickle model gagal dibaca karena versi dependency tidak cocok.
- File JSON metrik final tidak ditemukan.

Solusi:

- Pastikan `outputs/charts/income/final_metrics_summary.json` tersedia.
- Pastikan `streamlit/models/fingo_deploy.pkl` tersedia.
- Install dependency sesuai `streamlit/requirements.txt`.

### Model gagal load

Pastikan versi scikit-learn sesuai:

```txt
scikit-learn==1.6.1
```

### API Income Predictor timeout

Dashboard memanggil endpoint:

```txt
https://mes1205-fingo.hf.space/predict/income
```

Jika HuggingFace Space sedang sleep atau timeout, coba ulang beberapa saat kemudian. Dashboard juga memiliki fallback model lokal jika file model tersedia.
