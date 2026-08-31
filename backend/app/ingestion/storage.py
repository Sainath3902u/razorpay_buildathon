from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]

NORMALIZED_DIR = (
    ROOT / "data" / "processed" / "normalized"
)

NORMALIZED_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def save_normalized_data(
    df: pd.DataFrame,
    dataset_id: str = "demo"
) -> str:

    output_path = (
        NORMALIZED_DIR
        / f"{dataset_id}.parquet"
    )

    df.to_parquet(
        output_path,
        index=False
    )

    return str(output_path)