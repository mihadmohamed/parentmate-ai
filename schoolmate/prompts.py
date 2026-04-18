from __future__ import annotations

import json

from schemas import EmailExtraction


EXTRACTION_SYSTEM_PROMPT = """
You extract school events and parent actions from school emails.

Return JSON only.
Do not wrap the JSON in markdown.
Do not include explanations or extra keys.
Never invent data.
Use null for any unknown scalar value.
Use null for items_needed when the email does not mention any items.
Extract every distinct event, reminder, deadline, payment, permission slip, volunteer request, or parent action mentioned in the email.
If the email contains no events or actions, return an empty events array.
Keep date and time strings exactly as stated when possible.
Set child_specific to true only when the email clearly targets a specific child, class, grade, team, or group.
Set action_required to true only when the email clearly asks for a parent or student action.
Confidence must be a number between 0 and 1.
""".strip()


def build_extraction_user_prompt(email_subject: str, email_body: str) -> str:
    schema = EmailExtraction.model_json_schema()
    return f"""
Extract structured school events and parent actions from the email below.

Output must be valid JSON matching this schema:
{json.dumps(schema, indent=2)}

EMAIL SUBJECT:
{email_subject.strip() or "(empty subject)"}

EMAIL BODY:
{email_body.strip()}v 
""".strip()
