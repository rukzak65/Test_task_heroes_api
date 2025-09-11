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


def get_tallest_hero(gender: str, has_work: bool = False, heroes: list = None):

    if heroes is None:
        resp = requests.get(API_URL, timeout=10)
        if resp.status_code != 200:
            raise RuntimeError("Не удалось получить данные от API")
        heroes = resp.json()

    tallest = None

    for h in heroes:
        # фильтрация по полу
        if h.get("appearance", {}).get("gender", "").lower() != gender.lower():
            continue

        # фильтрация по работе
        occupation = (h.get("work") or {}).get("occupation")
        if has_work and (not occupation or occupation.strip() in ["-", ""]):
            continue

        # рост
        height_cm = parse_height_cm(h.get("appearance", {}).get("height"))
        if height_cm is None:
            continue

        # выбираем самого высокого
        if tallest is None or height_cm > tallest["height_cm"]:
            tallest = {"id": h.get("id"), "name": h.get("name"), "height_cm": height_cm}

    return tallest


