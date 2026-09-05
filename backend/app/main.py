# from fastapi import FastAPI

# from app.api.upload import router as upload_router


# app = FastAPI(
#     title="AI Revenue Intelligence",
#     version="1.0.0"
# )


# app.include_router(upload_router)


# @app.get("/")
# def root():
#     return {
#         "message": "AI Revenue Intelligence API"
#     }


# @app.get("/health")
# def health():
#     return {
#         "status": "healthy"
#     }




from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.upload import router as upload_router


app = FastAPI(
    title="AI Revenue Intelligence",
    version="1.0.0",
)


# -------------------------
# CORS
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Routes
# -------------------------

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