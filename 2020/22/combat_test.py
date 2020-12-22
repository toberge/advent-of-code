import unittest

from combat import combat, recursive_combat, score


class CombatTest(unittest.TestCase):
    def test_score(self):
        self.assertEqual(score([3, 2, 10, 6, 8, 5, 9, 4, 7, 1]), 306)
        self.assertEqual(score([7, 5, 6, 2, 4, 1, 10, 8, 9, 3]), 291)

    def test_game(self):
        self.assertEqual(combat([9, 2, 6, 3, 1], [5, 8, 4, 7, 10]), 306)

    def test_recursive_game(self):
        winner, score_ = recursive_combat([9, 2, 6, 3, 1], [5, 8, 4, 7, 10])
        self.assertEqual(score_, 291)
        self.assertEqual(winner, 2)


if __name__ == "__main__":
    unittest.main()
