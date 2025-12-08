import os
import sys
from os.path import exists

import requests
from aoc import get_ints, Point3d, distance
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
    return list(map(lambda d: Point3d(d[0],d[1],d[2]), data))

def first_part(data):
    distances = []
    for i1 in range(len(data) - 1):
        p1 = data[i1]
        for i2 in range(i1 + 1, len(data)):
            p2 = data[i2]
            dist = distance(p1, p2)
            distances.append((dist, p1, p2))

    distances.sort(key=lambda p: p[0])

    circuits = {}
    count = len(data)

    for step in range(len(distances) if PART2 else 10 if DEV else 1000):
        d,p1,p2 = distances[step]
        if p1 in circuits and p2 in circuits:
            if circuits[p1] == circuits[p2]:
                continue
            merged_circuit = circuits[p1] + circuits[p2]
            for p in merged_circuit:
                circuits[p] = merged_circuit
        elif p1 in circuits:
            circuits[p1].append(p2)
            circuits[p2] = circuits[p1]
        elif p2 in circuits:
            circuits[p2].append(p1)
            circuits[p1] = circuits[p2]
        else:
            circuit = [p1,p2]
            circuits[p1] = circuits[p2] = circuit
        if PART2 and count == 2:
            return p1[0] * p2[0]
        count -= 1

    overview = set()
    for p, circuit in circuits.items():
        overview.add(tuple(circuit))

    sorted_circuits = sorted(list(overview), key=lambda c: len(c), reverse=True)
    result = 1
    for i in range(3):
        result *= len(sorted_circuits[i])

    return result

def second_part(data):
    return first_part(data)

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
