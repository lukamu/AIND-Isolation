"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def centrality(game, move):
    x, y = move
    cx, cy = (math.ceil(game.width / 2), math.ceil(game.height / 2))
    return (game.width - cx) ** 2 + (game.height - cy) ** 2 - (x - cx) ** 2 - (y - cy) ** 2


def custom_score(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)

def custom_score_1(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player) or game.is_loser(player):
        return game.utility(player)
    moves = len(game.get_legal_moves())
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(moves - opp_moves + centrality(game, game.get_player_location(player)))


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    raise NotImplementedError


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    raise NotImplementedError


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move


    def terminaltest(self, game):
        """Utility function for minimax algo. Return legals moves, if any, otherwise return +/- inf or 0
         using utility function according to the specs given in pseudocode implementation.

         Parameters
         ----------
         game : isolation.Board
             An instance of the Isolation game `Board` class representing the
             current game state

         Returns
         -------
         Boolean
             Returns true if there are no legal moves left"""

        return True if len(game.get_legal_moves())==0 else False


    def maxvalue(self, game, depth):
        """Implement max search algorithm for minimax as described in AIMA pseudo-code.

         Parameters
         ----------
         game : isolation.Board
             An instance of the Isolation game `Board` class representing the
             current game state

         depth : int
             Depth is an integer representing the maximum number of plies to
             search in the game tree before aborting

         Returns
         -------
         max_val: maximum value, or +/- inf if no moves available
         """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #Test if there are legal moves. If not return utility function value according to pseudocode specs.
        if self.terminaltest(game):
            return game.utility(self)

        # Check if reached the root
        if depth==0:
            return self.score(game, self)

        # max_score at -inf, as specified in pseudocode
        max_score = float("-inf")

        # Get all possible moves at the current state
        possible_moves = game.get_legal_moves()

        for move in possible_moves:
            max_score = max(max_score, self.minvalue(game.forecast_move(move), depth - 1))

        return max_score

    def minvalue(self, game, depth):
        """Implement min search algorithm for minimax as described in AIMA pseudo-code.

         Parameters
         ----------
         game : isolation.Board
             An instance of the Isolation game `Board` class representing the
             current game state

         depth : int
             Depth is an integer representing the maximum number of plies to
             search in the game tree before aborting

         Returns
         -------
         min_val: minimum value, or +/- inf if no moves available
         """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #Test if there are legal moves. If not return utility function value according to pseudocode specs.
        if self.terminaltest(game):
            return game.utility(self)

        # Check if reached the root
        if depth==0:
            return self.score(game, self)

        # min_score at inf, as specified in pseudocode
        min_score = float("inf")

        # Get all possible moves at the current state
        possible_moves = game.get_legal_moves()

        for move in possible_moves:
            min_score = min(min_score, self.maxvalue(game.forecast_move(move), depth - 1))

        return min_score


    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Get all possible moves at the current state
        possible_moves = game.get_legal_moves()

        # Check if there are any legal moves left. If not return (-1,-1) as requested.
        if not possible_moves:
            return (-1,-1)

        # set best_score and best_move values at the lowest
        best_score = float("-inf")
        best_move = (-1,-1)

        for move in possible_moves:
            child_score = self.maxvalue(game.forecast_move(move), depth - 1)
            # Identify the minimum score branch for the opponent.
            if child_score > best_score:
                best_score = child_score
                best_move = move

        print ("best move: {}".format(best_move))
        return best_move



class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """
    def terminaltest(self, game):
        """Utility function for minimax algo. Return legals moves, if any, otherwise return +/- inf or 0
         using utility function according to the specs given in pseudocode implementation.

         Parameters
         ----------
         game : isolation.Board
             An instance of the Isolation game `Board` class representing the
             current game state

         Returns
         -------
         Boolean
             Returns true if there are no legal moves left"""

        return True if len(game.get_legal_moves())==0 else False

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # TODO: finish this function!
        raise NotImplementedError


    def alpha_maxvalue(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement max search algorithm for alpha-beta as described in AIMA pseudo-code.

         Parameters
         ----------
         game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

         Returns
         -------
         max_val: maximum value, or +/- inf if no moves available
         """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #Test if there are legal moves. If not return utility function value according to pseudocode specs.
        if self.terminaltest(game):
            return game.utility(self)

        # Check if reached the root
        if depth==0:
            return self.score(game, self)

        # max_score at -inf, as specified in pseudocode
        max_score = float("-inf")

        # Get all possible moves at the current state
        possible_moves = game.get_legal_moves()

        for move in possible_moves:
            max_score = max(max_score, self.alpha_minvalue(game.forecast_move(move), depth - 1), alpha, beta)
            if max_score >= beta:
                return max_score
            alpha = max(alpha, max_score)

        return max_score

    def alpha_minvalue(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement min search algorithm for alpha-beta as described in AIMA pseudo-code.

         Parameters
         ----------
         game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

         Returns
         -------
         min_val: minimum value, or +/- inf if no moves available
         """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #Test if there are legal moves. If not return utility function value according to pseudocode specs.
        if self.terminaltest(game):
            return game.utility(self)

        # Check if reached the root
        if depth==0:
            return self.score(game, self)

        # min_score at inf, as specified in pseudocode
        min_score = float("inf")

        # Get all possible moves at the current state
        possible_moves = game.get_legal_moves()

        for move in possible_moves:
            min_score = min(min_score, self.alpha_maxvalue(game.forecast_move(move), depth - 1), alpha, beta)
            if min_score <= alpha:
                return min_score
            beta = min(beta, min_score)

        return min_score


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Get all possible moves at the current state
        possible_moves = game.get_legal_moves()

        # Check if there are any legal moves left. If not return (-1,-1) as requested.
        if not possible_moves:
            return (-1, -1)

        # set temp_max and best_move values at the lowest
        best_score = float("-inf")
        best_move = (-1, -1)

        for move in possible_moves:
            score = self.alpha_maxvalue(game.forecast_move(move), depth - 1, alpha, beta)

            # Prune
            if best_score >= beta:
                return best_move

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)


        return best_move