from core.board import Board
from utils.types import EntityType, GamePhase


class GameSearch:
    """Provides utilities for AI search algorithms (heuristics, hashing, state comparison)."""

    @staticmethod
    def state_hash(board: Board, phase: GamePhase, move_count: int) -> int:
        """Hash function for efficient state comparison in search algorithms."""
        board_hash = hash(
            (
                board.width,
                board.height,
                tuple(sorted(board.entities.keys())),
                tuple(
                    (pos, tuple(sorted(ents)))
                    for pos, ents in sorted(board.position_map.items())
                ),
                board.player_id,
            )
        )
        return hash((board_hash, phase, move_count))

    @staticmethod
    def states_equal(
        board1: Board,
        phase1: GamePhase,
        move_count1: int,
        board2: Board,
        phase2: GamePhase,
        move_count2: int,
    ) -> bool:
        """Equality comparison for state deduplication in search algorithms."""
        return (
            board1.width == board2.width
            and board1.height == board2.height
            and board1.entities == board2.entities
            and board1.position_map == board2.position_map
            and board1.player_id == board2.player_id
            and phase1 == phase2
            and move_count1 == move_count2
        )


    @staticmethod
    def heuristic(board: Board, phase: GamePhase) -> float:
        """Heuristic function for A* algorithm. Estimates distance to goal.

        Uses Manhattan distance from player to goal, plus penalty for uncollected orbs.
        Returns 0 if goal is reached.
        """
        if phase == GamePhase.WON:
            return 0.0

        if phase == GamePhase.LOST:
            return float("inf")

        player = board.get_player()
        if player is None:
            return float("inf")

        goals = board.get_entities_by_type(EntityType.GOAL)
        if not goals:
            return 0.0

        goal = goals[0]

        distance = abs(player.position.x - goal.position.x) + abs(
            player.position.y - goal.position.y
        )

        all_orbs = board.get_entities_by_type(EntityType.PORTAL_ORB)
        uncollected_count = len(all_orbs)

        orb_penalty = uncollected_count * 2.0

        lava_penalty = 0.0
        lavas = board.get_entities_by_type(EntityType.LAVA)
        for lava in lavas:
            lava_dist = abs(player.position.x - lava.position.x) + abs(
                player.position.y - lava.position.y
            )
            if lava_dist <= 2:
                lava_penalty += (3 - lava_dist) * 0.5

        return distance + orb_penalty + lava_penalty
