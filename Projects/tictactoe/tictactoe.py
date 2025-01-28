"""
Tic Tac Toe Player
"""

import copy
import math
import sys

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def winning_states():
    """
    Returns possible winning states
    """
    return [((0, 0),(0, 1),(0, 2)),
            ((1, 0),(1, 1),(1, 2)),
            ((2, 0),(2, 1),(2, 2)),
            ((0, 0),(1, 0),(2, 0)),
            ((0, 1),(1, 1),(2, 1)),
            ((0, 2),(1, 2),(2, 2)),
            ((0, 0),(1, 1),(2, 2)),
            ((0, 2),(1, 1),(2, 0))]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    Xcount = sum(row.count(X) for row in board)
    Ocount = sum(row.count(O) for row in board)

    if (Xcount == 0):
        return X
    if (Xcount > Ocount):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_actions = set(tuple())

    for i in range(len(board)):  # Row index
        for j in range(len(board[i])):  # Column index
            if (board[i][j] == EMPTY):
                possible_actions.add(i, j)

    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    try:
        if (board[action[0]][action[1]] != EMPTY):
            raise ValueError("Invalid move.")
        else:
            new_board[action[0]][action[1]] = player(board)
            return new_board
    except ValueError as e:
        print(f"Error: {e}. Please try again.")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner_found = None

    for i in range(len(winning_states())):  # Row index
        if (((board[(winning_states()[i][0])[0]][(winning_states()[i][0])[1]]))
            == (board[(winning_states()[i][1])[0]][(winning_states()[i][1])[1]]) and
            ((board[(winning_states()[i][1])[0]][(winning_states()[i][1])[1]]))
            == (board[(winning_states()[i][2])[0]][(winning_states()[i][2])[1]]) and
            ((board[(winning_states()[i][0])[0]][(winning_states()[i][0])[1]])) != EMPTY):
            winner_found = board[(winning_states()[i][0])[0]][(winning_states()[i][0])[1]]
            break            
            
    return winner_found


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if ((winner(board) == X) or (winner(board) == O) or len(actions(board) == 0)):
        return True
    else:
        return False
    

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if (winner(board) == X):
        return 1
    elif (winner(board) == O):
        return -1
    elif len(actions(board) == 0):
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError


def main():
    print(winner([[O, EMPTY, EMPTY],
                [EMPTY, O, EMPTY],
                [EMPTY, EMPTY, EMPTY]]))
    

if __name__ == "__main__":
    main()