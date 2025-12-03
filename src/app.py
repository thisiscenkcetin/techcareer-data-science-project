# Basit Streamlit uygulaması (opsiyonel)
import sys
from pathlib import Path

# Ensure project root is on sys.path so `import src...` works when Streamlit
# executes this script from the `src/` folder.
project_root = str(Path(__file__).resolve().parents[1])
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd
from src.data import load_data

st.title("e-Bilet Satış Analizi")

uploaded = st.file_uploader("CSV yükle (CSV dosyası seçin)", type="csv")
if uploaded is not None:
    df = pd.read_csv(uploaded)
else:
    try:
        df = load_data()
    except Exception as e:
        st.write("Veri yüklenemedi:", e)
        df = None

if df is not None:
    st.write(df.head())
    if st.checkbox("Özet istatistikler"):
        # provide a Turkish-labeled describe table and replace None/NaN with '-'
        try:
            desc = df.describe(include='all')
            desc = desc.rename(index={
                'count': 'Adet',
                'unique': 'Benzersiz',
                'top': 'En Sık',
                'freq': 'Sıklık',
                'mean': 'Ortalama',
                'std': 'Std',
                'min': 'Min',
                '50%': 'Medyan',
                'max': 'Maks'
            })
            # replace NaN/None or literal 'None' strings with a nicer placeholder
            desc = desc.fillna('-')
            desc = desc.replace(to_replace=[None, 'None'], value='-')
            st.write(desc)
        except Exception as e:
            st.write('Özet istatistikler hesaplanamadı:', e)

    if st.checkbox("Aylık Satış Trendi"):
        try:
            df['Tarih'] = pd.to_datetime(df['Tarih'], errors='coerce')
            monthly = df.set_index('Tarih').resample('M').agg({'Satilan_Adet':'sum'})
            # Turkish month names
            months_tr = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık']
            months = [f"{str(idx.year)} {months_tr[idx.month-1]}" for idx in monthly.index]
            chart_df = monthly.copy()
            chart_df.index = months
            st.line_chart(chart_df['Satilan_Adet'])
        except Exception as e:
            st.write('Aylık trend hesaplanamadı:', e)
