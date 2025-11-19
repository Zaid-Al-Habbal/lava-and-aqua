from core.board import Board
from core.entitiy import Goal, Wall
from core.observer import Observer
from utils.types import GamePhase


class GameEvaluator:

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
