from core.loader import load_map


def test_default_map_loads():
    game_map = load_map()
    assert len(game_map.cities) > 0