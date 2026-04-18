import json
from pathlib import Path

FILE = Path(__file__).parent / "events.json"

def save_event(data):
    print(">>> SAVING EVENT <<<", data)

    if FILE.exists():
        existing = json.loads(FILE.read_text())
    else:
        existing = []

    existing.append(data)
    FILE.write_text(json.dumps(existing, indent=2))

def load_events():
    if not FILE.exists():
        return []
    return json.loads(FILE.read_text())