from core.board import Board
from core.actions import MoveAction
from core.evaluator import GameEvaluator
from core.observers import Observer
from utils.types import GamePhase, Direction


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
    def apply_action(
        board: Board, phase: GamePhase, move_count: int, action: MoveAction
    ) -> tuple[Board, GamePhase, int]:

        player = board.get_player()

        new_board = board

        new_board = new_board.apply_move(player, action.direction)

        new_board = new_board.spread_lava_and_water()
        new_board = new_board.tick_TIMED_DOORs()

        new_move_count = move_count + 1
        new_phase = phase

        if GameEvaluator.is_won(new_board, phase):
            new_phase = GamePhase.WON
        elif GameEvaluator.is_lost(new_board, phase):
            new_phase = GamePhase.LOST

        return new_board, new_phase, new_move_count
