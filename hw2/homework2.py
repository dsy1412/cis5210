############################################################
# CIS 521: Homework 2
############################################################

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math
import random
from collections import deque

############################################################

student_name = "Shengyang Dong"

############################################################
# Section 1: N-Queens
############################################################


def num_placements_all(n):
    return math.comb(n * n, n)


def num_placements_one_per_row(n):
    return n ** n


def n_queens_valid(board):
    seen_cols = set()
    seen_diag_down = set()
    seen_diag_up = set()

    for row, col in enumerate(board):
        diag_down = row - col
        diag_up = row + col
        if (col in seen_cols or diag_down in seen_diag_down
                or diag_up in seen_diag_up):
            return False
        seen_cols.add(col)
        seen_diag_down.add(diag_down)
        seen_diag_up.add(diag_up)

    return True


def n_queens_solutions(n):
    def helper(board):
        row = len(board)
        if row == n:
            yield board
            return

        for col in range(n):
            candidate = board + [col]
            if n_queens_valid(candidate):
                yield from helper(candidate)

    return list(helper([]))

############################################################
# Section 2: Lights Out
############################################################


class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0]) if self.rows else 0

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        for r, c in ((row, col), (row - 1, col), (row + 1, col),
                     (row, col - 1), (row, col + 1)):
            if 0 <= r < self.rows and 0 <= c < self.cols:
                self.board[r][c] = not self.board[r][c]

    def scramble(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if random.random() < 0.5:
                    self.perform_move(row, col)

    def is_solved(self):
        return all(not light for row in self.board for light in row)

    def copy(self):
        return LightsOutPuzzle([row[:] for row in self.board])

    def successors(self):
        for row in range(self.rows):
            for col in range(self.cols):
                puzzle = self.copy()
                puzzle.perform_move(row, col)
                yield (row, col), puzzle

    def find_solution(self):
        start = _board_to_tuple(self.board)
        if self.is_solved():
            return []

        frontier = deque([(self.copy(), [])])
        visited = {start}

        while frontier:
            puzzle, path = frontier.popleft()
            for move, successor in puzzle.successors():
                state = _board_to_tuple(successor.get_board())
                if state in visited:
                    continue
                new_path = path + [move]
                if successor.is_solved():
                    return new_path
                visited.add(state)
                frontier.append((successor, new_path))

        return None


def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False for _ in range(cols)]
                            for _ in range(rows)])

############################################################
# Section 3: Linear Disk Movement
############################################################


def solve_identical_disks(length, n):
    start = tuple([1] * n + [0] * (length - n))
    goal = tuple([0] * (length - n) + [1] * n)
    return _solve_disk_puzzle(start, goal, distinct=False)


def solve_distinct_disks(length, n):
    start = tuple(range(n)) + tuple([-1] * (length - n))
    goal = tuple([-1] * (length - n)) + tuple(reversed(range(n)))
    return _solve_disk_puzzle(start, goal, distinct=True)


def _board_to_tuple(board):
    return tuple(tuple(row) for row in board)


def _solve_disk_puzzle(start, goal, distinct):
    if start == goal:
        return []

    frontier = deque([(start, [])])
    visited = {start}

    while frontier:
        state, path = frontier.popleft()
        for move, next_state in _disk_successors(state, distinct):
            if next_state in visited:
                continue
            next_path = path + [move]
            if next_state == goal:
                return next_path
            visited.add(next_state)
            frontier.append((next_state, next_path))

    return None


def _disk_successors(state, distinct):
    empty = -1 if distinct else 0
    for index, disk in enumerate(state):
        if disk == empty:
            continue
        for step in (1, -1, 2, -2):
            target = index + step
            if not 0 <= target < len(state):
                continue
            if state[target] != empty:
                continue
            if abs(step) == 2 and state[index + step // 2] == empty:
                continue
            next_state = list(state)
            next_state[index], next_state[target] = empty, disk
            yield (index, target), tuple(next_state)

############################################################
# Section 4: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
Approximately 6 hours.
"""

feedback_question_2 = """
The most challenging part was keeping the search state representation separate
from the mutable puzzle objects. Lights Out required careful duplicate-state
checking, and the disk puzzles required making sure the BFS moves were legal
in both directions while still returning a shortest solution.
"""

feedback_question_3 = """
I liked that the assignment connected the lecture ideas about search directly
to concrete puzzles. It made the role of the frontier, explored set, and state
representation much clearer. I would have liked a few more optional tests for
edge cases, especially for the disk movement puzzles.
"""
