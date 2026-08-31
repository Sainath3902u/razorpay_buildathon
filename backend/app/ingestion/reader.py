from pathlib import Path
import pandas as pd


def read_file(file_path: str) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()

    if suffix == ".csv":
        df = pd.read_csv(path)

    elif suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(path)

    elif suffix == ".json":
        df = pd.read_json(path)

    else:
        raise ValueError(
            f"Unsupported file format: {suffix}. "
            "Supported: CSV, XLSX, JSON"
        )

    if df.empty:
        raise ValueError("Uploaded dataset is empty.")

    return df