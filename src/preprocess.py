import pandas as pd


def basic_preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Basit önişleme:
    - Tarih sütunlarını tespit etmeye çalışır ve parçalara ayırır
    - Sayısal eksikleri medyan ile doldurur
    - Kategorikleri one-hot ile kodlar (çok fazla unique varsa atlar)
    """
    df = df.copy()

    # Tarih sütunlarını tespit et
    for col in df.columns:
        if df[col].dtype == object:
            try:
                parsed = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
                if parsed.notna().sum() > 0:
                    df[col] = parsed
            except Exception:
                pass

    # Tarih parçaları
    for col in df.select_dtypes(include=["datetime64[ns]", 'datetime64']).columns:
        df[f"{col}_year"] = df[col].dt.year
        df[f"{col}_month"] = df[col].dt.month
        df[f"{col}_day"] = df[col].dt.day

    # Sayısal eksikler
    for col in df.select_dtypes(include=["number"]).columns:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())

    # Kategorik: küçük cardinality için one-hot
    for col in df.select_dtypes(include=["object"]).columns:
        if df[col].nunique() <= 20:
            dummies = pd.get_dummies(df[col], prefix=col, dummy_na=False)
            df = pd.concat([df.drop(columns=[col]), dummies], axis=1)

    return df
