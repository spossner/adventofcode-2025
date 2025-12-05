import os
import sys
from os.path import exists

import requests
from aoc import get_ints, Interval
from dotenv import load_dotenv

load_dotenv()

# select one of
# DEV, PART2 = True, False  # DEV PART1
# DEV, PART2 = False, False # PROD PART1
# DEV, PART2 = True, True # DEV PART2
DEV, PART2 = False, True # PROD PART2

STRIP = True
SPLIT_LINES = True
SPLIT_CHAR = "-"
GET_INTS = True
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
        ranges = []
        ids = []
        for row in data:
            if len(row[0]) == 0:
                continue
            elif len(row) == 1:
                ids.append(row[0][0])
            else:
                ranges.append(Interval(row[0][0], row[1][0]))
        return (ranges, ids)

    def first_part(self):
        result = 0
        ranges, ids = self.data

        for id in ids:
            for interval in ranges:
                if id in interval:
                    result += 1
                    break

        return result

    def second_part(self):
        ranges, _ = self.data
        sorted_ranges = sorted(ranges, key=lambda interval: interval.start)

        union_ranges = [sorted_ranges[0]]
        for i in range (1,len(sorted_ranges)):
            union_interval = union_ranges[-1].union(sorted_ranges[i])
            if union_interval is None:
                union_ranges.append(sorted_ranges[i])
            else:
                union_ranges[-1] = union_interval
        return sum(map(len, union_ranges))


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
