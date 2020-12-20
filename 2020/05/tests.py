import unittest

from boarding_pass import decode_boarding_pass

boarding_passes = [
    ("FBFBBFFRLR", (44, 5, 357)),
    ("BFFFBBFRRR", (70, 7, 567)),
    ("FFFBBBFRRR", (14, 7, 119)),
    ("BBFFBBFRLL", (102, 4, 820)),
]


class BoardingTests(unittest.TestCase):
    def test_decoder(self):
        for boarding_pass, result in boarding_passes:
            print(decode_boarding_pass(boarding_pass), result)
            self.assertEqual(decode_boarding_pass(boarding_pass), result)


if __name__ == "__main__":
    unittest.main()
