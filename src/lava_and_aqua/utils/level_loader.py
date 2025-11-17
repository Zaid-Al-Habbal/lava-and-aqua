import json
from pathlib import Path
from typing import Any


class LevelLoader:
    """Handles loading level data from JSON files."""

    @staticmethod
    def load_level(level_path: Path | str) -> dict[str, Any]:
        
        path = Path(level_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Level file not found: {path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return LevelLoader.validate_level_data(data)

    @staticmethod
    def validate_level_data(data: dict[str, Any]) -> dict[str, Any]:
        
        if "width" not in data:
            raise ValueError("Level data missing 'width' field")
        
        if "height" not in data:
            raise ValueError("Level data missing 'height' field")
        
        if "entities" not in data:
            data["entities"] = []
        
        
        return data

    @staticmethod
    def save_level(level_data: dict[str, Any], level_path: Path | str) -> None:
        
        path = Path(level_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(level_data, f, indent=2)
