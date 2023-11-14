#!/usr/bin/python3
# Set the path to your python3 above

"""
Go0 random Go player
Cmput 455 sample code
Written by Cmput 455 TA and Martin Mueller
"""
from gtp_connection import GtpConnection
from board_base import DEFAULT_SIZE, GO_POINT, GO_COLOR, BLACK, WHITE,EMPTY
from board import GoBoard
from board_util import GoBoardUtil
from engine import GoEngine
import copy

class Go0(GoEngine):
    def __init__(self) -> None:
        """
        Go player that selects moves randomly from the set of legal moves.
        Does not use the fill-eye filter.
        Passes only if there is no other legal move.
        """
        GoEngine.__init__(self, "Go0", 1.0)

    def get_move(self, board: GoBoard, color: GO_COLOR) -> GO_POINT:
        return GoBoardUtil.generate_random_move(board, color, 
                                                use_eye_filter=False)
    
    def solve(self, board: GoBoard):
        """
        A2: Implement your search algorithm to solve a board
        Change if deemed necessary
        """
        pass

class SimulationPlayer(object):
    def __init__(self, numSimulations):
        self.numSimulations = numSimulations

    def name(self):
        return "Simulation Player ({0} sim.)".format(self.numSimulations)

    def genmove(self, state: GoBoard):
        moves = state.get_empty_points()
        numMoves = len(moves)
        score = [0] * numMoves
        for i in range(numMoves):
            move = moves[i]
            score[i] = self.simulate(state, move)
        bestIndex = score.index(max(score))
        best = moves[bestIndex]
        return best

    def simulate(self, state: GoBoard, move: GO_POINT):
        stats = [0] * 3
        state_copy = copy.deepcopy(state)
        state_copy.play_move(move, state.current_player)
        for i in range(self.numSimulations):
            winner = state_copy.simulateMoves(move)
            stats[winner] += 1
            state_copy = copy.deepcopy(state)
        
        assert sum(stats) == self.numSimulations
        eval = (stats[BLACK] + 0.5 * stats[EMPTY]) / self.numSimulations
        if state.current_player == WHITE:
            eval = 1 - eval
        return eval

# def simulate(self, policytype: str, state, move):
#     n = 10
#     stats = [0] * 3
#     state.play(move)
#     moveNr = state.moveNumber()
#     for _ in range(self.numSimulations):
#         winner, _ = state.simulate()
#         stats[winner] += 1
#         state.resetToMoveNumber(moveNr)
#     assert sum(stats) == self.numSimulations
#     assert moveNr == state.moveNumber()
#     state.undoMove()
#     eval = (stats[BLACK] + 0.5 * stats[EMPTY]) / self.numSimulations
#     if state.toPlay == WHITE:
#         eval = 1 - eval
#     return eval
    
def run() -> None:
    """
    start the gtp connection and wait for commands.
    """
    board: GoBoard = GoBoard(DEFAULT_SIZE)
    con: GtpConnection = GtpConnection(Go0(), board)
    sim: SimulationPlayer = SimulationPlayer(10)
    con.start_connection(sim)


if __name__ == "__main__":
    run()
