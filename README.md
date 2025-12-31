```
                             _                        ___        _                     
                            | |    __ ___   ____ _   ( _ )      / \   __ _ _   _  __ _ 
                            | |   / _` \ \ / / _` |  / _ \/\   / _ \ / _` | | | |/ _` |
                            | |__| (_| |\ V / (_| | | (_>  <  / ___ \ (_| | |_| | (_| |
                            |_____\__,_| \_/ \__,_|  \___/\/ /_/   \_\__, |\__,_|\__,_|
                                                                        |_|            

```

A Python-based puzzle game engine featuring classic **Lava & Aqua** mechanics with AI search algorithms can play the game.

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
│   │   ├── entitiy.py          # Game entity definitions
│   │   ├── action.py           # Movement action system
│   │   ├── engine.py           # GameEngine state transitions
│   │   ├── observer.py         # Observer pattern for game mechanics
│   │   └── game_manager.py     # Game session and history management
│   ├── ai/                      # AI solvers and search algorithms
│   │   ├── search.py           # Search algorithm implementations (DFS, BFS, UCS, Hill Climbing, A*)
│   │   ├── problem.py          # Problem definition for AI and search
│   │   ├── node.py             # Node and state representations for search trees
│   │   └── priority_queue.py   # Priority queue implementation for informed search
│   ├── utils/
│   │   ├── types.py            # Type definitions and enums
│   │   ├── constants.py        # Game constants and obstacle definitions
│   │   ├── level_loader.py     # JSON level file loading
│   │   └── rendering.py        # ASCII emoji board rendering
│   ├── main.py                 # Interactive demo entry point
│   └── play.py                 # Game play entry point
├── levels/                      # JSON-based level definitions
│   ├── level_1.json
│   ├── level_4.json
│   ├── level_5.json
│   ├── level_7.json
│   ├── level_9.json
│   ├── level_10.json
│   ├── level_13.json
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
- **Logic Layer**: `GameEngine`, `Observer` handle rules and mechanics
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

## 🤖 AI Algorithms

The project implements several search algorithms to automatically solve puzzle levels. All algorithms are implemented in the `ai/` directory and use a unified problem-solving framework.

### Architecture

The AI system follows a standard problem-solving agent architecture:

```
Problem (Abstract Interface)
  └─ LavaAndAquaProblem
      ├─ actions(state) → list[MoveAction]
      ├─ result(state, action) → GameState
      └─ is_over(state) → bool

Node (Search Node)
  ├─ state: GameState
  ├─ parent: Node | None
  ├─ action: MoveAction | None
  ├─ path_cost: int
  ├─ expand(problem) → list[Node]
  ├─ path_actions() → list[MoveAction]
  ├─ path_states() → list[GameState]
  ├─ ucs_cost() → int
  └─ distance_to_the_goal(goal_pos) → int

SearchAlgorithm
  ├─ problem: Problem
  ├─ solution: Node | None
  ├─ visited: set[int] (hashed states)
  ├─ num_of_created_nodes: int
  └─ search methods (dfs, bfs, ucs, hill_climbing_backtrack, a_star)
```

### Implemented Algorithms

#### 1. **Depth-First Search (DFS)**
- **Type**: Uninformed search
- **Strategy**: Explores as deep as possible before backtracking
- **Implementation**: Recursive DFS with visited state tracking
- **Characteristics**:
  - Memory efficient (O(bm) where b=branching factor, m=max depth)
  - Not optimal (may find suboptimal solutions)
  - Not complete (can get stuck in infinite loops without proper cycle detection)
- **Use Case**: Quick exploration for simple levels

#### 2. **Breadth-First Search (BFS)**
- **Type**: Uninformed search
- **Strategy**: Explores all nodes at current depth before moving to next level
- **Implementation**: Uses `deque` for FIFO frontier management
- **Characteristics**:
  - Complete (finds solution if one exists)
  - Optimal for unweighted graphs (finds shortest path in terms of moves)
  - Memory intensive (O(b^d) where d=depth of solution)
- **Use Case**: Finding shortest solution paths

#### 3. **Uniform Cost Search (UCS)**
- **Type**: Informed search (cost-based)
- **Strategy**: Expands nodes with lowest path cost first
- **Implementation**: Uses priority queue ordered by cumulative path cost
- **Cost Function**: `ucs_cost() = number of lava entities on board`
- **Characteristics**:
  - Optimal (finds least-cost solution)
  - Complete (if solution exists)
  - Explores states with less lava first
- **Use Case**: Minimizing hazards in solution path

#### 4. **Hill Climbing with Backtracking**
- **Type**: Local search with backtracking
- **Strategy**: Greedily moves toward goal, backtracks when stuck
- **Heuristic**: Manhattan distance to goal position
- **Implementation**: 
  - Prioritizes children by distance to goal
  - Recursively explores best options first
  - Backtracks when no solution found
- **Characteristics**:
  - Memory efficient (explores one path at a time)
  - Can get stuck in local optima
  - Fast for well-structured problems
- **Use Case**: Quick solutions when goal is reachable

#### 5. **A* (A-Star)**
- **Type**: Informed search (heuristic-based)
- **Strategy**: Combines path cost (g) and heuristic estimate (h) to guide search
- **Evaluation Function**: `f(n) = g(n) + h(n)`
  - `g(n)`: Number of moves from start (path cost)
  - `h(n)`: Manhattan distance to goal (heuristic)
- **Implementation**: Priority queue ordered by `f(n) = cost + distance_to_goal`
- **Characteristics**:
  - Optimal (if heuristic is admissible)
  - Complete (if solution exists)
  - Efficient (explores fewer nodes than BFS/UCS)
- **Use Case**: Best balance of optimality and efficiency

### Key Components

#### Node Class (`ai/node.py`)
Represents a search node in the state space:
- **State**: Current `GameState` snapshot
- **Parent**: Reference to parent node (for path reconstruction)
- **Action**: The action that led to this state
- **Path Cost**: Cumulative cost from start
- **Methods**:
  - `expand(problem)`: Generates child nodes for all valid actions
  - `path_actions()`: Reconstructs sequence of actions to reach this node
  - `path_states()`: Reconstructs sequence of states to reach this node
  - `ucs_cost()`: Returns cost based on lava count
  - `distance_to_the_goal(goal_pos)`: Manhattan distance heuristic

#### Problem Class (`ai/problem.py`)
Defines the problem interface and game-specific implementation:
- **LavaAndAquaProblem**: Concrete implementation for the game
  - `actions(state)`: Returns all valid moves from current state
  - `result(state, action)`: Applies action and returns new state
  - `is_over(state)`: Checks if state is terminal (won/lost)

#### Priority Queue (`ai/priority_queue.py`)
Min-heap implementation using Python's `heapq`:
- Used by UCS, Hill Climbing, and A* algorithms
- Maintains nodes ordered by evaluation function


### Algorithm Selection Guide

| Algorithm | Best For | Trade-offs |
|-----------|----------|------------|
| **DFS** | Simple levels, memory-constrained | Fast but may find suboptimal solutions |
| **BFS** | Shortest path guarantee | Memory intensive, slower |
| **UCS** | Minimizing hazards | Optimal but explores more states |
| **Hill Climbing** | Quick solutions, clear paths | May get stuck, not optimal |
| **A*** | Best overall performance | Optimal and efficient with good heuristic |

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

