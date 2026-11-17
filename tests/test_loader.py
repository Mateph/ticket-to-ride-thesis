import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from core.loader import load_map


def test_loader_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_map(Path("this_file_does_not_exist.json"))


def test_loader_invalid_json(tmp_path):
    bad_file = tmp_path / "bad_map.json"

    invalid_data = {"cities": [{"id": "bud", "name": "Budapest", "x": 0, "y": 0}]}
    bad_file.write_text(json.dumps(invalid_data))

    with pytest.raises(ValidationError):
        load_map(bad_file)
