import unittest

from homework4 import DominoesGame, create_dominoes_game


def exhaustive_value(game, root_player, turn, depth):
    moves = list(game.legal_moves(turn))
    if depth == 0 or not moves:
        return (len(list(game.legal_moves(root_player)))
                - len(list(game.legal_moves(not root_player))))

    values = []
    for move, child in game.successors(turn):
        values.append(exhaustive_value(
            child, root_player, not turn, depth - 1))
    return max(values) if turn == root_player else min(values)


class DominoesGameTests(unittest.TestCase):
    def test_board_operations_and_copy(self):
        game = create_dominoes_game(3, 3)
        self.assertEqual(
            list(game.legal_moves(True)),
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)])
        self.assertEqual(
            list(game.legal_moves(False)),
            [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)])
        self.assertFalse(game.is_legal_move(-1, 0, True))
        self.assertFalse(game.is_legal_move(2, 0, True))
        self.assertFalse(game.is_legal_move(0, 2, False))

        copied = game.copy()
        game.perform_move(0, 1, True)
        self.assertEqual(copied.get_board(), [[False] * 3 for _ in range(3)])
        self.assertFalse(game.is_legal_move(0, 1, False))
        game.reset()
        self.assertEqual(game.get_board(), copied.get_board())

    def test_successors_do_not_mutate_parent(self):
        game = create_dominoes_game(2, 2)
        successors = list(game.successors(True))
        self.assertEqual([move for move, _ in successors], [(0, 0), (0, 1)])
        self.assertEqual(game.get_board(), [[False, False], [False, False]])
        self.assertNotEqual(
            successors[0][1].get_board(), successors[1][1].get_board())

    def test_official_search_examples(self):
        game = create_dominoes_game(3, 3)
        self.assertEqual(game.get_best_move(True, 1), ((0, 1), 2, 6))
        self.assertEqual(game.get_best_move(True, 2), ((0, 1), 3, 10))
        game.perform_move(0, 1, True)
        self.assertEqual(game.get_best_move(False, 1), ((2, 0), -3, 2))
        self.assertEqual(game.get_best_move(False, 2), ((2, 0), -2, 5))

    def test_values_match_exhaustive_minimax(self):
        for mask in (0, 1, 16, 73, 341):
            board = [[bool(mask & (1 << (row * 3 + col)))
                      for col in range(3)] for row in range(3)]
            game = DominoesGame(board)
            for player in (True, False):
                for depth in (1, 2, 3):
                    move, value, leaves = game.get_best_move(player, depth)
                    self.assertEqual(
                        value, exhaustive_value(game, player, player, depth))
                    self.assertGreaterEqual(leaves, 1)
                    if move is not None:
                        self.assertTrue(game.is_legal_move(*move, player))

    def test_terminal_board(self):
        game = DominoesGame([[True, False], [True, False]])
        self.assertTrue(game.game_over(False))
        self.assertFalse(game.game_over(True))
        self.assertEqual(game.get_best_move(False, 2), (None, -1, 1))


if __name__ == "__main__":
    unittest.main()
