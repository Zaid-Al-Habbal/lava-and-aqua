from utils.types import EntityType


def create_grid(width: int, height: int) -> list[list[str]]:
    return [["◻️" for _ in range(width)] for _ in range(height)]


def render_grid_state(board, position_map, entities) -> list[list[str]]:
    grid = create_grid(board.width, board.height)

    for pos, ents in position_map.items():
        x, y = pos
        entity_types = [entities[ent_id].entity_type for ent_id in ents]

        if EntityType.PLAYER in entity_types:
            if EntityType.WATER in entity_types:
                grid[y][x] = "🥶"
            elif EntityType.LAVA in entity_types:
                grid[y][x] = "😭"
            else:
                grid[y][x] = "🤣"

        elif EntityType.METAL_BOX in entity_types:
            grid[y][x] = "🗄️"

        elif EntityType.LAVA in entity_types:
            if EntityType.CRACKED_WALL in entity_types:
                grid[y][x] = "🛑"
            elif EntityType.PORTAL_ORB in entity_types:
                grid[y][x] = "🌶️"
            else:
                grid[y][x] = "🔥"

        elif EntityType.GOAL in entity_types:
            grid[y][x] = "🏁"

        elif EntityType.WATER in entity_types:
            if EntityType.CRACKED_WALL in entity_types:
                grid[y][x] = "❄️"
            elif EntityType.PORTAL_ORB in entity_types:
                grid[y][x] = "🍇"
            else:
                grid[y][x] = "💧"

        elif EntityType.PORTAL_ORB in entity_types:
            grid[y][x] = "🍉"

        elif EntityType.CRACKED_WALL in entity_types:
            grid[y][x] = "🚧"

        elif EntityType.TIMED_DOOR in entity_types:
            from core.entitiy import TimedDoor

            for ent_id in ents:
                entity = entities[ent_id]
                if isinstance(entity, TimedDoor):
                    if entity.remaining_time <= 10:
                        nums = [
                            "1️⃣",
                            "2️⃣",
                            "3️⃣",
                            "4️⃣",
                            "5️⃣",
                            "6️⃣",
                            "7️⃣",
                            "8️⃣",
                            "9️⃣",
                            "🔟",
                        ]
                        grid[y][x] = nums[entity.remaining_time - 1]
                    else:
                        grid[y][x] = "⏳"

        elif EntityType.WALL in entity_types:
            grid[y][x] = "🧱"

    return grid


def print_board(game_state) -> None:
    grid = render_grid_state(
        game_state.board,
        game_state.board.position_map,
        game_state.board.entities,
    )

    print("\n" + "                                " + "🟦" * (game_state.board.width + 2))
    for row in grid:
        print("                                " + "🟦" + "".join(row) + "🟦")
    print("                                " + "🟦" * (game_state.board.width + 2))
    print(game_state)
    print()
