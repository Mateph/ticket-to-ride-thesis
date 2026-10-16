import json
from pathlib import Path

from core.models import GameMap

MAP_PATH = Path(__file__).parent / "data" / "map_testmap1.json"

def load_map(path: Path = MAP_PATH) -> GameMap:
    return GameMap.model_validate(json.loads(path.read_text(encoding="utf-8")))

