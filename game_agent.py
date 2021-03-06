"""This file contains all the classes you must complete for this project.
You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.
You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import math


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def simple_scoring(game,player):

    own_starting_moves = game.get_legal_moves(player)
    number_of_agent_moves = len(own_starting_moves)
    for move in own_starting_moves:
        new_game=game.forecast_move (move)
        number_of_agent_moves += len(new_game.get_legal_moves(player))

    opponent = game.get_opponent(player)
    opp_starting_moves = game.get_legal_moves(opponent)
    number_of_opponent_moves = len(opp_starting_moves)
    for move in opp_starting_moves:
        new_game = game.forecast_move(move)
        number_of_opponent_moves += len(new_game.get_legal_moves(opponent))

    return float(number_of_agent_moves - number_of_opponent_moves)


def complex_heuristic(game, player):
    """ This function will try to grab center squares and increase the difference between the agent's center and
    """
    own_starting_moves = game.get_legal_moves(player)

    number_of_agent_moves = len(own_starting_moves)
    own_dist_from_center = 0
    opp_dist_from_center = 0
    for move in own_starting_moves:
        new_game=game.forecast_move (move)
        number_of_agent_moves += len(new_game.get_legal_moves(player))
        own_dist_from_center += math.sqrt((move[0]-3)** 2 + (move[1]-3)**2)

    opponent = game.get_opponent(player)
    opp_starting_moves = game.get_legal_moves(opponent)
    number_of_opponent_moves = len(opp_starting_moves)
    for move in opp_starting_moves:
        new_game = game.forecast_move(move)
        number_of_opponent_moves += len(new_game.get_legal_moves(opponent))
        opp_dist_from_center+= math.sqrt ( (move[0] - 3) ** 2 + (move[1] - 3) ** 2 )

    return float(number_of_agent_moves - number_of_opponent_moves) + float(own_dist_from_center - opp_dist_from_center)

def close_proximity(game,player):
    """ This function will try to grab center squares and increase the difference between the agent's center and
        """
    own_starting_moves=game.get_legal_moves ( player )

    own_proximity_dist=0
    opp_proximity_dist=0

    for move in own_starting_moves:
        new_game=game.forecast_move ( move )
        all_moves = new_game.get_legal_moves ( player )
        for allmove in all_moves:
            own_proximity_dist+=math.sqrt ( (allmove[0] - move[0]) ** 2 + (allmove[1] - move[1]) ** 2 )

    opponent=game.get_opponent ( player )
    opp_starting_moves=game.get_legal_moves ( opponent )

    for oppmove in opp_starting_moves:
        new_game = game.forecast_move (oppmove)
        all_opp_moves = new_game.get_legal_moves(opponent)
        for alloppmove in all_opp_moves:
            opp_proximity_dist += math.sqrt ( (alloppmove[0] - oppmove[0]) ** 2 + (alloppmove[1] - oppmove[1]) ** 2 )

    return float(own_proximity_dist - opp_proximity_dist)



def custom_score(game, player):
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
    #raise NotImplementedError
    #return simple_scoring(game,player)
    #return complex_heuristic(game, player)
    return close_proximity(game,player)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.
    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)
    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.
    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).
    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().
    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.
        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.
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
        # if there aren't legal moves left, return

        if not legal_moves:
            return (-1,-1)

        best_score=float ( "-inf" )
        best_move=(-1 , -1)
        timeout = False

        self.time_left = time_left


        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            #pass

            if not self.iterative:
                #print ("No iterative Deepening")
                if self.method=="minimax":
                    #print ("depth while calling minimax is:",self.search_depth)
                    best_score, best_move = self.minimax(game,self.search_depth,maximizing_player=True)

                elif self.method=="alphabeta":
                    #print ( "depth while calling alphabeta is:" , self.search_depth )
                    best_score , best_move=self.minimax ( game , self.search_depth , maximizing_player=True )
                else:
                    pass
            else:
                #print ( "iterative Deepening" )
                depth = 1
                while True  :
                    if self.method=="minimax":
                        current_score , current_move=self.minimax ( game , depth , maximizing_player=True )

                    elif self.method=="alphabeta":
                        current_score , current_move=self.minimax ( game , depth , maximizing_player=True )
                    else:
                        pass

                    if current_score > best_score:
                        best_score=current_score
                        best_move=current_move

                    depth += 1

            return best_move

        except Timeout:
            # Handle any actions required at timeout, if necessary
            #pass
            timeout = True
            return best_move

        # Return the best move from the last completed search iteration
        raise NotImplementedError

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)
        Returns
        -------
        float
            The score for the current search branch
        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        #print ( "depth at the entry is:" , depth )
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        best_move=(-1,-1)
        best_score=float ( "-inf" ) if maximizing_player else float ( "inf" )
        # TODO: finish this function!
        if depth != 0:
            #print ("depth is:",depth)
            legal_moves=game.get_legal_moves ( )

            for move in legal_moves:
                # print ("we are dealing with move:", move)
                # print  ("depth is:",depth)
                new_game = game.forecast_move(move)
                if not maximizing_player:
                    # print ( "***************************************************************" )
                    # print ( "Going into minimizing player condition" )
                    # print ( "Calling minimizing player" )
                    current_score , current_move=self.minimax ( new_game , depth - 1 , True )
                    # print ( "current_score after maximizing is:" , current_score )
                    # print ( "current_move after maximizing is:" , current_move )
                    # print ( "best score in the maximizing player condition is:" , best_score )
                    # print ( "***************************************************************" )

                    if current_score < best_score:
                        # print ( "***************************************************************" )
                        # print ( "current score less than the best score" )
                        best_score = current_score
                        best_move = move
                        # print ( "best score after resetting is:" , best_score )
                        # print ( "best move after resetting is:" , best_move )
                        # print ( "***************************************************************" )
                else:
                    # print ("***************************************************************")
                    # print ("Going into maximizing player condition")
                    # print ("Calling minimizing player")
                    current_score , current_move=self.minimax ( new_game , depth - 1 , False)
                    # print ("current_score after minimizing is:",current_score)
                    # print ( "current_move after minimizing is:" , current_move )
                    # print ("best score in the maximizing player condition is:",best_score)
                    # print ( "***************************************************************" )

                    if current_score > best_score:
                        # print ( "***************************************************************" )
                        # print ("current score greater than the best score")
                        best_score = current_score
                        best_move = move

                        # print ("best score after resetting is:", best_score)
                        # print ( "best move after resetting is:" , best_move )
                        # print ( "***************************************************************" )
            return best_score , best_move
        else:
            best_score=self.score ( game , game.inactive_player if not maximizing_player else game.active_player )
            return best_score,best_move


            #raise NotImplementedError

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):

        """Implement minimax search with alpha-beta pruning as described in the
        lectures.
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
        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)
        Returns
        -------
        float
            The score for the current search branch
        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """


        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # print ( "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^" )
        # print ( "Iterative Flag is:", self.iterative )
        # print ( "depth inside alphabeta is:" , depth )
        # print ( "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^" )

        # TODO: finish this function!
        best_move=(-1 , -1)
        best_score=float ( "-inf" ) if maximizing_player else float ( "inf" )

        # TODO: finish this function!
        #print ( "!!!!!!!!!!!!!!!!  outside depth check" , depth )
        if depth != 0:
            # print ("!!!!!!!!!!!!!!!!  inside depth not eq zero",depth)
            # print ("going to get legal moves")
            legal_moves=game.get_legal_moves ( )
            # print ("legal moves are:", legal_moves)
            for move in legal_moves:
                # print ( "we are dealing with move:" , move )
                #print ( "depth is:" , depth )

                if not maximizing_player:
                    # print ( "***************************************************************" )
                    # print ( "Going into minimizing player condition" )
                    # print ( "Calling minimizing player" )
                    # print ( "current move is:" , move )
                    new_game=game.forecast_move ( move )
                    current_score , current_move=self.alphabeta ( new_game , depth - 1 , alpha, beta, True )
                    # print ( "current_score after maximizing is:" , current_score )
                    # print ( "current_move after maximizing is:" , current_move )
                    # print ( "best score in the maximizing player condition is:" , best_score )
                    # print ( "***************************************************************" )
                    if current_score < best_score:
                        # print ( "***************************************************************" )
                        # print ( "current score less than the best score" )
                        best_score=current_score
                        best_move=move
                        # print ( "best score after resetting is:" , best_score )
                        # print ( "best move after resetting is:" , best_move )
                        # print ( "***************************************************************" )
                    if best_score <= alpha:
                        return best_score , best_move
                    if best_score < beta:
                        beta =  best_score
                else:
                    # print ( "***************************************************************" )
                    # print ( "Going into maximizing player condition" )
                    # print ( "Calling minimizing player" )
                    # print ("current move is:",move)
                    new_game=game.forecast_move ( move )
                    current_score , current_move=self.alphabeta ( new_game , depth - 1 ,alpha, beta, False )
                    # print ( "current_score after minimizing is:" , current_score )
                    # print ( "current_move after minimizing is:" , current_move )
                    # print ( "best score in the maximizing player condition is:" , best_score )
                    # print ( "***************************************************************" )

                    if current_score > best_score:
                        # print ( "***************************************************************" )
                        # print ( "current score greater than the best score" )
                        best_score=current_score
                        best_move=move
                        # print ( "best score after resetting is:" , best_score )
                        # print ( "best move after resetting is:" , best_move )
                        # print ( "***************************************************************" )
                    if best_score >= beta:
                        return best_score , best_move
                    if best_score > alpha:
                        alpha = best_score
        else:
            best_score=self.score ( game, game.inactive_player if not maximizing_player else game.active_player)

        return best_score , best_move
        #raise NotImplementedError