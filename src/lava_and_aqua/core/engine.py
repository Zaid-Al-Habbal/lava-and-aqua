from core.board import Board
from core.action import MoveAction
from core.observer import Observer
from core.entitiy import Goal, Wall
from utils.types import GamePhase, Direction


class GameEngine:

    
    @staticmethod
    def is_won(board: Board, phase: GamePhase) -> bool:
        if phase == GamePhase.WON:
            return True

        player = board.get_player()
        if player is None:
            return False

        if Observer.has_collected_all_orbs(board, player):
            for ent in board.get_entities_at(player.position):
                if isinstance(ent, Goal):
                    return True

        return False

    @staticmethod
    def is_lost(board: Board, phase: GamePhase) -> bool:
        if phase == GamePhase.LOST:
            return True

        player = board.get_player()
        if player is None:
            return False

        if Observer.player_is_on_lava(board, player):
            return True

        for ent in board.get_entities_at(player.position):
            if isinstance(ent, Wall):
                return True

        return False

    @staticmethod
    def is_terminal(phase: GamePhase) -> bool:
        return phase in [GamePhase.WON, GamePhase.LOST]
    
    @staticmethod
    def is_valid_action(board: Board, phase: GamePhase, action: MoveAction) -> bool:
        if GameEngine.is_terminal(phase):
            return False

        return Observer.is_valid_action(board, action)

    @staticmethod
    def get_available_actions(board: Board, phase: GamePhase) -> list[MoveAction]:
        if GameEngine.is_terminal(phase):
            return []

        available_actions: list[MoveAction] = []
        for direction in Direction:
            move_action = MoveAction(direction)
            if GameEngine.is_valid_action(board, phase, move_action):
                available_actions.append(move_action)

        return available_actions