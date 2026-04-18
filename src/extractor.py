from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI
from pydantic import ValidationError

try:
    from .prompts import (
        EXTRACTION_SYSTEM_PROMPT,
        build_extraction_user_prompt,
    )
    from .schemas import EmailExtraction
except ImportError:
    from prompts import (
        EXTRACTION_SYSTEM_PROMPT,
        build_extraction_user_prompt,
    )
    from schemas import EmailExtraction


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


class ExtractionError(RuntimeError):
    pass


def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ExtractionError(
            "OPENAI_API_KEY is not set. Add it to your environment before running the app."
        )
    return OpenAI(api_key=api_key)


def _parse_response_content(content: str) -> dict[str, Any]:
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ExtractionError("OpenAI returned invalid JSON.") from exc

    if not isinstance(parsed, dict):
        raise ExtractionError("OpenAI returned JSON, but it was not an object.")

    return parsed


def extract_email(email_subject: str, email_body: str) -> EmailExtraction:
    if not email_body.strip():
        raise ExtractionError("Email body is required.")

    client = _get_client()
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_extraction_user_prompt(email_subject, email_body),
            },
        ],
    )

    message = response.choices[0].message.content
    if not message:
        raise ExtractionError("OpenAI returned an empty response.")

    parsed = _parse_response_content(message)

    try:
        return EmailExtraction.model_validate(parsed)
    except ValidationError as exc:
        raise ExtractionError(f"Structured extraction failed validation: {exc}") from exc
