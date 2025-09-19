import pytest
from hero import get_tallest_hero, parse_height_cm

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
def test_api(heroes_api):
    heroes = heroes_api
    assert isinstance(heroes, list) and len(heroes) > 0


def test_get_tallest_male_without_work_api(heroes_api):
    heroes = heroes_api
    expected = _check_expected_from_live(heroes, gender="male", has_work=False)
    if expected is None:
        pytest.skip("В live-данных не найдено подходящих male-героев.")
    result = get_tallest_hero("male", False, heroes=heroes)
    assert result is not None
    assert result["id"] == expected["id"]
    assert result["height_cm"] == expected["height_cm"]


def test_get_tallest_male_with_work_api(heroes_api):
    heroes = heroes_api
    expected = _check_expected_from_live(heroes, gender="male", has_work=True)
    if expected is None:
        pytest.skip("В live-данных не найдено male-героев с работой.")
    result = get_tallest_hero("male", True, heroes=heroes)
    assert result is not None
    assert result["id"] == expected["id"]
    assert result["height_cm"] == expected["height_cm"]

def test_get_tallest_female_with_and_without_work_matches_api(heroes_api):
    heroes = heroes_api

    expected_no_work = _check_expected_from_live(heroes, gender="female", has_work=False)
    if expected_no_work is None:
        pytest.skip("В live-данных не найдено female-героев.")
    result_no_work = get_tallest_hero("female", False, heroes=heroes)
    assert result_no_work is not None
    assert result_no_work["id"] == expected_no_work["id"]
    assert result_no_work["height_cm"] == expected_no_work["height_cm"]

    expected_with_work = _check_expected_from_live(heroes, gender="female", has_work=True)
    if expected_with_work is None:
        pytest.skip("В live-данных не найдено female-героев с работой.")
    result_with_work = get_tallest_hero("female", True, heroes=heroes)
    assert result_with_work is not None
    assert result_with_work["id"] == expected_with_work["id"]
    assert result_with_work["height_cm"] == expected_with_work["height_cm"]



