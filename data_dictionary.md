# Data Dictionary — Fingo Income Predictor
**Tim:** CC26-PSU217 | **Versi:** v13-FINAL | **Tanggal:** Mei 2026

---

## Temporal Mapping untuk Data Survey

Kolom `income_w1`, `income_w2`, `income_w3`, dan `income_w4` berasal dari pertanyaan
pendapatan 1–4 minggu terakhir pada Google Form.

Karena responden mengisi form pada rentang tanggal tertentu (Mei 2026), periode pendapatan
historis bersifat **relatif terhadap `timestamp` masing-masing responden**.

### Definisi
| Kolom | Periode | Rentang |
|-------|---------|---------|
| `income_w1` | Pendapatan 1 minggu terakhir | H-7 sampai H-1 dari timestamp |
| `income_w2` | Pendapatan 2 minggu terakhir | H-14 sampai H-8 dari timestamp |
| `income_w3` | Pendapatan 3 minggu terakhir | H-21 sampai H-15 dari timestamp |
| `income_w4` | Pendapatan 4 minggu terakhir | H-28 sampai H-22 dari timestamp |

### Urutan Kronologis untuk Model Forecasting
```
income_w4 → income_w3 → income_w2 → income_w1
(terlama)                             (terbaru)
```

> Kolom ini **tidak** merepresentasikan minggu 1–4 dalam satu bulan kalender secara langsung.
> Melainkan 4 periode mingguan relatif sebelum responden mengisi form.

### Kolom Hasil Temporal Mapping
Untuk analisis kalender, notebook `02_Temporal_Mapping.ipynb` membuat kolom tambahan:

| Kolom | Deskripsi |
|-------|-----------|
| `income_wN_period_start` | Tanggal awal periode minggu ke-N |
| `income_wN_period_end`   | Tanggal akhir periode minggu ke-N (representative date) |
| `income_wN_month`        | Bulan kalender dari period_end |
| `income_wN_year`         | Tahun dari period_end |
| `income_wN_week_of_month`| Minggu ke berapa dalam bulan (dari period_end) |
| `income_wN_iso_week`     | ISO week number dari period_end |

### Definisi week_of_month
| Week | Tanggal |
|------|---------|
| Week 1 | 1–7 |
| Week 2 | 8–14 |
| Week 3 | 15–21 |
| Week 4 | 22–28 |
| Week 5 | 29–31 |

---

## Kolom Utama Dataset

### Survey / Profile
| Kolom | Tipe | Deskripsi | Sumber |
|-------|------|-----------|--------|
| `respondent_id` | string | ID unik responden (R0000–R0383) | Generated |
| `timestamp` | datetime | Waktu pengisian form | Form col 0 |
| `survey_date` | date | Tanggal pengisian form | Derived |
| `usia` | int | Usia responden (clip 17–65) | Form col 2 |
| `gig_type` | string | 8 kategori pekerjaan gig | Form col 4 |
| `domisili_code` | string | Kode domisili (9 region) | Form col 3 |
| `hari_kerja_per_minggu` | int | Hari kerja per minggu (clip 1–7) | Form col 8 |
| `jam_kerja_per_hari` | int | Jam kerja per hari (clip 1–16) | Form col 9 |
| `lama_kerja_bulan` | float | Pengalaman dalam bulan | Form col 7 |

### Income (Survey)
| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `income_w1` | float | Pendapatan **minggu lalu** (TERBARU) |
| `income_w2` | float | Pendapatan **2 minggu lalu** |
| `income_w3` | float | Pendapatan **3 minggu lalu** |
| `income_w4` | float | Pendapatan **4 minggu lalu** (TERLAMA) |

### Lag Features (Model)
| Kolom | Tipe | Deskripsi | Leakage Risk |
|-------|------|-----------|--------------|
| `lag_1_income` | float | Income lag 1 (dari urutan kronologis) | Low |
| `lag_2_income` | float | Income lag 2 | Low |
| `lag_3_income` | float | Income lag 3 | Low |
| `lag_4_income` | float | Income lag 4 (terlama) | Low |
| `rolling_mean_4w` | float | Rata-rata 4 lag | Low |
| `rolling_std_4w` | float | Std 4 lag | Low |
| `income_growth_1w` | float | Growth rate lag_1 vs lag_2 | Low |
| `income_volatility` | float | CV dari 4 lag | Low |

### Targets (JANGAN masuk X)
| Kolom | Tipe | Deskripsi | Leakage Risk |
|-------|------|-----------|--------------|
| `next_week_income` | float | **TARGET**: pendapatan minggu depan | **HIGH** |
| `next_week_direction` | string | **TARGET**: Up/Stable/Down | **HIGH** |

### Synthetic
| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `synthetic_user_id` | string | ID unik (SYN_000001–SYN_002999) |
| `synthetic_weekly_income` | float | Observed income (sumber lag) |
| `dataset_type` | string | synthetic_52w |

---

## 8 Kategori Gig Type
| Kode | Label Form |
|------|-----------|
| `ojek_online` | Ojek online / driver aplikasi |
| `kurir` | Kurir / pengantar barang atau makanan |
| `jualan_online` | Jualan online / reseller / toko online |
| `freelance_desain` | Freelance desain / editing / ilustrasi |
| `freelance_it` | Freelance IT / website / programming / data |
| `content_creator` | Content creator / admin media sosial |
| `tutor` | Tutor / guru les / pengajar lepas |
| `pekerja_harian` | Pekerja harian / event / part-time |

---

## Direction Classification
- **Up**: perubahan income >= 10% (bukan >)
- **Down**: perubahan income <= -10% (bukan <)
- **Stable**: perubahan antara -10% dan +10%
