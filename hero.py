import requests

API_URL = "https://akabab.github.io/superhero-api/api/all.json"

def parse_height_cm(height_field):
    if not height_field or not isinstance(height_field, list):
        return None
    val = str(height_field[1]).strip().lower()
    if not val.endswith("cm"):
        return None
    try:
        num = int(val.replace("cm", "").strip())         # "203 cm" -> "203"
    except Exception:
        return None

    if num <= 0:
        return None
    return num

def get_tallest_hero(gender, has_work=False, heroes=None):
    if heroes is None:
        resp = requests.get(API_URL, timeout=10)
        if resp.status_code != 200:
            raise RuntimeError("Не удалось получить данные от API")
        heroes = resp.json()

    if not isinstance(gender, str):
        raise ValueError("gender must be a string 'male' or 'female'")
    target_gender = gender.lower()

    tallest = None
    for h in heroes:
        appearance = h.get("appearance") or {}
        hero_gender = appearance.get("gender", "")
        if not isinstance(hero_gender, str) or hero_gender.lower() != target_gender:
            continue

        occupation = (h.get("work") or {}).get("occupation")
        if has_work and (not occupation or occupation.strip() in ["-", ""]):
            continue

        height_cm = parse_height_cm(appearance.get("height"))
        if height_cm is None:
            continue

        if tallest is None or height_cm > tallest["height_cm"]:
            tallest = {"id": h.get("id"), "name": h.get("name"), "height_cm": height_cm}

    return tallest
