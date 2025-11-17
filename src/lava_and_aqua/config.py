from pathlib import Path

# Project structure
PROJECT_ROOT = Path(__file__).parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
SPRITES_DIR = ASSETS_DIR
LEVELS_DIR = PROJECT_ROOT / "levels"

# Game settings
TILE_SIZE = 32  # Size of each tile in pixels
FPS = 60  # Frames per second for the game loop

# Display settings
WINDOW_TITLE = "Lava and Aqua"
BACKGROUND_COLOR = (20, 20, 30)  # Dark blue-gray

# Sprite file names (to be loaded from SPRITES_DIR)
SPRITE_FILES = {
    "player": "player.png",
    "lava": "lava.png",
    "water": "water.png",
    "metal_box": "metal_box.png",
    "TIMED_DOOR": "TIMED_DOOR.png",
    "cracked_wall": "cracked_wall.png",  # Blue corner blocks
    "portal_orb": "portal_orb.png",  # Purple dots
    "wall": "wall.png",
    "goal": "goal.png",  # Purple portal
    "button": "button.png",
    "black_block": "black_block.png",
    "empty": None,  # No sprite for empty tiles
}

# Input mapping
KEY_BINDINGS = {
    "move_up": ["w", "up"],
    "move_down": ["s", "down"],
    "move_left": ["a", "left"],
    "move_right": ["d", "right"],
    "undo": ["z", "u"],
    "restart": ["r"],
    "quit": ["escape", "b"],
}

# Default level
DEFAULT_LEVEL = "level_15.json"

# Debug settings
DEBUG_MODE = False
SHOW_GRID = True
SHOW_FPS = True


