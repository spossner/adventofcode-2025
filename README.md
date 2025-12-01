# Advent of code 2025

Again.. this year hust 12 puzzles.. at least state now

## PRE-CONFIGURATION
- update `YEAR` in `_.py`
- init project with uv
```
uv init
```

## 3rd party libs
Add the following dependencies
```
uv add python-dotenv requests 
```

If you want to use a local implementation of the aoc-lib library (heavily recommended) please clone aoc-lib in some folder
and make that folder available in your dependencies - .e.g.
```
...
dependencies = [
    "aoc-lib @ file:///Users/sebastian.possner/workspace/playground/advent-of-code/aoc-lib",
    ...
]
```

## Code linting & formatting
Feel free to use things like `ruff` for code formatting.
To install `ruff` just add it as (dev) dependency and afterwards call `uv run ruff check --fix`.
In `pyproject.toml` add this section
```
[dependency-groups]
dev = [
  "ruff>=0.8.0"
]
```

## New day

Clone the `_.py` blueprint and the `_-dev.txt` for every new day
and name them e.g. `01.py` and `01-dev.txt`

## Puzzle input

Puzzle input is automatically fetched when the valid AOC cookie is specified in `.env` file. 
Note that the script must be named with the number of the day - e.g. 7.py or 07.py for day 7.
Therefore

- clone the `.env.sample` into `.env`
- log into https://adventofcode.com with your browser
- search for `session` cookie
- copy & paste the value into .env file

## aoc-lib

aoc-lib (https://github.com/spossner/aoc-lib) is my own library with some helpful classes and functions for AOC.

### LOCAL

In order to use the local installation of aoc-lib, add the local copy as uv dependency. 
Therefore add ```aoc-lib @ file://<absolute path to aoc-lib>``` as uv dependency
```
...
dependencies = [
    "aoc-lib @ file:///Users/sebastian.possner/workspace/playground/advent-of-code/aoc-lib",
    ...
]
```

## Git
Note that the puzzle input data is ignored and not pushed into git.