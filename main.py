from pathlib import Path
import json
from typing import Literal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

# Allow the Vite dev server to call this API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


CASE_FILE = Path(__file__).parent / "cases.json"


CaseStatus = Literal["open", "closed"]
CasePriority = Literal["high", "medium", "low"]


class Case(BaseModel):
    id: int
    title: str
    description: str
    status: CaseStatus
    client: str | None = None
    priority: CasePriority | None = None
    createdAt: str


@app.get("/")
def read_root():
    return {"message": "Case Management API"}


@app.get("/cases", response_model=list[Case])
def get_cases():
    """
    Return all cases from the JSON text file.

    For now this reads from file on each request.
    """
    if not CASE_FILE.exists():
        return []

    with CASE_FILE.open() as f:
        data = json.load(f)

    return data