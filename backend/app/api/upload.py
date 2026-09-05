# from pathlib import Path
# import uuid

# from fastapi import APIRouter, UploadFile, File, HTTPException

# from app.ingestion.reader import read_file
# from app.ingestion.schema_detector import detect_schema
# from app.ingestion.column_mapper import map_columns
# from app.ingestion.normalizer import normalize_dataset


# router = APIRouter(prefix="/api", tags=["Upload"])


# BASE_DIR = Path(__file__).resolve().parents[3]

# UPLOAD_DIR = BASE_DIR / "data" / "raw" / "uploads"
# NORMALIZED_DIR = BASE_DIR / "data" / "processed" / "normalized"

# UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
# NORMALIZED_DIR.mkdir(parents=True, exist_ok=True)


# @router.post("/upload")
# async def upload_dataset(
#     file: UploadFile = File(...)
# ):

#     allowed_extensions = {
#         ".csv",
#         ".xlsx",
#         ".xls",
#         ".json"
#     }

#     extension = Path(file.filename).suffix.lower()

#     if extension not in allowed_extensions:
#         raise HTTPException(
#             status_code=400,
#             detail="Only CSV, Excel and JSON files are supported."
#         )

#     dataset_id = str(uuid.uuid4())

#     filename = f"{dataset_id}_{file.filename}"

#     upload_path = UPLOAD_DIR / filename

#     content = await file.read()

#     with open(upload_path, "wb") as f:
#         f.write(content)

#     try:

#         df = read_file(str(upload_path))

#         capabilities = detect_schema(df)

#         mapping = map_columns(df)

#         normalized = normalize_dataset(
#             df,
#             mapping
#         )

#         normalized_path = (
#             NORMALIZED_DIR
#             / f"{dataset_id}.parquet"
#         )

#         normalized.to_parquet(
#             normalized_path,
#             index=False
#         )

#         return {
#             "success": True,
#             "dataset_id": dataset_id,
#             "filename": file.filename,
#             "rows": len(df),
#             "columns": len(df.columns),
#             "capabilities": capabilities,
#             "column_mapping": mapping,
#             "normalized_file": str(normalized_path)
#         }

#     except Exception as e:

#         raise HTTPException(
#             status_code=400,
#             detail=str(e)
#         )




from pathlib import Path
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.ingestion.reader import read_file
from app.ingestion.schema_detector import detect_schema
from app.ingestion.column_mapper import map_columns
from app.ingestion.normalizer import normalize_dataset
from app.engine.detector_engine import detect_all_opportunities


router = APIRouter(prefix="/api", tags=["Upload"])


BASE_DIR = Path(__file__).resolve().parents[3]

UPLOAD_DIR = BASE_DIR / "data" / "raw" / "uploads"
NORMALIZED_DIR = BASE_DIR / "data" / "processed" / "normalized"


UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
NORMALIZED_DIR.mkdir(parents=True, exist_ok=True)


# In-memory store for the current backend process.
# This is enough for local development/demo use.
DATASET_RESULTS = {}


def serialize_opportunity(opportunity):
    """
    Convert the dataclass Opportunity into JSON-safe dict.
    """
    return {
        "opportunity_id": opportunity.opportunity_id,
        "category": opportunity.category,
        "opportunity_type": opportunity.opportunity_type,
        "customer_id": opportunity.customer_id,
        "amount_at_risk": float(opportunity.amount_at_risk),
        "probability": float(opportunity.probability),
        "expected_value": float(opportunity.expected_value),
        "reason": opportunity.reason,
        "recommended_action": opportunity.recommended_action,
        "priority": opportunity.priority,
        "recovery_eligible": opportunity.recovery_eligible,
        "recovery_reason": opportunity.recovery_reason,
        "source_detector": opportunity.source_detector,
    }


def build_summary(opportunities):
    """
    Build dashboard KPI summary from detected opportunities.
    """

    total_at_risk = sum(
        float(item.amount_at_risk)
        for item in opportunities
    )

    total_expected = sum(
        float(item.expected_value)
        for item in opportunities
    )

    recover_count = sum(
        1 for item in opportunities
        if item.category == "RECOVER"
    )

    prevent_count = sum(
        1 for item in opportunities
        if item.category == "PREVENT"
    )

    grow_count = sum(
        1 for item in opportunities
        if item.category == "GROW"
    )

    high_count = sum(
        1 for item in opportunities
        if item.priority == "HIGH"
    )

    medium_count = sum(
        1 for item in opportunities
        if item.priority == "MEDIUM"
    )

    low_count = sum(
        1 for item in opportunities
        if item.priority == "LOW"
    )

    return {
        "total_opportunities": len(opportunities),
        "total_amount_at_risk": round(total_at_risk, 2),
        "total_expected_value": round(total_expected, 2),

        "category_counts": {
            "RECOVER": recover_count,
            "PREVENT": prevent_count,
            "GROW": grow_count,
        },

        "priority_counts": {
            "HIGH": high_count,
            "MEDIUM": medium_count,
            "LOW": low_count,
        },
    }


@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...)
):

    allowed_extensions = {
        ".csv",
        ".xlsx",
        ".xls",
        ".json",
    }

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only CSV, XLS, XLSX and JSON files are supported."
        )

    dataset_id = str(uuid.uuid4())

    safe_name = Path(file.filename).name

    upload_path = (
        UPLOAD_DIR
        / f"{dataset_id}_{safe_name}"
    )

    try:

        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        with open(upload_path, "wb") as output:
            output.write(content)

        # -----------------------------------------------------
        # READ
        # -----------------------------------------------------

        df = read_file(
            str(upload_path)
        )

        # -----------------------------------------------------
        # SCHEMA
        # -----------------------------------------------------

        capabilities = detect_schema(df)

        # -----------------------------------------------------
        # COLUMN MAPPING
        # -----------------------------------------------------

        mapping = map_columns(df)

        # -----------------------------------------------------
        # NORMALIZE
        # -----------------------------------------------------

        normalized = normalize_dataset(
            df,
            mapping
        )

        # -----------------------------------------------------
        # DETECT OPPORTUNITIES
        # -----------------------------------------------------

        opportunities = detect_all_opportunities(
            normalized
        )

        # -----------------------------------------------------
        # SERIALIZE
        # -----------------------------------------------------

        opportunity_data = [
            serialize_opportunity(item)
            for item in opportunities
        ]

        summary = build_summary(
            opportunities
        )

        # -----------------------------------------------------
        # STORE RESULTS
        # -----------------------------------------------------

        DATASET_RESULTS[dataset_id] = {
            "dataset_id": dataset_id,
            "filename": file.filename,
            "rows": len(df),
            "columns": len(df.columns),
            "capabilities": capabilities,
            "column_mapping": mapping,
            "summary": summary,
            "opportunities": opportunity_data,
        }

        # -----------------------------------------------------
        # RESPONSE
        # -----------------------------------------------------

        return {
            "success": True,
            "dataset_id": dataset_id,
            "filename": file.filename,
            "rows": len(df),
            "columns": len(df.columns),
            "capabilities": capabilities,
            "column_mapping": mapping,
            "summary": summary,
            "opportunities": opportunity_data,
        }

    except HTTPException:
        raise

    except Exception as exc:

        # Clean failed file
        try:
            upload_path.unlink(
                missing_ok=True
            )
        except Exception:
            pass

        raise HTTPException(
            status_code=400,
            detail=f"Dataset processing failed: {exc}"
        )


@router.get("/opportunities/{dataset_id}")
def get_opportunities(dataset_id: str):

    result = DATASET_RESULTS.get(
        dataset_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found. Upload the dataset again."
        )

    return {
        "success": True,
        "dataset_id": dataset_id,
        "summary": result["summary"],
        "opportunities": result["opportunities"],
    }