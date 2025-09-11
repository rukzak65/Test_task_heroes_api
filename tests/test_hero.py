import pytest
from hero import get_tallest_hero

TEST_DATA = [
    {"id": 1, "name": "Alpha", "appearance": {"gender": "Male", "height": ["6'0", "183 cm"]}, "work": {"occupation": "Scientist"}},
    {"id": 2, "name": "Beta", "appearance": {"gender": "Female", "height": ["5'9", "175 cm"]}, "work": {"occupation": "-"}},
    {"id": 3, "name": "Gamma", "appearance": {"gender": "Male", "height": ["6'6", "198 cm"]}, "work": {"occupation": ""}},
    {"id": 4, "name": "Delta", "appearance": {"gender": "Male", "height": ["6'6", "198 cm"]}, "work": {"occupation": "Superhero"}},
    {"id": 5, "name": "Givi", "appearance": {"gender": "Male", "height": ["- cm", "0 cm"]}, "work": {"occupation": "Worker"}},
    {"id": 6, "name": "Messi", "appearance": {"gender": "Male", "height": ["6'7", "200 cm"]}, "work": {"occupation": "Worker"}},
    {"id": 7, "name": "George", "appearance": {"gender": "Female", "height": ["6'2", "188 cm"]}, "work": {"occupation": "Detective"}},
    {"id": 8, "name": "Ronaldo", "appearance": {"gender": "Female", "height": ["5'11", "180 cm"]}, "work": {"occupation": "Unknown"}},
    {"id": 9, "name": "StrangeMeters", "appearance": {"gender": "Female", "height": ["200", "61.0 meters"]}, "work": {"occupation": "Giant"}},
    {"id": 10, "name": "NoAppearance", "work": {"occupation": "None"}},
]

def test_tallest_male_without_work():
    res = get_tallest_hero("male", False, heroes=TEST_DATA)
    assert res is not None
    assert res["id"] == 6
    assert res["height_cm"] == 200
    assert res["name"] == "Messi"

def test_tallest_male_with_work():
    res = get_tallest_hero("male", True, heroes=TEST_DATA)
    assert res is not None
    assert res["id"] == 6
    assert res["height_cm"] == 200

def test_tallest_female_without_work():
    res = get_tallest_hero("female", False, heroes=TEST_DATA)
    assert res is not None
    # id 9 самый высокий
    assert res["id"] == 9
    assert res["height_cm"] == 6100

def test_tallest_female_with_work_counts_unknown_as_work():
    res = get_tallest_hero("female", True, heroes=TEST_DATA)
    assert res is not None
    assert res["id"] == 9
    assert res["height_cm"] == 6100

def test_equal_heights_choose_first(): # Проверка на показ только первого
    equal_list = [
        {"id": 101, "name": "A", "appearance": {"gender": "Male", "height": ["6'6", "198 cm"]}, "work": {"occupation": "X"}},
        {"id": 102, "name": "B", "appearance": {"gender": "Male", "height": ["6'6", "198 cm"]}, "work": {"occupation": "X"}},
    ]
    res = get_tallest_hero("male", False, heroes=equal_list)
    assert res is not None
    assert res["id"] == 101
    assert res["height_cm"] == 198
