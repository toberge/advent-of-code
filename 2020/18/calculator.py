"""
Day 18: Operation Order

123 millis for part two _and_ one

Time to implement: Less than an hour
"""
import sys

OPERATORS = {"+": lambda a, b: a + b, "*": lambda a, b: a * b}

PRECEDENCE = {"+": 2, "*": 1}  # for "advanced" math


def shunting_yard(expression: str, dont_care=False) -> []:
    """Use a simplified Shunting-Yard algorithm to transform infix to RPN notation"""
    output = []
    stack = []

    for token in expression:
        if token.isdigit():
            output.append(int(token))  # only one-digit numbers!
        elif token in OPERATORS:
            while (
                len(stack) > 0
                and stack[-1] != "("
                and (dont_care or PRECEDENCE[stack[-1]] > PRECEDENCE[token])
            ):
                output.append(stack.pop())
            stack.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":  # time to evaluate parenthesis
            while stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()  # discard the (

    while len(stack) > 0:
        output.append(stack.pop())
    return output


def rpn(expression: []) -> int:
    """Evaluate RPN (Reverse Polish Notation, postorder)"""
    nums = []

    for token in expression:
        if token in OPERATORS:
            nums.append(OPERATORS[token](nums.pop(), nums.pop()))
        else:
            nums.append(token)

    return nums.pop()


def evaluate_simple(expression: str) -> int:
    """Evaluate an expression without caring for precedence"""
    return rpn(shunting_yard(expression, dont_care=True))


def evaluate_advanced(expression: str) -> int:
    """Evaluate an expression with the opposite of normal precedence"""
    return rpn(shunting_yard(expression))


def main():
    """Main function, nothing to see here"""
    lines = sys.stdin.readlines()
    print(sum(evaluate_simple(line.rstrip()) for line in lines))
    print(sum(evaluate_advanced(line.rstrip()) for line in lines))


if __name__ == "__main__":
    main()
