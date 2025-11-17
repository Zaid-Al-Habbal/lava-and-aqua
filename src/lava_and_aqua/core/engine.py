from core.board import Board
from core.actions import MoveAction
from core.evaluator import GameEvaluator
from core.entities import MetalBox, Orb, Player
from core.observers import Observer
from utils.types import GamePhase, Direction
from utils.constants import FLUID_ENTITIES


class GameEngine:

    @staticmethod
    def is_valid_action(board: Board, phase: GamePhase, action: MoveAction) -> bool:
        if GameEvaluator.is_terminal(phase):
            return False

        return Observer.is_valid_action(board, action)

    @staticmethod
    def get_available_actions(board: Board, phase: GamePhase) -> list[MoveAction]:
        if GameEvaluator.is_terminal(phase):
            return []

        available_actions: list[MoveAction] = []
        for direction in Direction:
            move_action = MoveAction(direction)
            if GameEngine.is_valid_action(board, phase, move_action):
                available_actions.append(move_action)

        return available_actions
    @staticmethod
    def apply_move(board: Board, player: Player, direction: Direction) -> Board:
        target_pos = player.position.move(direction.dx, direction.dy)
        entities_at_target = board.get_entities_at(target_pos)

        if entities_at_target is None or len(entities_at_target) == 0:
            pass  
        else:
            box = None
            for entBox in entities_at_target:
                if isinstance(entBox, MetalBox):
                    box = entBox
                    break
            if box is not None:
                box_target = target_pos.move(direction.dx, direction.dy)
                entity_behind_box = board.get_entities_at(box_target)

                if entity_behind_box is not None:
                    for ent in entity_behind_box:
                        if ent.entity_type in FLUID_ENTITIES:
                            board = board.remove_entity(ent.entity_id)

                moved_box = entities_at_target[0].move_to(box_target)
                board = board.update_entity(moved_box)

            orb = None
            for entOrb in entities_at_target:
                if isinstance(entOrb, Orb):
                    orb = entOrb
                    break
            if orb is not None:
                player = player.collect_orb(orb.entity_id)
                board = board.remove_entity(orb.entity_id)

        moved_player = player.move_to(target_pos)
        board = board.update_entity(moved_player)

        return board

    @staticmethod
    def apply_action(
        board: Board, phase: GamePhase, move_count: int, action: MoveAction
    ) -> tuple[Board, GamePhase, int]:

        player = board.get_player()

        new_board = board

        new_board = GameEngine.apply_move(new_board, player, action.direction)

        new_board = new_board.spread_lava_and_water()
        new_board = new_board.tick_TIMED_DOORs()

        new_move_count = move_count + 1
        new_phase = phase

        if GameEvaluator.is_won(new_board, phase):
            new_phase = GamePhase.WON
        elif GameEvaluator.is_lost(new_board, phase):
            new_phase = GamePhase.LOST

        return new_board, new_phase, new_move_count
