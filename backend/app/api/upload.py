from pathlib import Path
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.ingestion.reader import read_file
from app.ingestion.schema_detector import detect_schema
from app.ingestion.column_mapper import map_columns
from app.ingestion.normalizer import normalize_dataset


router = APIRouter(prefix="/api", tags=["Upload"])


BASE_DIR = Path(__file__).resolve().parents[3]

UPLOAD_DIR = BASE_DIR / "data" / "raw" / "uploads"
NORMALIZED_DIR = BASE_DIR / "data" / "processed" / "normalized"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
NORMALIZED_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...)
):

    allowed_extensions = {
        ".csv",
        ".xlsx",
        ".xls",
        ".json"
    }

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only CSV, Excel and JSON files are supported."
        )

    dataset_id = str(uuid.uuid4())

    filename = f"{dataset_id}_{file.filename}"

    upload_path = UPLOAD_DIR / filename

    content = await file.read()

    with open(upload_path, "wb") as f:
        f.write(content)

    try:

        df = read_file(str(upload_path))

        capabilities = detect_schema(df)

        mapping = map_columns(df)

        normalized = normalize_dataset(
            df,
            mapping
        )

        normalized_path = (
            NORMALIZED_DIR
            / f"{dataset_id}.parquet"
        )

        normalized.to_parquet(
            normalized_path,
            index=False
        )

        return {
            "success": True,
            "dataset_id": dataset_id,
            "filename": file.filename,
            "rows": len(df),
            "columns": len(df.columns),
            "capabilities": capabilities,
            "column_mapping": mapping,
            "normalized_file": str(normalized_path)
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )