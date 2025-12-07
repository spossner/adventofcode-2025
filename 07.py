import os
import sys
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
SPLIT_CHAR = ""
GET_INTS = False
DATA_OVERWRITE = None
AOC_SESSION = os.environ.get("AOC_SESSION")
YEAR = 2025


def parse_data(puzzle_input):
    if puzzle_input and STRIP and type(puzzle_input) is str:
        puzzle_input = puzzle_input.strip()
    if puzzle_input and SPLIT_LINES and type(puzzle_input) is str:
        puzzle_input = puzzle_input.splitlines()
    if puzzle_input and SPLIT_CHAR is not None:
        if SPLIT_CHAR == "":
            puzzle_input = [list(row) for row in puzzle_input] if SPLIT_LINES else list(puzzle_input)
        else:
            puzzle_input = (
                [row.split(SPLIT_CHAR) for row in puzzle_input]
                if SPLIT_LINES
                else puzzle_input.split(SPLIT_CHAR)
            )
    if GET_INTS:
        if type(puzzle_input) is str:
            puzzle_input = get_ints(puzzle_input)
        else:
            puzzle_input = list(
                map(
                    lambda e: get_ints(e)
                    if type(e) is str
                    else [get_ints(v) for v in e],
                    puzzle_input,
                )
            )
    return puzzle_input

def first_part(data: list[list[str]]):
    result = 0

    height, width = len(data), len(data[0])

    start = data[0].index("S")
    beams = {start,}

    for row in data[1:]:
        new_beams = set()
        for beam in beams:
            if row[beam] == ".":
                new_beams.add(beam)
            else:
                result += 1
                if beam > 0:
                    new_beams.add(beam - 1)
                if beam < width:
                    new_beams.add(beam + 1)
        beams = new_beams


    return result

def second_part(data):
    height, width = len(data), len(data[0])
    start = data[0].index("S")

    ways = [[1] * width for _ in range(height)]
    for y in range(height-2,-1,-1):
        for x in range(width):
            if data[y][x] == ".":
                ways[y][x] = ways[y+1][x]
            else: # simplified: no splitter in first and last column and also not in last row
                ways[y][x] = ways[y+1][x-1] + ways[y+1][x+1]
    return ways[0][start]

if __name__ == "__main__":
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if "-" in script:
        script = script.split("-")[0]

    DATA_URL = f"https://adventofcode.com/{YEAR}/day/{int(script)}/input"

    data = DATA_OVERWRITE
    if not data:
        file_name = (
            f"{script}-dev{DEV if type(DEV) is not bool else ''}.txt"
            if DEV
            else f"{script}.txt"
        )
        if exists(file_name):
            with open(file_name) as f:
                data = f.read()
        elif AOC_SESSION and DATA_URL:
            data = requests.get(
                DATA_URL, headers={"Cookie": f"session={AOC_SESSION}"}
            ).text
            with open(file_name, "w") as f:
                f.write(data)

    print(f"DAY {int(script)}")
    parsed_data = parse_data(data)
    print("RESULT", first_part(parsed_data) if not PART2 else second_part(parsed_data))
