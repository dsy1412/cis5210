############################################################
# CIS 521: Homework 3
############################################################

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import heapq
import itertools
import math
import random

############################################################

student_name = "Shengyang Dong"

############################################################
# Section 1: Tile Puzzle
############################################################


def create_tile_puzzle(rows, cols):
    board = []
    tile = 1
    for row in range(rows):
        board.append([])
        for col in range(cols):
            if row == rows - 1 and col == cols - 1:
                board[row].append(0)
            else:
                board[row].append(tile)
                tile += 1
    return TilePuzzle(board)


class TilePuzzle(object):

    # Required
    def __init__(self, board):
        self.board = [row[:] for row in board]
        self.rows = len(board)
        self.cols = len(board[0]) if self.rows else 0
        self.empty = self._find_empty()

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        moves = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
        }
        if direction not in moves:
            return False

        row, col = self.empty
        d_row, d_col = moves[direction]
        new_row, new_col = row + d_row, col + d_col
        if not (0 <= new_row < self.rows and 0 <= new_col < self.cols):
            return False

        self.board[row][col], self.board[new_row][new_col] = (
            self.board[new_row][new_col], self.board[row][col])
        self.empty = (new_row, new_col)
        return True

    def scramble(self, num_moves):
        for _ in range(num_moves):
            self.perform_move(random.choice(["up", "down", "left", "right"]))

    def is_solved(self):
        return _board_to_tuple(self.board) == _solved_tile_state(
            self.rows, self.cols)

    def copy(self):
        return TilePuzzle([row[:] for row in self.board])

    def successors(self):
        for direction in ("up", "down", "left", "right"):
            puzzle = self.copy()
            if puzzle.perform_move(direction):
                yield direction, puzzle

    # Required
    def find_solutions_iddfs(self):
        depth = 0
        while True:
            found_solution = False
            start = _board_to_tuple(self.board)
            for solution in self._iddfs_helper(depth, [], {start}):
                found_solution = True
                yield solution
            if found_solution:
                return
            depth += 1

    # Required
    def find_solution_a_star(self):
        start = _board_to_tuple(self.board)
        goal = _solved_tile_state(self.rows, self.cols)
        if start == goal:
            return []

        counter = itertools.count()
        frontier = []
        start_h = _tile_manhattan(start, self.rows, self.cols)
        heapq.heappush(frontier, (start_h, 0, next(counter), start, []))
        best_cost = {start: 0}

        while frontier:
            _, cost, _, state, path = heapq.heappop(frontier)
            if state == goal:
                return path
            if cost != best_cost[state]:
                continue

            for move, next_state in _tile_successor_states(
                    state, self.rows, self.cols):
                next_cost = cost + 1
                if (next_state not in best_cost
                        or next_cost < best_cost[next_state]):
                    best_cost[next_state] = next_cost
                    priority = (next_cost
                                + _tile_manhattan(
                                    next_state, self.rows, self.cols))
                    heapq.heappush(
                        frontier,
                        (priority, next_cost, next(counter),
                         next_state, path + [move]))

        return None

    def _find_empty(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == 0:
                    return row, col
        return None

    def _iddfs_helper(self, limit, moves, visited):
        if self.is_solved():
            yield moves
            return
        if limit == 0:
            return

        for move, successor in self.successors():
            state = _board_to_tuple(successor.get_board())
            if state in visited:
                continue
            visited.add(state)
            yield from successor._iddfs_helper(
                limit - 1, moves + [move], visited)
            visited.remove(state)

############################################################
# Section 2: Grid Navigation
############################################################


def find_path(start, goal, scene):
    rows = len(scene)
    cols = len(scene[0]) if rows else 0
    if not (_valid_grid_point(start, rows, cols)
            and _valid_grid_point(goal, rows, cols)):
        return None
    if scene[start[0]][start[1]] or scene[goal[0]][goal[1]]:
        return None
    if start == goal:
        return [start]

    counter = itertools.count()
    frontier = []
    start_h = _euclidean(start, goal)
    heapq.heappush(frontier, (start_h, 0.0, next(counter), start, [start]))
    best_cost = {start: 0.0}

    while frontier:
        _, cost, _, point, path = heapq.heappop(frontier)
        if point == goal:
            return path
        if cost != best_cost[point]:
            continue

        for neighbor, step_cost in _grid_successors(point, scene):
            next_cost = cost + step_cost
            if (neighbor not in best_cost
                    or next_cost < best_cost[neighbor]):
                best_cost[neighbor] = next_cost
                priority = next_cost + _euclidean(neighbor, goal)
                heapq.heappush(
                    frontier,
                    (priority, next_cost, next(counter),
                     neighbor, path + [neighbor]))

    return None

############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################


def solve_distinct_disks(length, n):
    start = tuple(range(n)) + tuple([-1] * (length - n))
    goal = tuple([-1] * (length - n)) + tuple(reversed(range(n)))
    if start == goal:
        return []

    counter = itertools.count()
    frontier = []
    start_h = _distinct_disk_heuristic(start, length, n)
    heapq.heappush(frontier, (start_h, 0, next(counter), start, []))
    best_cost = {start: 0}

    while frontier:
        _, cost, _, state, path = heapq.heappop(frontier)
        if state == goal:
            return path
        if cost != best_cost[state]:
            continue

        for move, next_state in _disk_successors(state):
            next_cost = cost + 1
            if (next_state not in best_cost
                    or next_cost < best_cost[next_state]):
                best_cost[next_state] = next_cost
                priority = (next_cost
                            + _distinct_disk_heuristic(
                                next_state, length, n))
                heapq.heappush(
                    frontier,
                    (priority, next_cost, next(counter),
                     next_state, path + [move]))

    return None


def _board_to_tuple(board):
    return tuple(tuple(row) for row in board)


def _tuple_to_board(state):
    return [list(row) for row in state]


def _solved_tile_state(rows, cols):
    values = list(range(1, rows * cols)) + [0]
    return tuple(tuple(values[row * cols:(row + 1) * cols])
                 for row in range(rows))


def _empty_position(state):
    for row, row_values in enumerate(state):
        for col, value in enumerate(row_values):
            if value == 0:
                return row, col
    return None


def _tile_successor_states(state, rows, cols):
    deltas = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1),
    }
    row, col = _empty_position(state)
    for direction in ("up", "down", "left", "right"):
        d_row, d_col = deltas[direction]
        new_row, new_col = row + d_row, col + d_col
        if not (0 <= new_row < rows and 0 <= new_col < cols):
            continue
        board = _tuple_to_board(state)
        board[row][col], board[new_row][new_col] = (
            board[new_row][new_col], board[row][col])
        yield direction, _board_to_tuple(board)


def _tile_manhattan(state, rows, cols):
    distance = 0
    for row in range(rows):
        for col in range(cols):
            tile = state[row][col]
            if tile == 0:
                continue
            goal_row, goal_col = divmod(tile - 1, cols)
            distance += abs(row - goal_row) + abs(col - goal_col)
    return distance


def _valid_grid_point(point, rows, cols):
    row, col = point
    return 0 <= row < rows and 0 <= col < cols


def _euclidean(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def _grid_successors(point, scene):
    rows = len(scene)
    cols = len(scene[0]) if rows else 0
    row, col = point
    for d_row in (-1, 0, 1):
        for d_col in (-1, 0, 1):
            if d_row == 0 and d_col == 0:
                continue
            new_row, new_col = row + d_row, col + d_col
            if not (0 <= new_row < rows and 0 <= new_col < cols):
                continue
            if scene[new_row][new_col]:
                continue
            yield (new_row, new_col), math.hypot(d_row, d_col)


def _disk_successors(state):
    for index, disk in enumerate(state):
        if disk == -1:
            continue
        for step in (1, -1, 2, -2):
            target = index + step
            if not 0 <= target < len(state):
                continue
            if state[target] != -1:
                continue
            if abs(step) == 2 and state[index + step // 2] == -1:
                continue
            next_state = list(state)
            next_state[index], next_state[target] = -1, disk
            yield (index, target), tuple(next_state)


def _distinct_disk_heuristic(state, length, n):
    positions = {}
    for index, disk in enumerate(state):
        if disk != -1:
            positions[disk] = index

    distance_bound = 0
    for disk in range(n):
        goal_position = length - 1 - disk
        distance_bound += math.ceil(abs(positions[disk] - goal_position) / 2)

    order = [disk for disk in state if disk != -1]
    inversion_bound = 0
    for i in range(len(order)):
        for j in range(i + 1, len(order)):
            if order[i] < order[j]:
                inversion_bound += 1

    return max(distance_bound, inversion_bound)

############################################################
# Section 4: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
Approximately 7 hours.
"""

feedback_question_2 = """
The most challenging part was choosing state representations that worked well
with informed search. The tile puzzle and disk puzzle both have mutable-looking
states, but A* needs immutable states for priority queues and best-cost tables.
It was also important to design admissible heuristics without accidentally
overestimating the remaining cost.
"""

feedback_question_3 = """
The assignment was useful because it connected the lecture idea of heuristics
to concrete puzzles. Implementing Manhattan distance, Euclidean distance, and a
disk-movement lower bound made the difference between uninformed and informed
search much clearer. A few more small official test cases would have made the
edge cases easier to check.
"""
