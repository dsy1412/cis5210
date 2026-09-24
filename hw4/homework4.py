############################################################
# CIS 521: Homework 4
############################################################

############################################################
# Imports
############################################################

import math
import random

############################################################

student_name = "Shengyang Dong"

############################################################
# Section 1: Dominoes Game
############################################################


def create_dominoes_game(rows, cols):
    return DominoesGame([[False] * cols for _ in range(rows)])


class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0]) if board else 0

    def get_board(self):
        return self.board

    def reset(self):
        for row in self.board:
            for col in range(len(row)):
                row[col] = False

    def is_legal_move(self, row, col, vertical):
        next_row = row + (1 if vertical else 0)
        next_col = col + (0 if vertical else 1)
        return (0 <= row < self.rows and 0 <= col < self.cols
                and next_row < self.rows and next_col < self.cols
                and not self.board[row][col]
                and not self.board[next_row][next_col])

    def legal_moves(self, vertical):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_legal_move(row, col, vertical):
                    yield (row, col)

    def perform_move(self, row, col, vertical):
        self.board[row][col] = True
        self.board[row + (1 if vertical else 0)][
            col + (0 if vertical else 1)] = True

    def game_over(self, vertical):
        return next(self.legal_moves(vertical), None) is None

    def copy(self):
        return DominoesGame([row[:] for row in self.board])

    def successors(self, vertical):
        for move in self.legal_moves(vertical):
            successor = self.copy()
            successor.perform_move(*move, vertical)
            yield (move, successor)

    def get_random_move(self, vertical):
        return random.choice(list(self.legal_moves(vertical)))

    # Required
    def get_best_move(self, vertical, limit):
        def evaluate(game):
            own_moves = sum(1 for _ in game.legal_moves(vertical))
            opponent_moves = sum(1 for _ in game.legal_moves(not vertical))
            return own_moves - opponent_moves

        def search(game, turn, depth, alpha, beta):
            if depth == 0:
                return evaluate(game), 1

            moves = list(game.legal_moves(turn))
            if not moves:
                return evaluate(game), 1

            maximizing = turn == vertical
            value = -math.inf if maximizing else math.inf
            leaves = 0
            for move in moves:
                child = game.copy()
                child.perform_move(*move, turn)
                child_value, child_leaves = search(
                    child, not turn, depth - 1, alpha, beta)
                leaves += child_leaves
                if maximizing:
                    value = max(value, child_value)
                    alpha = max(alpha, value)
                else:
                    value = min(value, child_value)
                    beta = min(beta, value)
                if alpha >= beta:
                    break
            return value, leaves

        moves = list(self.legal_moves(vertical))
        if limit <= 0 or not moves:
            return (None, evaluate(self), 1)

        best_move = None
        best_value = -math.inf
        leaves = 0
        alpha = -math.inf
        for move in moves:
            child = self.copy()
            child.perform_move(*move, vertical)
            value, child_leaves = search(
                child, not vertical, limit - 1, alpha, math.inf)
            leaves += child_leaves
            if value > best_value:
                best_move, best_value = move, value
            alpha = max(alpha, best_value)
        return (best_move, best_value, leaves)

############################################################
# Section 2: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
Approximately 5 hours.
"""

feedback_question_2 = """
Keeping the evaluation relative to the original player while alternating MAX
and MIN turns, especially when counting only the leaves actually evaluated.
"""

feedback_question_3 = """
The small game makes alpha-beta pruning easy to inspect. A worked search tree
alongside the GUI would make the move ordering and cutoffs easier to study.
"""
