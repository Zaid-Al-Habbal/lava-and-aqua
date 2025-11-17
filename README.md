```
                             _                        ___        _                     
                            | |    __ ___   ____ _   ( _ )      / \   __ _ _   _  __ _ 
                            | |   / _` \ \ / / _` |  / _ \/\   / _ \ / _` | | | |/ _` |
                            | |__| (_| |\ V / (_| | | (_>  <  / ___ \ (_| | |_| | (_| |
                            |_____\__,_| \_/ \__,_|  \___/\/ /_/   \_\__, |\__,_|\__,_|
                                                                        |_|            

```

A Python-based puzzle game engine featuring classic **Lava & Aqua** mechanics. Navigate a grid-based board, collect portal orbs, reach goal positions, and outsmart spreading lava and water hazards.

## Quick Start

### Prerequisites
- **Python 3.13+**
- **UV** (Python package manager)

### Installation & Running

```bash
# navigate to the project
cd lava-and-aqua

# Install dependencies using UV
uv sync

# Run the game
uv run src/lava_and_aqua/main.py
```

### Game Controls
| Key | Action |
|-----|--------|
| `w` | Move up |
| `a` | Move left |
| `s` | Move down |
| `d` | Move right |
| `r` | Reset current level |
| `u` | Undo last move |
| `q` | Quit game |

---

## 📁 Project Structure

```
lava-and-aqua/
├── src/lava_and_aqua/
│   ├── core/                    # Game engine and state management
│   │   ├── state.py            # Immutable GameState container
│   │   ├── board.py            # Board representation and entity management
│   │   ├── entities.py         # Game entity definitions
│   │   ├── actions.py          # Movement action system
│   │   ├── engine.py           # GameEngine state transitions
│   │   ├── evaluator.py        # Win/loss condition evaluation
│   │   ├── observers.py        # Observer pattern for game mechanics
│   │   └── game_manager.py     # Game session and history management
│   ├── utils/
│   │   ├── types.py            # Type definitions and enums
│   │   ├── constants.py        # Game constants and obstacle definitions
│   │   ├── level_loader.py     # JSON level file loading
│   │   └── rendering.py        # ASCII emoji board rendering
│   ├── config.py               # Global configuration
│   └── main.py                 # Interactive demo entry point
├── levels/                      # JSON-based level definitions
│   ├── level_1.json
│   ├── level_4.json
│   ├── level_10.json
│   ├── level_15.json
│   └── test_level.json
├── pyproject.toml              # UV project configuration
├── uv.lock                     # Dependency lock file
└── README.md
```

---

## 🏗️ Architecture & Design Patterns

### Core Design Principles

**1. Immutability-First Approach**
- All core game objects (`GameState`, `Board`, `Entity`) are frozen dataclasses
- State transitions create new objects rather than mutating existing ones
- Enables reliable undo/redo functionality and state history

**2. Separation of Concerns**
- **State Layer**: `GameState` and `Board` manage data representation
- **Logic Layer**: `GameEngine`, `GameEvaluator`, `Observer` handle rules and mechanics
- **Presentation Layer**: `rendering.py` and `main.py` handle UI
- **Utility Layer**: `types.py`, `constants.py` provide shared definitions

**3. Design Patterns Used**

| Pattern | Implementation | Purpose |
|---------|-----------------|---------|
| **Observer** | `Observer` class | Encapsulates game mechanics (spread, collision, movement validation) |
| **State** | `GameState`, `GamePhase` | Represents distinct game states (PLAYING, WON, LOST) |
| **Factory** | `Board.from_dict()`, `create_entity_class()` | Creates objects from configuration and generates entity types dynamically |
| **Facade** | `GameState` and `GameEngine` | Provide unified interface to complex subsystems |
| **Strategy** | `MoveAction`, pathfinding algorithms | Support different action types and search strategies |

---

## 🔗 Class Relationships & Architecture Diagram

### Class Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                     GameState (Frozen)                       │
│              ┌─ Immutable game snapshot                      │
│              ├─ board: Board                                │
│              ├─ phase: GamePhase                            │
│              ├─ move_history: list[MoveAction]              │
│              └─ move_count: int                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ├──────────────┐
                            │              │
                    ┌───────▼──────┐   ┌──▼────────┐
                    │    Board     │   │ GamePhase │
                    │  (Frozen)    │   │  (Enum)   │
                    └──────────────┘   └───────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
        ┌───▼────────┐  ┌──▼────────┐  ┌──▼────────┐
        │ Entities   │  │ Position  │  │Position   │
        │ dict       │  │ Mapping   │  │ Map       │
        └────────────┘  └───────────┘  └───────────┘


┌─────────────────────────────────────────────────────────────┐
│                    Entity Hierarchy                          │
├─────────────────────────────────────────────────────────────┤
│ Entity (Base Class - frozen dataclass)                       │
│ ├─ Player                                                    │
│ │  └─ collected_orbs: frozenset[EntityId]                   │
│ ├─ MetalBox        (created via factory)                     │
│ ├─ Wall            (created via factory)                     │
│ ├─ Goal            (created via factory)                     │
│ ├─ Lava            (created via factory)                     │
│ ├─ Water           (created via factory)                     │
│ ├─ Orb (PortalOrb) (created via factory)                     │
│ ├─ CrackedWall     (created via factory)                     │
│ └─ TimedDoor                                                 │
│    └─ remaining_time: int                                    │
└─────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────┐
│                 Game Logic Components                        │
├─────────────────────────────────────────────────────────────┤
│ GameEngine                                                   │
│ ├─ apply_action(board, phase, move_count, action)            │
│ ├─ apply_move(board, player, direction)                      │
│ └─ get_available_actions(board, phase)                       │
│                                                              │
│ GameEvaluator                                                │
│ ├─ is_won(board, phase)                                     │
│ ├─ is_lost(board, phase)                                    │
│ └─ is_terminal(phase)                                       │
│                                                              │
│ Observer                                                     │
│ ├─ can_move(board, player, direction)                       │
│ ├─ spread_lava_and_water(board)                             │
│ ├─ player_is_on_lava(board, player)                         │
│ └─ has_collected_all_orbs(board, player)                    │
│                                                              │
│ GameManager                                                  │
│ └─ game_states: deque[GameState]  (for undo/redo)           │
└─────────────────────────────────────────────────────────────┘
```

### Interaction Flow

```
main.py
  │
  ├─ LevelLoader.load_level() ──→ JSON file
  │
  ├─ GameState.from_level_data() ──→ Board
  │
  ├─ GameManager.add_state()
  │
  └─ Game Loop:
     │
     ├─ User Input ──→ MoveAction
     │
     ├─ GameState.is_valid_action()
     │   └─ GameEngine.is_valid_action()
     │      └─ Observer.can_move()
     │
     ├─ GameState.update_state()
     │   └─ GameEngine.apply_action()
     │      ├─ apply_move()
     │      │  ├─ Collision detection
     │      │  ├─ Orb collection
     │      │  └─ Metal box pushing
     │      ├─ spread_lava_and_water()
     │      ├─ tick_TIMED_DOORs()
     │      └─ GameEvaluator checks terminal state
     │
     ├─ GameManager.add_state() (history)
     │
     ├─ print_board() ──→ Render to console
     │
     └─ Check win/loss conditions
```

---

## 🎮 Key Game Mechanics

### 1. **Movement & Collision**
- **Player Movement**: 4-directional (UP, DOWN, LEFT, RIGHT)
- **Boundary Checking**: Actions constrained within board bounds
- **Collision Detection**: Observer pattern validates valid moves

### 2. **Metal Box Mechanics**
- Player can **push metal boxes** in the direction of movement
- Boxes can push other boxes (chain reaction)
- Boxes **block lava and water spread**
- Boxes can be pushed into fluids (fluid is destroyed)

### 3. **Spread System**
Two-phase fluid spreading that occurs **after each player move**:

**Phase 1: Water Spread**
- Water spreads to adjacent empty cells (4 directions)
- Water + Lava = Wall (collision creates obstacle)
- Water spreads through cracked walls and portal orbs

**Phase 2: Lava Spread**
- Lava spreads to adjacent empty cells (4 directions)
- Lava + Water = Wall (same collision rule)
- Lava spreads through cracked walls and portal orbs

### 4. **Win Condition**
- Collect **all portal orbs** on the board
- Reach the **goal position**
- Both conditions must be met simultaneously

### 5. **Loss Condition**
- Player touches **lava** during their position update
- Player occupies same cell as **wall** after move

### 6. **Portal Orbs (Collectibles)**
- Must be collected for winning
- Can be in any cell
- Automatically collected when player moves to their position
- Can have water/lava on top (layering)

### 7. **Timed Doors**
- Green blocks that appear for a set duration
- Count down each turn after player moves
- Disappear when timer reaches 0
- Passable when gone

### 8. **Cracked Walls**
- Blue passable obstacles
- Lava and water can spread through them
- Block direct movement (solid)
- Can stack with fluids

---

## 📋 Level File Format

Levels are defined in **JSON format** with entity positioning:

```json
{
  "width": 14,
  "height": 6,
  "entities": {
    "players": [
      { "position": [1, 1] }
    ],
    "metal_boxes": [
      { "position": [5, 3] },
      { "position": [7, 2] }
    ],
    "walls": [
      { "position": [13, 0] },
      { "position": [0, 5] }
    ],
    "goals": [
      { "position": [13, 1] }
    ],
    "lavas": [
      { "position": [3, 5] },
      { "position": [11, 4] }
    ],
    "waters": [
      { "position": [2, 2] }
    ],
    "portal_orbs": [
      { "position": [6, 2] },
      { "position": [10, 3] }
    ],
    "cracked_walls": [
      { "position": [5, 5] }
    ],
    "timed_doors": [
      { "position": [8, 4], "timer": 10 }
    ]
  }
}
```

## 🔧 Core Components Reference

### GameState (`core/state.py`)
**Immutable frozen dataclass representing a game snapshot**

```python
GameState(
    board: Board,
    phase: GamePhase,
    move_history: list[MoveAction],
    move_count: int
)
```

**Key Methods**:
- `from_level_data()`: Create initial state from JSON
- `is_valid_action()`: Validate move possibility
- `update_state()`: Apply action and return new GameState
- `get_available_actions()`: List all valid moves
- `is_won()`, `is_lost()`: Check terminal conditions

### Board (`core/board.py`)
**Manages entity grid with efficient position lookup**

```python
Board(
    width: int,
    height: int,
    entities: dict[EntityId, GameEntity],
    position_map: dict[Coordinate, list[EntityId]],
    player_id: EntityId
)
```

**Key Methods**:
- `from_dict()`: Create from level JSON
- `get_entities_at(position)`: O(1) position lookup
- `update_entity()`, `remove_entity()`, `add_entity()`: Immutable updates
- `get_player()`: Retrieve player entity
- `spread_lava_and_water()`: Trigger fluid mechanics
- `tick_TIMED_DOORs()`: Update door timers

### Entity & Subclasses (`core/entities.py`)

```python
# Frozen base class
Entity(
    entity_id: EntityId,
    entity_type: EntityType,
    position: Position
)

# Special subclasses
Player(collected_orbs: frozenset[EntityId])
TimedDoor(remaining_time: int)

# Dynamically generated via factory
MetalBox, Wall, Goal, Lava, Water, Orb, CrackedWall
```

### GameEngine (`core/engine.py`)
**Orchestrates state transitions and applies actions**

**Responsibilities**:
- Validate actions against board state
- Apply player movement with collision handling
- Manage metal box pushing
- Trigger spread mechanics
- Check terminal conditions

### Observer (`core/observers.py`)
**Implements game mechanics and collision logic**

**Responsibilities**:
- Movement validation (`can_move`, `can_push_box`)
- Fluid spread algorithm
- Orb collection detection
- Lava collision detection
- Timed door countdown

### GameEvaluator (`core/evaluator.py`)
**Determines win/loss conditions**

```python
is_won(board, phase) → bool      # All orbs + at goal
is_lost(board, phase) → bool     # On lava or wall
is_terminal(phase) → bool        # Game ended
```

### GameManager (`core/game_manager.py`)
**Maintains game session history for undo functionality**

```python
game_states: deque[GameState]
add_state(state)
remove_last_state() → GameState
```

---

## 🎨 Rendering System

### Emoji Board Visualization

| Entity | Symbol | Details |
|--------|--------|---------|
| Player | 🤣 | 😭 if on lava, 🥶 if on water |
| Goal | 🏁 | Purple portal exit |
| Portal Orb | 🍉 | Collectible on empty cell |
| Lava | 🔥 | Red hazard (spreads) |
| Water | 💧 | Blue hazard (spreads) |
| Metal Box | 🗄️ | Pushable container |
| Wall | 🧱 | Solid obstacle |
| Cracked Wall | 🚧 | Passable to fluids |
| Timed Door | ⏳ 1️⃣-🔟 | Green timer (10→1 shows countdown) |


---


## 📝 License

This project is open source and available under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

