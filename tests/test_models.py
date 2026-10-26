import pytest

from core.models import City, GameMap, Route


class TestGameMapValidators:
    def test_routes_with_unknown_cities(self):
        cities = [City(id="bal", name="Balassagyarmat", x=0, y=0)]
        routes = [
            Route(id="bud-bal", a="bud", b="bal", length=3, color="gray", type="normal")
        ]

        with pytest.raises(ValueError, match="Unknown cities"):
            GameMap(cities=cities, routes=routes)

    def test_cities_without_routes(self):
        cities = [
            City(id="bal", name="Balassagyarmat", x=0, y=0),
            City(id="bud", name="Budapest", x=1, y=1),
            City(id="esz", name="Esztergom", x=2, y=2),
        ]
        routes = [
            Route(id="bud-bal", a="bud", b="bal", length=3, color="gray", type="normal")
        ]

        with pytest.raises(ValueError, match="Cities without any route"):
            GameMap(cities=cities, routes=routes)

    def test_cities_with_same_coordinates(self):
        cities = [
            City(id="bal", name="Balassagyarmat", x=0, y=0),
            City(id="bud", name="Budapest", x=0, y=0),
        ]
        routes = [
            Route(id="bud-bal", a="bud", b="bal", length=3, color="gray", type="normal")
        ]

        with pytest.raises(ValueError, match="same coordinates"):
            GameMap(cities=cities, routes=routes)


class TestRouteValidators:
    def test_not_allowed_color(self):
        with pytest.raises(ValueError, match="not_allowed_color"):
            Route(
                id="bud-pra",
                a="bud",
                b="pra",
                length=3,
                color="not_allowed_color",
                type="normal",
            )

    def test_not_allowed_type(self):
        with pytest.raises(ValueError, match="not_allowed_type"):
            Route(
                id="bud-pra",
                a="bud",
                b="pra",
                length=3,
                color="gray",
                type="not_allowed_type",
            )

    def test_not_allowed_length(self):
        with pytest.raises(ValueError, match="333"):
            Route(
                id="bud-pra",
                a="bud",
                b="pra",
                length=333,
                color="gray",
                type="normal",
            )

    def test_same_start_and_end_point(self):
        with pytest.raises(ValueError, match="start and end point"):
            Route(
                id="bud-pra",
                a="bud",
                b="bud",
                length=3,
                color="gray",
                type="normal",
            )
