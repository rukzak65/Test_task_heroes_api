import pytest
import requests


API_URL = "https://akabab.github.io/superhero-api/api/all.json"
REQUEST_TIMEOUT = 5
@pytest.fixture(scope="session")
def heroes_api():
    try:
        r = requests.get(API_URL, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        if not isinstance(data, list):
            pytest.skip("API вернул не список.")
        return data
    except Exception as e:
        pytest.skip(f"Не удалось достучаться до API: {e}")