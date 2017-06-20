"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)

    def test_minimax_interface(self):
        """ Test MinimaxPlayer.minimax() interface and output """
        test_depth = 1
        starting_location = (5, 3)
        adversary_location = (0, 0)  # top left corner

        # create a player agent & a game board
        agentMinMax = game_agent.MinimaxPlayer()
        agentMinMax.time_left = lambda: 99  # ignore timeout for fixed-depth search
        board = isolation.Board(agentMinMax, self.player2)

        # place two "players" on the board at arbitrary (but fixed) locations
        board.apply_move(starting_location)
        board.apply_move(adversary_location)

        print(board.print_board())

        for move in board.get_legal_moves():
            next_state = board.forecast_move(move)
            move = agentMinMax.minimax(next_state, test_depth)
            print("Value: {} - Type: {}".format(move, type(move)))
            self.assertIsInstance(move, tuple,
                            ("Minimax function should return a tuple"))


if __name__ == '__main__':
    unittest.main()
