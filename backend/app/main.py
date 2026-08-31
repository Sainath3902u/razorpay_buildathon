from fastapi import FastAPI

from app.api.upload import router as upload_router


app = FastAPI(
    title="AI Revenue Intelligence",
    version="1.0.0"
)


app.include_router(upload_router)


@app.get("/")
def root():
    return {
        "message": "AI Revenue Intelligence API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }