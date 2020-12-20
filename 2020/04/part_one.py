import sys

from common import read_passports

MANDATORY_FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]


def is_valid(passport: {}) -> bool:
    for field in MANDATORY_FIELDS:
        if passport.get(field) is None:
            return False
    return True


if __name__ == "__main__":
    print(sum(map(int, map(is_valid, read_passports(sys.stdin)))))
