import os
import sys
import math
from os.path import exists

import requests
from aoc import get_ints, Grid
from dotenv import load_dotenv

load_dotenv()

# select one of
# DEV, PART2 = True, False  # DEV PART1
# DEV, PART2 = False, False # PROD PART1
# DEV, PART2 = True, True # DEV PART2
DEV, PART2 = False, True # PROD PART2

STRIP = True
SPLIT_LINES = True
SPLIT_CHAR = None
GET_INTS = False
DATA = None
AOC_SESSION = os.environ.get("AOC_SESSION")
YEAR = 2025


class Solution:
    def __init__(self, data):
        if data and STRIP and type(data) is str:
            data = data.strip()
        if data and SPLIT_LINES and type(data) is str:
            data = data.splitlines()
        if data and SPLIT_CHAR is not None:
            if SPLIT_CHAR == "":
                data = [list(row) for row in data] if SPLIT_LINES else list(data)
            else:
                data = (
                    [row.split(SPLIT_CHAR) for row in data]
                    if SPLIT_LINES
                    else data.split(SPLIT_CHAR)
                )
        if GET_INTS:
            if type(data) is str:
                data = get_ints(data)
            else:
                data = list(
                    map(
                        lambda e: get_ints(e)
                        if type(e) is str
                        else [get_ints(v) for v in e],
                        data,
                    )
                )
        self.data = self.parse_data(data)

    def parse_data(self, data):
        if PART2:
            return data
        return list(filter(bool, map(get_ints, data))), list(filter(bool, data[-1].split(" ")))

    def first_part(self):
        problems, operators = self.data
        result = list(map(lambda op: 0 if op == "+" else 1, operators))

        for i, op in enumerate(operators):
            for row in problems:
                if op == "+":
                    result[i] += row[i]
                else:
                    result[i] *= row[i]

        return sum(result)

    def second_part(self):
        problem_starts = self.data[-1].split(" ")
        operators = list(filter(bool, problem_starts))

        problems = []
        input = list(Grid(self.data[:-1]).transpose().rows())
        problem = []
        for number in [*input,""]:
            v = number.strip()
            if v == "":
                problems.append(problem)
                problem = []
            else:
                problem.append(int(v))
        result = 0
        for op,problem in zip(operators,problems):
            if op == "+":
                result += sum(problem)
            else:
                result += math.prod(problem)
        return result


if __name__ == "__main__":
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if "-" in script:
        script = script.split("-")[0]

    DATA_URL = f"https://adventofcode.com/{YEAR}/day/{int(script)}/input"

    if not DATA:
        file_name = (
            f"{script}-dev{DEV if type(DEV) is not bool else ''}.txt"
            if DEV
            else f"{script}.txt"
        )
        if exists(file_name):
            with open(file_name) as f:
                DATA = f.read()
        elif AOC_SESSION and DATA_URL:
            DATA = requests.get(
                DATA_URL, headers={"Cookie": f"session={AOC_SESSION}"}
            ).text
            with open(file_name, "w") as f:
                f.write(DATA)

    print(f"DAY {int(script)}")
    s = Solution(DATA)
    print("RESULT", s.first_part() if not PART2 else s.second_part())
