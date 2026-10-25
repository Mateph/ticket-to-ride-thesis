from pathlib import Path

from core.loader import load_map


def test_testmap1_loads():
    TEST_PATH = Path(__file__).parent.parent / "core" / "data" / "map_testmap1.json"
    game_map = load_map(TEST_PATH)

    assert len(game_map.cities) == 4
    assert len(game_map.routes) == 6

    assert game_map.cities[0].id == "ber"
    assert game_map.cities[0].name == "Berlin"
    assert game_map.cities[0].x == 250
    assert game_map.cities[0].y == 60

    assert game_map.routes[0].id == "bud-vie-1"
    assert game_map.routes[0].a == "bud"
    assert game_map.routes[0].b == "vie"
    assert game_map.routes[0].length == 2
    assert game_map.routes[0].color == "red"
    assert game_map.routes[0].type == "normal"


def test_default_map_loads():
    game_map = load_map()

    assert len(game_map.cities) > 0
    assert len(game_map.routes) > 0

    for city in game_map.cities:
        assert isinstance(city.id, str) and len(city.id) > 0
        assert isinstance(city.name, str) and len(city.name) > 0
        assert isinstance(city.x, (int, float))
        assert isinstance(city.y, (int, float))

    for route in game_map.routes:
        assert isinstance(route.id, str) and len(route.id) > 0
        assert isinstance(route.a, str) and len(route.a) > 0
        assert isinstance(route.b, str) and len(route.b) > 0
        assert isinstance(route.length, int) and route.length > 0
        assert isinstance(route.color, str)
        assert isinstance(route.type, str)
