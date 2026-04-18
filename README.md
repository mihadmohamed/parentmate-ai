# ParentMate AI

ParentMate AI extracts school events and parent actions from raw school emails.

## What It Does

- Accepts an email subject and body.
- Uses the OpenAI API to extract structured event data.
- Validates the model output with Pydantic.
- Stores extracted results in `src/events.json`.
- Exposes both a Streamlit UI and a FastAPI endpoint.

## Run The Streamlit App

```bash
streamlit run src/app.py
```

## Run The API

```bash
uvicorn src.api:app --reload
```

Then send a `POST` request to `/ingest`:

```json
{
  "subject": "Year 3 Trip",
  "body": "There will be a school farm trip on 10 May 2026 to AB Farm."
}
```

## Environment

Set `OPENAI_API_KEY` before running extraction.

Optionally set `OPENAI_MODEL`; otherwise the app uses `gpt-4.1-mini`.
