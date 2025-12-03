import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
from src.data import load_data
from src.preprocess import basic_preprocess


def train_and_save(random_state: int = 42):
    df = load_data()
    df = basic_preprocess(df)

    # Hedef: Satilan_Adet
    if 'Satilan_Adet' not in df.columns:
        raise ValueError('Hedef sütun `Satilan_Adet` bulunamadı')

    # Basit özellik seçimi: sayısal olanlar
    X = df.select_dtypes(include=[np.number]).drop(columns=['Satilan_Adet'], errors='ignore')
    y = df['Satilan_Adet'].fillna(0)

    # Eğer hiç sayısal feature yoksa hata ver
    if X.shape[1] == 0:
        raise ValueError('Sayısal özellik bulunamadı; önişleme sonrası özellikler yetersiz')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)

    model = RandomForestRegressor(n_estimators=50, random_state=random_state)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    # some sklearn versions may not support `squared` arg; use sqrt(MSE)
    rmse = mean_squared_error(y_test, preds) ** 0.5

    # Kaydet
    joblib.dump(model, 'models/rf_model.pkl')

    # Rapor yaz
    with open('reports/metrics.md', 'w', encoding='utf-8') as f:
        f.write('# Model Metrikleri\n\n')
        f.write(f'- Model: RandomForestRegressor\n')
        f.write(f'- Test RMSE: {rmse:.4f}\n')

    print('Training completed. Test RMSE:', rmse)


if __name__ == '__main__':
    train_and_save()
