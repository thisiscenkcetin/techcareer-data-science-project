import pandas as pd
from typing import Optional


def load_data(path: Optional[str] = None) -> pd.DataFrame:
    """CSV dosyasını yükler. Varsayılan olarak repo kökündeki `bilet_satislar.csv` kullanılır.

    Args:
        path: Dosya yolu (opsiyonel)

    Returns:
        pd.DataFrame
    """
    if path is None:
        path = "bilet_satislar.csv"
    df = pd.read_csv(path, encoding="utf-8", low_memory=False)

    # If there's a `Tarih` column and dates are in 2023 or earlier,
    # shift them forward by 2 years so the dataset years become 2025 (for demo/sunuma uygunluk).
    if 'Tarih' in df.columns:
        try:
            parsed = pd.to_datetime(df['Tarih'], errors='coerce')
            # only shift if the data appears to be <= 2023
            if parsed.dt.year.max() <= 2023:
                df['Tarih'] = (parsed + pd.DateOffset(years=2)).dt.strftime('%Y-%m-%d')
            else:
                df['Tarih'] = parsed.dt.strftime('%Y-%m-%d')
        except Exception:
            # leave original if parsing fails
            pass

    return df
