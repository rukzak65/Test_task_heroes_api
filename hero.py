import requests

API_URL = "https://akabab.github.io/superhero-api/api/all.json"

def parse_height_cm(height_field):
    if not height_field or not isinstance(height_field, list):
        return None
    val = str(height_field[1]).strip().lower()
    if not val.endswith("cm"):
        return None
    try:
        num = int(val.replace("cm", "").strip())
        return num if num > 0 else None
    except Exception:
        return None





