from shopping import query_pchome, query_elite
import json
from unittest import mock
import pytest
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_pricing_sort_by_pricing_desc():
    "3, 2, 1"
    with mock.patch(
        "main.shopping.query_elite",
        return_value=[
            {"name": "elite1", "pricing": 100.1},
            {"name": "elite2", "pricing": 90.1}
    ]) as query_elite:
        with mock.patch(
            "main.shopping.query_pchome",
            return_value=[
                {"name": "pchome1", "pricing": 80.1},
                {"name": "pchome2", "pricing": 110.1},
        ]) as query_pchome:
            response = client.get("/pricing?keyword=行動電源&sort_by=pricing")

    data = response.json()

    for pre, curr in zip(data, data[1:]):
        assert pre["pricing"] >= curr["pricing"]


def test_pricing_sort_by_pricing_asc():
    "1, 2, 3"
    with mock.patch(
        "main.shopping.query_elite",
        return_value=[
            {"name": "elite1", "pricing": 100.1},
            {"name": "elite2", "pricing": 90.1}
    ]) as query_elite:
        with mock.patch(
            "main.shopping.query_pchome",
            return_value=[
                {"name": "pchome1", "pricing": 80.1},
                {"name": "pchome2", "pricing": 110.1},
        ]) as query_pchome:
            response = client.get("/pricing?keyword=行動電源&sort_by=-pricing")

    data = response.json()

    for pre, curr in zip(data, data[1:]):
        assert pre["pricing"] <= curr["pricing"]


def test_pricing_will_return_200_with_keyword():
    with mock.patch(
        "main.shopping.query_elite",
        return_value=[{"name": "elite", "pricing": 100.1}]
        ) as query_elite:
        with mock.patch(
            "main.shopping.query_pchome",
            return_value=[{"name": "pchome", "pricing": 100.1}]
        ) as query_pchome:
            response = client.get("/pricing?keyword=行動電源")

    query_elite.assert_called_once_with("行動電源")
    query_pchome.assert_called_once_with("行動電源")
    assert response.status_code == 200
    assert len(response.json()) > 0
    data = response.json()[0]
    assert "name" in data
    assert "pricing" in data

    assert isinstance(data["name"], str)
    assert isinstance(data["pricing"], float)

    assert data["name"] == "pchome"
    data = response.json()[1]
    assert data["name"] == "elite"


@pytest.fixture
def pchome_battery() -> list:
    with open("./pchome_battery.json", encoding="utf-8") as f:
        data = json.loads(f.read())
    return data


def test_query_pchome_will_return_list_of_pricing_and_name(pchome_battery):
    response = mock.Mock()
    response.json.return_value = pchome_battery

    with mock.patch("shopping.requests.get", side_effect=[response]) as get:
        result = query_pchome("行動電源")

    assert len(result) > 0
    assert "pricing" in result[0]
    assert isinstance(result[0]["pricing"], float)

    assert "name" in result[0]
    assert isinstance(result[0]["name"], str)

    assert result[0]["name"] == "超強行動電源"


@pytest.fixture
def elite_battery() -> list:
    with open("./elite_battery.json", encoding="utf-8") as f:
        data = json.loads(f.read())
    return data


def test_query_elite_will_return_list_of_pricing_and_name(elite_battery):
    response = mock.Mock()
    response.json.return_value = elite_battery

    with mock.patch("shopping.requests.get", side_effect=[response]) as get:
        result = query_elite("行動電源")

    assert len(result) > 0
    assert "pricing" in result[0]
    assert isinstance(result[0]["pricing"], float)

    assert "name" in result[0]
    assert isinstance(result[0]["name"], str)

    assert result[0]["name"] == "大方塊行動電源"