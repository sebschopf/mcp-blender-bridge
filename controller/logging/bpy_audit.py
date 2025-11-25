from pathlib import Path
import json
from datetime import datetime

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def audit_record(record: dict, filename_prefix: str = "inject_") -> Path:
    """Persist an audit record as JSON and return path."""
    ts = datetime.utcnow().isoformat().replace(":", "-")
    fn = LOG_DIR / f"{filename_prefix}{ts}.json"
    fn.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return fn
