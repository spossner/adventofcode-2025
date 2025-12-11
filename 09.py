import os
import sys
from os.path import exists

import requests
from aoc import get_ints, Rect, Point
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
GET_INTS = True
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

def convert_data(data):
    return data

def first_part(data):
    result = 0
    for p1 in range(len(data)-1):
        for p2 in range(p1+1, len(data)):
            rect = (abs(data[p1][0]-data[p2][0])+1) * (abs(data[p1][1]-data[p2][1])+1)
            if rect > result:
                result = rect
    return result


def intersect(rect:Rect, edge: tuple[Point, Point]) -> bool:
    eb = Rect.boundary(edge[0], edge[1])
    return rect.x < eb.x2 and rect.x2 > eb.x and rect.y < eb.y2 and rect.y2 > eb.y


def second_part(data):
    result = 0

    edges: list[tuple[Point, Point]] = []
    last = data[-1]
    for next in data:
        edges.append((Point(*last), Point(*next)))
        last = next

    for i1 in range(len(data)-1):
        for i2 in range(i1+1, len(data)):
            p1, p2 = data[i1], data[i2]
            rect = Rect.boundary(p1, p2)
            area = rect.w  * rect.h
            if area <= result: # already found at least as big as rect
                continue
            if any(filter(lambda e: intersect(rect, e), edges)): # skip if intersecting with any edge
                continue
            result = area

    return result


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
    converted_data = convert_data(parsed_data)
    print("RESULT", first_part(converted_data) if not PART2 else second_part(converted_data))
