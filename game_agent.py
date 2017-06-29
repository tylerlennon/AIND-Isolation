"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
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
    # TODO: finish this function!
    # raise NotImplementedError


    # test for terminal conditions
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    
    # this is the improved_score heuristic
    # temporary testing for now
    #own_moves = len(game.get_legal_moves(player))
    #opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    #return float(own_moves - opp_moves)


    # Short Term Fortune Teller
    # This heuristic simply calculates the number of escape moves for the current legal move list.  The intent is to reward 
    # boards that have the most options for escaping. Allows the current iteration so see one level past the current one
    own_moves = game.get_legal_moves(player)
    own_escape_count = 0

    for move in own_moves:
        forecasted_game = game.forecast_move(move)
        own_escape_count += len(forecasted_game.get_legal_moves(player))

    opp_moves = game.get_legal_moves(game.get_opponent(player))
    opp_escape_count = 0

    for move in opp_moves:
        forecasted_game = game.forecast_move(move)
        opp_escape_count += len(forecasted_game.get_legal_moves(game.get_opponent(player)))    

    return float(own_escape_count - opp_escape_count)   


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
    #raise NotImplementedError

    
    # test for terminal conditions
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # Nobody Puts Baby in the Corner:
    # This heuristic is based on the fact that corner moves poor choices for the isolation player move selection.
    # This fact also becomes worse as there are less legal moves to select from in later stages of the game.
    # This heuristic rewards remaining legal moves against the opponent and penelizes both players scores depending on 
    # the stage of the game, how many corners are remaining in the legal move list and by how many of the corner escape moves
    # are left


    # define the corners of the board
    top_left     = (0,0)
    top_right    = (game.width-1, 0)
    bottom_left  = (0, game.height-1)
    bottom_right = (game.width-1, game.height-1)           
    corners = [top_left, top_right, bottom_left, bottom_right]
    
    # define the escape moves from the corners
    corner_escapes = [];
    for corner in corners:
        
        # get the x coordinates for the escape move
        if (corner[0]==0):
            x1 = corner[0] + 1
            x2 = corner[0] + 2

        if (corner[0] == game.width-1):
            x1 = corner[0] - 1
            x2 = corner[0] - 2 

        # get the y coordinates for the escape move    
        if (corner[1] == 0):
            y1 = corner[1] + 2
            y2 = corner[1] + 1

        if (corner[1] == game.height-1):
            y1 = corner[1] - 2
            y2 = corner[1] - 1

        # add escape moves to the list    
        corner_escapes.append([x1,y1])
        corner_escapes.append([x2,y2])               


    # get remaining legal moves
    own_moves = game.get_legal_moves(player)
    
    # get the remaining moves that are corners
    own_corner_moves = [move for move in own_moves if move in corners]
    
    # get the remaining corner move escapes
    own_corner_escape_moves = [move for move in own_corner_moves if move in corner_escapes]

    

    # get remaining legal moves for the opponent
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    # get the remaining moves that are corners for the opponent
    opp_corner_moves = [move for move in opp_moves if move in corners]
    
    # get the remaining corner move escapes for the opponent
    opp_corner_escape_moves = [move for move in opp_corner_moves if move in corner_escapes]
    

    
    # get the stage of the game penalty
    game_stage_penalty = 1
    if len(game.get_blank_spaces()) < game.width * game.height / 2:
        game_stage_penalty = 2
    if len(game.get_blank_spaces()) < game.width * game.height / 3:
        game_stage_penalty = 3
    if len(game.get_blank_spaces()) < game.width * game.height / 4:
        game_stage_penalty = 4

    

    # get own penalty of escape moves
    own_escape_penalty = len(own_corner_moves)*2 - len(own_corner_escape_moves)
    if own_escape_penalty == 0:
        own_escape_penalty = 1    

    # get opp penalty of escape moves
    opp_escape_penalty = len(opp_corner_moves)*2 - len(opp_corner_escape_moves)
    if opp_escape_penalty == 0:
        opp_escape_penalty = 1


    # calculate the heuristic
    return float( len(own_moves) - 
        (len(own_corner_moves) * own_escape_penalty * game_stage_penalty) - 
        len(opp_moves) + 
        (len(opp_corner_moves) * opp_escape_penalty * game_stage_penalty) )   


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
    # raise NotImplementedError


    # test for terminal conditions
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # Keeping My Options Open:    
    # This heuristic simply returns the sum of the amount of legal moves and 
    # the number of blank game locations. The intention is to reward a higher score for games that have the 
    # most options available in each move.
    # We may need to adjust this strategy as the legal moves converges on the number of remaining blank game locations
    # This threshold is currently set to when 1/2 of the game locations have been filled
    # Once the threshold has been hit we move into an agressive imporved score heuristic
    # Temporary testing continues


    # get the number of legal moves
    number_own_moves = len(game.get_legal_moves(player))

    #get the number of legal moves for the opponent
    number_opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    # get the remaining blank spaces
    number_remaining_moves = len(game.get_blank_spaces())

    if (len(game.get_blank_spaces()) > game.width * game.height / 2):
        score = (number_own_moves + number_remaining_moves)
    else:
        score = number_own_moves-(2*number_opp_moves)


    return float(score)


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

        # TODO: finish this function!
        # raise NotImplementedError

        # get legal moves (active player = default)
        legalMoves = game.get_legal_moves()
        
        # initialize the best move/score variables 
        bestMove = (-1,-1)
        bestScore = float("-inf")

        # iterate the legal moves list to determine the best move
        for move in legalMoves:
            
            # make a copy of the game with the current move
            forecastedGame = game.forecast_move(move)

            # recursively expand this node to the next depth returning the best score
            # the min MinValue/MaxValue helper funcitons alternate in their recursive calls 
            forecastedScore = self.MinValue(forecastedGame, depth-1)    

            # update best score/move if the current move is better
            if forecastedScore > bestScore:
                bestScore = forecastedScore
                bestMove = move      
                
        # return the best move
        return bestMove
    

    def MaxValue(self, game, depth):
        """
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
        float
            The max score of the current search branch

        Notes
        -----
        - This helper function calls the MinValue methode to reflect the best value for the opposition score
        - The recursive calls for both of these functions is terminated by:
                1. Time threshold expiry
                2. No more legal moves are available
                3. Depth has been reached
        """

        # terminal test: time has expired
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # get the actions for this state
        legalMoves = game.get_legal_moves()        

        # terminal tests
        if not legalMoves:
            return game.utility(self) 

        # terminal test: we have reached our depth limit
        if depth == 0:
            return  self.score(game,self)    

        # initialize the variable for the best score
        maxScore = float("-inf")

        # iterate the legal moves list to determine the max score    
        for move in legalMoves:

            # make a copy of the game with the current move
            forecastedGame = game.forecast_move(move)
                
            # get the score with the forecasted move    
            value = self.MinValue(forecastedGame, depth-1)

            # update best score
            if value > maxScore:
                maxScore = value 

        return maxScore    

    def MinValue(self, game, depth):

        """
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
        float
            The min score of the current search branch

        Notes
        -----
        - This helper function calls the MaxValue methode to reflect the best value for the initial player score
        - The recursive calls for both of these functions is terminated by:
                1. Time threshold expiry
                2. No more legal moves are available
                3. Depth has been reached
        """

        # terminal test: time has expired
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # get the actions for this state
        legalMoves = game.get_legal_moves()        

        # terminal test: no legal moves left
        if not legalMoves:
            return game.utility(self) 

        # terminal test: we have reached our depth limit     
        if  depth == 0:
            return self.score(game,self)

        
        # initialize the variable for the best score
        minScore = float("inf")

        # iterate the legal moves list to determine the min score
        for move in legalMoves:

            # make a copy of the game with the current move
            forecastedGame = game.forecast_move(move)
                
            # get the score with the forecasted move    
            value = self.MaxValue(forecastedGame, depth-1)

            # update best score
            if value < minScore:
                minScore = value

        return minScore        


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

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
        #raise NotImplementedError

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        # instead of returning the default -1,-1 default lets return a random legal move
        
        # get list of legal moves
        legalMoves = game.get_legal_moves()

        # check if there are legal moves
        if not legalMoves:
            return (-1,-1)

        # get a random position
        randomMovePosition = random.randint(0,len(legalMoves)-1)
        
        # set the default best move with a random legal move
        best_move = legalMoves[randomMovePosition]  

        #iterative deepening depth variable
        depth = 1

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            #return self.alpahbeta(game, self.search_depth)

            while True:
                best_move = self.alphabeta(game, depth)
                depth  = depth + 1;

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move


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

        # TODO: finish this function!
        #raise NotImplementedError

        # initialize the best move/score variables 
        bestScore = float("-inf")

        # get legal moves (active player = default)
        legalMoves = game.get_legal_moves()
        
        # terminal test: no legal moves left - return default
        if not legalMoves:
            return (-1,-1)

        # get a random position
        randomMovePosition = random.randint(0,len(legalMoves)-1)
        
        # set the best move with a random legal move
        bestMove = legalMoves[randomMovePosition]    

        # terminal test: we have reached our depth limit - return the first move 
        if depth == 0:
            return  legalMove[0] 

        
        # iterate the legal moves list to determine the best move
        for move in legalMoves:
            
            # make a copy of the game with the current move
            forecastedGame = game.forecast_move(move)

            # recursively expand this node to the next depth returning the best score
            # the min MinValue/MaxValue helper funcitons alternate in their recursive calls 
            forecastedScore = self.MinValue(forecastedGame, depth-1, alpha, beta)    

            # update best score/move if the forecasted move is better
            if forecastedScore > bestScore:
                bestScore = forecastedScore
                bestMove = move 

            # update teh beta limit
            if bestScore >= beta:
                return bestMove   

            # update the alpha limit
            alpha = max(alpha, bestScore)     
    
        # return the best move
        return bestMove

    def MaxValue(self, game, depth, alpha, beta):
        """
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
        float
            The max score of the current search branch

        Notes
        -----
        - This helper function calls the MinValue methode to reflect the best value for the opposition score
        - The recursive calls for both of these functions is terminated by:
                1. Time threshold expiry
                2. No more legal moves are available
                3. Depth has been reached
        """

        # terminal test: time has expired
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # get the actions for this state
        legalMoves = game.get_legal_moves()        

        # terminal test: no legal moves left - return the utility function value
        if not legalMoves:
            return game.utility(self) 

        # terminal test: we have reached our depth limit - return the current score value
        if depth == 0:
            return  self.score(game,self)    

        # initialize the variable for the best score
        value = float("-inf")

        # iterate the legal moves list to determine the max score    
        for move in legalMoves:    

            # make a copy of the game with the current move
            forecastedGame = game.forecast_move(move)
                
            # get the max value score with the forecasted move    
            value = max(value, self.MinValue(forecastedGame, depth-1, alpha, beta))

            # prune the rest of the nodes (moves)
            if value >= beta:
                return value

            # update the alpha limit
            alpha = max(alpha, value)    
            
        return value

    
    def MinValue(self, game, depth, alpha, beta):

        """
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
        float
            The min score of the current search branch

        Notes
        -----
        - This helper function calls the MaxValue methode to reflect the best value for the initial player score
        - The recursive calls for both of these functions is terminated by:
                1. Time threshold expiry
                2. No more legal moves are available
                3. Depth has been reached
        """

        # terminal test: time has expired
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # get the actions for this state
        legalMoves = game.get_legal_moves()        

        # terminal test: no legal moves left - return the utility function value
        if not legalMoves:
            return game.utility(self) 

        # terminal test: we have reached our depth limit - return the current score value    
        if  depth == 0:
            return self.score(game,self)

        # initialize the variable for the best score
        value = float("inf")

        # iterate the legal moves list to determine the min score
        for move in legalMoves:

            # make a copy of the game with the current move
            forecastedGame = game.forecast_move(move)
                
            # get the score with the forecasted move    
            value = min(value, self.MaxValue(forecastedGame, depth-1, alpha, beta))

            # prune the rest of the nodes (moves)
            if value <= alpha:
                return value

            # update the beta limit
            beta = min(beta, value)
                
            
        return value        
    