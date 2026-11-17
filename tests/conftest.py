from pathlib import Path

import pytest

from core.loader import load_map
from core.models import GameMap, GameState
from core.rules import new_game
from main import store


@pytest.fixture
def game_map() -> GameMap:
    return load_map(Path(__file__).parent / "testdata" / "testmap1.json")


@pytest.fixture
def state(game_map) -> GameState:
    return new_game(game_map=game_map, player_names=["apple", "pear"])


@pytest.fixture
def reset_game_state(game_map):
    store["game_state"] = new_game(game_map=game_map, player_names=["apple", "pear"])
