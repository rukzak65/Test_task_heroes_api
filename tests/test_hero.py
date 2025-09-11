import pytest

SAMPLE_DATA = [
    {"id": 1, "name": "Alpha", "appearance": {"gender": "Male", "height": ["6'0", "183 cm"]}, "work": {"occupation": "Scientist"}},
    {"id": 2, "name": "Beta", "appearance": {"gender": "Female", "height": ["5'9", "175 cm"]}, "work": {"occupation": "-"}},
    {"id": 3, "name": "Gamma", "appearance": {"gender": "Male", "height": ["6'6", "198 cm"]}, "work": {"occupation": ""}},
    {"id": 4, "name": "Delta", "appearance": {"gender": "Male", "height": ["6'6", "198 cm"]}, "work": {"occupation": "Superhero"}},
    {"id": 5, "name": "Givi", "appearance": {"gender": "Male", "height": ["- cm", "0 cm"]}, "work": {"occupation": "Worker"}},
    {"id": 6, "name": "Messi", "appearance": {"gender": "Male", "height": ["6'7", "200 cm"]}, "work": {"occupation": "Worker"}},
    {"id": 7, "name": "George", "appearance": {"gender": "Female", "height": ["6'2", "188 cm"]}, "work": {"occupation": "Detective"}},
    {"id": 8, "name": "Ronaldo", "appearance": {"gender": "Female", "height": ["5'11", "180 cm"]}, "work": {"occupation": "Unknown"}}
]