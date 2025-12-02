import os
import sys
from os.path import exists

import requests
from aoc import get_ints
from dotenv import load_dotenv

load_dotenv()

# select one of
# DEV, PART2 = True, False  # DEV PART1
# DEV, PART2 = False, False # PROD PART1
# DEV, PART2 = True, True # DEV PART2
DEV, PART2 = False, True # PROD PART2

STRIP = True
SPLIT_LINES = False
SPLIT_CHAR = ","
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
        return data

    def first_part(self):
        result = 0
        for row in self.data:
            lower_str, upper_str = row.split("-")
            lower, upper = int(lower_str), int(upper_str)
            print(f"checking {lower}-{upper}")

            for i in range(1, upper):
                target_str=f"{i}" * 2
                target = int(target_str)
                if target > upper:
                    break
                if target >= lower:
                    # print(f"{lower}-{upper}\tcontains\t{target_str}")
                    result += target

        return result
    # 15873079070 too low - missed the [2-17]
    # 15873079081

    def second_part(self):
        result = 0
        for row in self.data:
            lower_str, upper_str = row.split("-")
            lower, upper = int(lower_str), int(upper_str)
            seen = set()
            # print(f"checking {lower}-{upper}")

            for i in range(1, (upper >> 1) * 10):
                min_pair = int(f"{i}{i}")
                if min_pair > upper:
                    break

                for j in range(2,upper):
                    target_str = f"{i}" * j
                    target = int(target_str)
                    if target > upper:
                        break
                    if target in seen:
                        continue
                    seen.add(target)
                    if target >= lower:
                        # print(f"{lower}-{upper}\tcontains\t{target_str}")
                        result += target

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
