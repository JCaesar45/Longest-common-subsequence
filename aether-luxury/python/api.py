"""Aether LCS — FastAPI backend service.

Exposes a single production endpoint, /lcs, accepting JSON payloads
and returning the longest common subsequence plus metadata.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from lcs_engine import lcs


class LcsRequest(BaseModel):
    a: str = Field(..., min_length=0, max_length=2000, description="First sequence")
    b: str = Field(..., min_length=0, max_length=2000, description="Second sequence")


class LcsResponse(BaseModel):
    subsequence: str
    length: int
    density: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Aether LCS API started")
    yield
    print("Aether LCS API stopped")


app = FastAPI(
    title="Aether LCS API",
    description="Longest Common Subsequence as a service.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "aether-lcs"}


@app.post("/lcs", response_model=LcsResponse)
async def compute_lcs(payload: LcsRequest) -> LcsResponse:
    try:
        result = lcs(payload.a, payload.b)
        return LcsResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=False)
