from pathlib import Path
import pandas as pd

from core.panel import generate_panel
from core.validate import validate_dataset

BASE = Path(__file__).resolve().parent.parent

def load_data():
    path = BASE / "assets" / "geostatlab_base.csv"

    if not path.exists():
        raise FileNotFoundError(f"Missing dataset: {path}")

    df_base = pd.read_csv(path)

    # Generate panel
    df = generate_panel(df_base)

    # Validate
    valid, messages = validate_dataset(df)

    if not valid:
        raise ValueError(f"Dataset validation failed: {messages}")

    return df
