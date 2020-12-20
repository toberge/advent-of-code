"""
Day V: Binary Boarding
"""

import sys

from boarding_pass import decode_boarding_pass

if __name__ == "__main__":
    print(max(id_ for _, _, id_ in map(decode_boarding_pass, sys.stdin.readlines())))
