# Streamlit Dashboard Data README
*Fingo Weekly Income Forecasting — v10-FINAL*

## File Dashboard (outputs/dashboard/)
| File | Deskripsi |
|------|-----------|
| kpi_summary.csv | KPI utama proyek |
| gig_type_income_summary.csv | Income per jenis pekerjaan |
| domisili_income_summary.csv | Income per domisili + BPS gap |
| weekly_trend_summary.csv | Tren W4→W1 |
| direction_distribution_summary.csv | Distribusi Up/Stable/Down |
| factor_fluctuation_summary.csv | Faktor fluktuasi |
| work_pattern_summary.csv | Pola kerja per gig_type |
| model_performance_summary.csv | Perbandingan semua model |
| weekly_performance_dashboard.csv | Performa per target_week |
| ab_testing_summary.csv | Hasil A/B test |
| calendar_income_summary.csv | Income per calendar context |
| seasonal_event_summary.csv | Income per seasonal preference |
| payday_vs_normal_summary.csv | Payday vs Normal comparison |
| data_dictionary.csv | Dokumentasi semua kolom |

## Contoh Penggunaan
```python
import streamlit as st
import pandas as pd
kpi = pd.read_csv("outputs/dashboard/kpi_summary.csv").iloc[0]
st.metric("Total Responden", kpi["total_respondents"])
```
