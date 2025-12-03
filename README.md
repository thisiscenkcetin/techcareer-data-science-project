
# techcareer-data-science-project

Proje: e-Bilet Satış Analizi

Kısa: `bilet_satislar.csv` ile EDA, önişleme ve basit satış tahmini 

Paketler

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# (Streamlit eksikse) pip install streamlit
```

Çalıştırma

```powershell
# Model eğitimi
python src\train.py

# Notebooks
jupyter notebook

# Dashboard
python -m streamlit run src\app.py
```

İskelet
- `notebooks/EDA.ipynb`, `notebooks/Model.ipynb`
- `src/` (data, preprocess, train, app)
- `models/rf_model.pkl`, `reports/metrics.md`

Demo



İletişim
[![Gmail](https://img.shields.io/badge/Gmail-EA4335?style=flat&logo=gmail&logoColor=white)](mailto:dev.cenkcetin@gmail.com)
[![Telegram](https://img.shields.io/badge/Telegram-0088cc?style=flat&logo=telegram&logoColor=white)](https://t.me/thisiscenkcetin)
