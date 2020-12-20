"""
Part Two - Stricter requirements

Note to self: re.match matches from the beginning of the line
              and *ignores* anything beyond the match.
              That was *not* the behavior I was looking for.
"""
import re
import sys

from common import read_passports

MANDATORY_FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
EYE_COLORS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def is_height(height):
    if not re.match(r"\d+(cm|in)$", height):
        return False
    if height.endswith("in"):
        return 59 <= int(height[:-2]) <= 76
    if height.endswith("cm"):
        return 150 <= int(height[:-2]) <= 193


def is_year_within(year, low, high):
    return re.match(r"\d{4}$", year) and low <= int(year) <= high


is_hair_color = lambda color: re.match(r"#[0-9a-f]{6}$", color)
is_eye_color = lambda color: color in EYE_COLORS
is_pid = lambda pid: re.match(r"[0-9]{9}$", pid)


def is_valid(passport: {}) -> bool:
    for field in MANDATORY_FIELDS:
        if passport.get(field) is None:
            return False

    return all(
        [
            is_year_within(passport["byr"], 1920, 2002),
            is_year_within(passport["iyr"], 2010, 2020),
            is_year_within(passport["eyr"], 2020, 2030),
            is_height(passport["hgt"]),
            is_hair_color(passport["hcl"]),
            is_eye_color(passport["ecl"]),
            is_pid(passport["pid"]),
        ]
    )


if __name__ == "__main__":
    print(sum(map(int, map(is_valid, read_passports(sys.stdin)))))
