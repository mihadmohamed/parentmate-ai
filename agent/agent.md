# Project: ParentMate v1

## Goal
Convert school emails into accurate calendar events automatically, without the parent reading the email.

---

## Inputs
- Raw email text (subject + body)

---

## Outputs
- Structured JSON representing calendar events

Example:
{
  "school_name": null,
  "email_subject": "Year 3 Trip",
  "events": [
    {
      "title": "",
      "event_type": "trip",
      "date": "10 May 2026",
      "start_time": null,
      "end_time": null,
      "location": "",
      "child_specific": null,
      "action_required": false,
      "deadline": null,
      "items_needed": null,
      "cost": null,
      "confidence": 0.9
    }
  ]
}

---

## Rules

- Only extract school-related events
- Ignore non-event content
- Keep date and time strings exactly as stated when possible
- If date/time is unclear → set to null
- Do NOT hallucinate missing information
- Extract multiple events if present
- Do NOT output anything outside JSON
- Output keys must match the application schema exactly

---

## Decision Logic

1. Determine if email contains an event
2. If no event → return empty events array
3. If event exists → extract structured fields
4. If multiple events → return multiple entries

---

## Success Criteria

- ≥90% correct event extraction
- ≤5% false positives
- Clean JSON output every time

---

## Out of Scope

- Non-school emails
- Task extraction
- Notes or summaries
- Calendar editing
- UI formatting

---

## Failure Handling

- If uncertain → leave fields null
- Never guess missing data
- Return empty events array if no event found
