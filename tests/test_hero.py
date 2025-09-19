import pytest
import requests
from hero import get_tallest_hero, parse_height_cm

# TEST_DATA = [
#     {"id": 1, "name": "Alpha", "appearance": {"gender": "Male", "height": ["6'0", "183 cm"]}, "work": {"occupation": "Scientist"}},
#     {"id": 2, "name": "Beta", "appearance": {"gender": "Female", "height": ["5'9", "175 cm"]}, "work": {"occupation": "-"}},
#     {"id": 3, "name": "Gamma", "appearance": {"gender": "Male", "height": ["6'6", "198 cm"]}, "work": {"occupation": ""}},
#     {"id": 4, "name": "Delta", "appearance": {"gender": "Male", "height": ["6'6", "198 cm"]}, "work": {"occupation": "Superhero"}},
#     {"id": 5, "name": "Givi", "appearance": {"gender": "Male", "height": ["- cm", "0 cm"]}, "work": {"occupation": "Worker"}},
#     {"id": 6, "name": "Messi", "appearance": {"gender": "Male", "height": ["6'7", "200 cm"]}, "work": {"occupation": "Worker"}},
#     {"id": 7, "name": "George", "appearance": {"gender": "Female", "height": ["6'2", "188 cm"]}, "work": {"occupation": "Detective"}},
#     {"id": 8, "name": "Ronaldo", "appearance": {"gender": "Female", "height": ["5'11", "180 cm"]}, "work": {"occupation": "Unknown"}},
#     {"id": 9, "name": "StrangeMeters", "appearance": {"gender": "Female", "height": ["200", "61.0 meters"]}, "work": {"occupation": "Giant"}},
#     {"id": 10, "name": "NoAppearance", "work": {"occupation": "None"}},
# ]

API_URL = "https://akabab.github.io/superhero-api/api/all.json"
TIME_OUT = 5


def get_all(url):
    try:
        r = requests.get(url, timeout=TIME_OUT)
        r.raise_for_status()
        data = r.json()
        if not isinstance(data, list):
            pytest.skip("Запрос вернул не список.")
        return data
    except Exception as e:
        pytest.skip(f"Не удалось достучаться до API: {e}")

# проверка поля work.occupation в объекте героя h
def _occupation_has_work(h):
    occ = (h.get("work") or {}).get("occupation")
    if not occ or not isinstance(occ, str):
        return False
    if occ.strip() in ("", "-"):
        return False
    return True

#берёт из h поле appearance.gender
def _gender_matches(h, target_gender):
    ap = h.get("appearance") or {}
    hero_gender = ap.get("gender", "")
    if not isinstance(hero_gender, str):
        return False
    return hero_gender.lower() == target_gender


# поиск ожидаемого самого высокого героя для заданного gender и has_work
def _check_expected_from_live(heroes, gender, has_work):
    target = gender.lower()
    candidates = []
    for h in heroes:
        ap = h.get("appearance") or {}
        hero_gender = ap.get("gender", "")
        if not isinstance(hero_gender, str) or hero_gender.lower() != target:
            continue

        occ = (h.get("work") or {}).get("occupation")
        work_ok = isinstance(occ, str) and occ.strip() not in ("", "-")
        if has_work and not work_ok:
            continue

        height_cm = parse_height_cm(ap.get("height"))
        if height_cm is None:
            continue

        candidates.append((h, height_cm))

    if not candidates:
        return None

    expected = max(candidates, key=lambda x: x[1])[0]
    return {
        "id": expected.get("id"),
        "name": expected.get("name"),
        "height_cm": parse_height_cm((expected.get("appearance") or {}).get("height")),
    }

#tests

# проверяем что апи работает
def test_api():
    heroes = get_all(API_URL)
    assert isinstance(heroes, list) and len(heroes) > 0


def test_get_tallest_male_without_work_api():
    heroes = get_all(API_URL)
    expected = _check_expected_from_live(heroes, gender="male", has_work=False)
    if expected is None:
        pytest.skip("В live-данных не найдено подходящих male-героев.")
    result = get_tallest_hero("male", False)
    assert result is not None
    assert result["id"] == expected["id"]
    assert result["height_cm"] == expected["height_cm"]


def test_get_tallest_male_with_work_api():
    heroes = get_all(API_URL)
    expected = _check_expected_from_live(heroes, gender="male", has_work=True)
    if expected is None:
        pytest.skip("В live-данных не найдено male-героев с работой.")
    result = get_tallest_hero("male", True)
    assert result is not None
    assert result["id"] == expected["id"]
    assert result["height_cm"] == expected["height_cm"]

def test_get_tallest_female_with_and_without_work_matches_api():
    heroes = get_all(API_URL)

    expected_no_work = _check_expected_from_live(heroes, gender="female", has_work=False)
    if expected_no_work is None:
        pytest.skip("В live-данных не найдено female-героев.")
    result_no_work = get_tallest_hero("female", False)
    assert result_no_work is not None
    assert result_no_work["id"] == expected_no_work["id"]
    assert result_no_work["height_cm"] == expected_no_work["height_cm"]



# def test_tallest_male_without_work():
#     res = get_tallest_hero("male", False, heroes=TEST_DATA)
#     assert res is not None
#     assert res["id"] == 6
#     assert res["height_cm"] == 200
#     assert res["name"] == "Messi"
#
# def test_tallest_male_with_work():
#     res = get_tallest_hero("male", True, heroes=TEST_DATA)
#     assert res is not None
#     assert res["id"] == 6
#     assert res["height_cm"] == 200
#
# def test_tallest_female_without_work():
#     res = get_tallest_hero("female", False, heroes=TEST_DATA)
#     assert res is not None
#     assert res["id"] == 7
#     assert res["height_cm"] == 188
#
# def test_tallest_female_with_work_counts_unknown_as_work():
#     res = get_tallest_hero("female", True, heroes=TEST_DATA)
#     assert res is not None
#     assert res["id"] == 7
#     assert res["height_cm"] == 188
#
# def test_equal_heights_choose_first(): #должен вернуть только 1
#     equal_list = [
#         {"id": 101, "name": "A", "appearance": {"gender": "Male", "height": ["6'6", "198 cm"]}, "work": {"occupation": "X"}},
#         {"id": 102, "name": "B", "appearance": {"gender": "Male", "height": ["6'6", "198 cm"]}, "work": {"occupation": "X"}},
#     ]
#     res = get_tallest_hero("male", False, heroes=equal_list)
#     assert res is not None
#     assert res["id"] == 101
#     assert res["height_cm"] == 198
#
# def test_invalid_and_missing_fields_do_not_break():
#     broken = [
#         {"id": 201, "name": "Broken1", "appearance": None, "work": {"occupation": "X"}},
#         {"id": 202, "name": "Broken2", "appearance": {"gender": "Male"}, "work": None},
#         {"id": 203, "name": "Valid", "appearance": {"gender": "Male", "height": ["6'1", "185 cm"]}, "work": {"occupation": "X"}},
#     ]
#     res = get_tallest_hero("male", False, heroes=broken)
#     assert res is not None
#     assert res["id"] == 203
#     assert res["height_cm"] == 185
#
# def test_no_matching_returns_none_empty_or_wrong_gender():
#     assert get_tallest_hero("male", False, heroes=[]) is None
#     assert get_tallest_hero("alien", False, heroes=TEST_DATA) is None
#
# def test_zero_and_invalid_height_ignored():
#     res = get_tallest_hero("male", True, heroes=TEST_DATA)
#     assert res is not None
#     assert res["id"] != 5

