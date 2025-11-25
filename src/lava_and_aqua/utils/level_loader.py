import json
import os
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

    def choose_level() -> str:
        levels_dir = "levels"
        level_files = [f for f in os.listdir(levels_dir) if f.endswith(".json")]
        if not level_files:
            print("No level files found in levels/")
            return None
        print("Available levels:")
        for idx, fname in enumerate(level_files):
            print(f"  {idx + 1}. {fname}")
        while True:
            choice = input("Choose a level by number: ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(level_files):
                    return os.path.join(levels_dir, level_files[idx])
            print("Invalid choice. Try again.")