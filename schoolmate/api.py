from fastapi import FastAPI
from pydantic import BaseModel
from extractor import extract_email
from storage import save_event   # ← move this here

app = FastAPI()

class EmailInput(BaseModel):
    subject: str
    body: str

@app.post("/ingest")
def ingest_email(email: EmailInput):
    result = extract_email(email.subject, email.body)

    save_event(result.model_dump())   # ✅ INSIDE function

    return result                     # ✅ INSIDE function