"""
Day VIII: Finally some computations!
"""

import sys


def parse_instructions(lines: [str]):
    """Split and intify line"""
    return [(line.split()[0], int(line.split()[1].replace("+", ""))) for line in lines]


def permutations(instructions: [(str, int)]):
    """Essentially flipping a trinary digit each time there's a -1 or 1"""
    for i, instruction in enumerate(instructions):
        cmd, count = instruction
        if cmd != "jmp" and cmd != "nop":
            continue
        test = instructions[:]
        test[i] = ("jmp" if cmd == "nop" else "nop", count)
        yield test


def bruteforce_corrupt_instruction(instructions):
    """Part two - what instruction needed changing, and what is the result?"""
    for test in permutations(instructions):
        result = Handheld(test).detect_loop_or_completion()
        if result is not None:
            return result.acc
    return None


class Handheld:
    """Handheld game console as per Day 8's requirements"""

    def __init__(self, instructions, initial_acc=0):
        self.instr = instructions[:]
        self.performed_instr = set()
        self.num_instr = len(self.instr)
        self.acc = initial_acc
        self.instr_ptr = 0

    def _eval(self, instruction):
        cmd, arg = instruction
        if cmd == "nop":
            self.instr_ptr += 1
        elif cmd == "acc":
            self.instr_ptr += 1
            self.acc += arg
        elif cmd == "jmp":
            self.instr_ptr += arg

    def detect_loop(self):
        """Part one - detect loop"""
        while self.instr_ptr not in self.performed_instr:
            self.performed_instr.add(self.instr_ptr)
            self._eval(self.instr[self.instr_ptr])
        return self

    def detect_loop_or_completion(self):
        """Part two - will this loop or end?"""
        while self.instr_ptr < self.num_instr:
            if self.instr_ptr in self.performed_instr:
                return None  # loop
            self.performed_instr.add(self.instr_ptr)
            self._eval(self.instr[self.instr_ptr])
        return self  # termination

    def run(self):
        """Terminates when a non-existent instruction is executed"""
        while self.instr_ptr < self.num_instr:
            self.performed_instr.add(self.instr_ptr)
            self._eval(self.instr[self.instr_ptr])
        return self

    def run_until(self, condition):
        """Runs until a condition is reached (for a misunderstood part one)"""
        while not condition(self):
            if self.instr_ptr in self.performed_instr:
                return self
            self.performed_instr.add(self.instr_ptr)
            self._eval(self.instr[self.instr_ptr])
        return self


if __name__ == "__main__":
    instruction_set = parse_instructions(sys.stdin.readlines())
    # print(handheld.run_until(lambda h: h.acc == 5).acc)
    print(Handheld(instruction_set).detect_loop().acc)
    print(bruteforce_corrupt_instruction(instruction_set))
