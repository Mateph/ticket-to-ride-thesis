import pytest

from core.models import City, GameMap, Route


def test_routes_with_unknown_cities():
    cities = [City(id="bal", name="Balassagyarmat", x=0, y=0)]
    routes = [
        Route(id="bud-bal", a="bud", b="bal", length=3, color="gray", type="normal")
    ]

    with pytest.raises(ValueError):
        GameMap(cities=cities, routes=routes)


def test_cities_without_routes():
    cities = [
        City(id="bal", name="Balassagyarmat", x=0, y=0),
        City(id="bud", name="Budapest", x=1, y=1),
        City(id="esz", name="Esztergom", x=2, y=2),
    ]
    routes = [
        Route(id="bud-bal", a="bud", b="bal", length=3, color="gray", type="normal")
    ]

    with pytest.raises(ValueError):
        GameMap(cities=cities, routes=routes)


def test_cities_with_same_coordinates():
    cities = [
        City(id="bal", name="Balassagyarmat", x=0, y=0),
        City(id="bud", name="Budapest", x=0, y=0),
    ]
    routes = [
        Route(id="bud-bal", a="bud", b="bal", length=3, color="gray", type="normal")
    ]

    with pytest.raises(ValueError):
        GameMap(cities=cities, routes=routes)
