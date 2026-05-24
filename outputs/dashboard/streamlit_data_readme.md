# Streamlit Dashboard Data README
*Fingo Weekly Income Forecasting — v11-FINAL*

## ⚠️ Peringatan Dataset
- **Data real 4w** = dasar validitas utama (535 responden nyata)
- **Data sintetis 52w** = simulasi longitudinal untuk dashboard & AI Engineer
- Jangan klaim performa synthetic sebagai performa dunia nyata

## File Dashboard (outputs/dashboard/)
| File | Deskripsi | Sumber |
|------|-----------|--------|
| gig_type_distribution.csv | Distribusi 8 jenis pekerjaan | Real |
| real_4w_income_summary.csv | Income summary per gig_type | Real |
| synthetic_52w_income_summary.csv | Income summary synthetic | Synthetic |
| synthetic_monthly_trend_summary.csv | Tren income per bulan | Synthetic |
| synthetic_seasonal_event_summary.csv | Income per seasonal event | Synthetic |
| synthetic_gig_type_monthly_summary.csv | Income per gig per bulan | Synthetic |
| synthetic_weekly_forecasting_summary.csv | Forecasting summary | Synthetic |
| dataset_comparison_summary.csv | Perbandingan real vs synthetic | Mixed |
| model_performance_summary.csv | Semua model | Mixed |
| weekly_performance_dashboard.csv | Performa per target_week | Real |
| ab_testing_summary.csv | A/B test summary | Real |
| seasonal_event_income_summary.csv | Seasonal preferences | Real |
| data_dictionary.csv | Dokumentasi kolom | - |

## Contoh Penggunaan Streamlit
```python
import streamlit as st
import pandas as pd

real = pd.read_csv("outputs/dashboard/real_4w_income_summary.csv")
synth = pd.read_csv("outputs/dashboard/synthetic_52w_income_summary.csv")

st.header("Fingo — Income Forecasting Dashboard")
st.warning("Data sintetis adalah simulasi, bukan data penghasilan nyata.")
st.dataframe(real)
```
