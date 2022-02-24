# play-lichess

[![build](https://img.shields.io/github/workflow/status/DenverCoder1/play-lichess/Python%20application/main)](https://github.com/DenverCoder1/play-lichess/actions/workflows/python-app.yml)
[![version](https://img.shields.io/pypi/v/play-lichess)](https://pypi.org/project/play-lichess/)
[![license](https://img.shields.io/pypi/l/play-lichess)](https://github.com/DenverCoder1/play-lichess/blob/main/LICENSE)
[![Discord](https://img.shields.io/discord/819650821314052106?color=7289DA&logo=discord&logoColor=white "Dev Pro Tips Discussion & Support Server")](https://discord.gg/fPrdqh3Zfu)

Python module for creating match links on Lichess that two players can join

> Note: Until version 0.1.3, the requests were done synchronously using `requests`. Starting with version 1.0.0, all requests are done asynchronously using `aiohttp`.

## 📥 Installation

`pip install play-lichess`

## 🧑‍💻 Usage

### Start a real-time match

```py
from play_lichess import RealTimeMatch

async def create_match():
    match = await RealTimeMatch.create()

    print(match.challenge_id)       # e.g. 'f1S4BBYW'
    print(match.challenge_url)      # e.g. 'https://lichess.org/f1S4BBYW'
    print(match.status)             # 'created'
    print(match.variant)            # Variant.STANDARD
    print(match.rated)              # False
    print(match.speed)              # TimeMode.BLITZ
    print(match.time_control.show)  # '5+0'
    print(match.color)              # Color.RANDOM
    print(match.url_white)          # e.g. 'https://lichess.org/f1S4BBYW?color=white'
    print(match.url_black)          # e.g. 'https://lichess.org/f1S4BBYW?color=black'
    print(match.name)               # None

asyncio.run(create_match())  # import asyncio to call async functions outside event loop
```

### Start a correspondence match

```py
from play_lichess import CorrespondenceMatch

async def correspondence_match():
    match = await CorrespondenceMatch.create()

    print(match.challenge_id)               # e.g. 'KGO4ICDn'
    print(match.challenge_url)              # e.g. 'https://lichess.org/KGO4ICDn'
    print(match.status)                     # 'created'
    print(match.variant)                    # Variant.STANDARD
    print(match.rated)                      # False
    print(match.speed)                      # TimeMode.CORRESPONDENCE
    print(match.time_control.type)          # TimeControlType.CORRESPONDENCE
    print(match.time_control.days_per_turn) # 1
    print(match.color)                      # Color.RANDOM
    print(match.url_white)                  # e.g. 'https://lichess.org/KGO4ICDn?color=white'
    print(match.url_black)                  # e.g. 'https://lichess.org/KGO4ICDn?color=black'
    print(match.name)                       # None
```

### Start an unlimited time match

```py
from play_lichess import UnlimitedMatch

async def unlimited_correspondence_match():
    match = await UnlimitedMatch.create()

    print(match.challenge_id)       # e.g. 'JLA868mV'
    print(match.challenge_url)      # e.g. 'https://lichess.org/JLA868mV'
    print(match.status)             # 'created'
    print(match.variant)            # Variant.STANDARD
    print(match.rated)              # False
    print(match.speed)              # TimeMode.CORRESPONDENCE
    print(match.time_control.type)  # TimeControlType.UNLIMITED
    print(match.color)              # Color.RANDOM
    print(match.url_white)          # e.g. 'https://lichess.org/JLA868mV?color=white'
    print(match.url_black)          # e.g. 'https://lichess.org/JLA868mV?color=black'
    print(match.name)               # None
```

### Specify game options

```py
from play_lichess import RealTimeMatch, Variant, Color

async def create_match_options():
    match: RealTimeMatch = await RealTimeMatch.create(
        rated=False,
        clock_limit=180,
        clock_increment=0,
        variant=Variant.ANTICHESS,
        name="Test match",
    )

    print(match.challenge_id)       # e.g. 'cuZGwbcO'
    print(match.challenge_url)      # e.g. 'https://lichess.org/cuZGwbcO'
    print(match.status)             # 'created'
    print(match.variant)            # Variant.ANTICHESS
    print(match.rated)              # False
    print(match.speed)              # TimeMode.BLITZ
    print(match.time_control.show)  # '3+0'
    print(match.color)              # Color.RANDOM
    print(match.url_white)          # e.g. 'https://lichess.org/cuZGwbcO?color=white'
    print(match.url_black)          # e.g. 'https://lichess.org/cuZGwbcO?color=black'
    print(match.name)               # 'Test match'
```

### Alternate syntax

```py
from play_lichess import Match, TimeMode, Variant, Color

async def create_any_match():
    # real-time
    match1 = await Match.create(clock_limit=180, clock_increment=0)
    # unlimited time
    match2 = await Match.create(clock_limit=None, clock_increment=None)
    # correspondence
    match3 = await Match.create(days=1, clock_limit=None, clock_increment=None)
```

## 🔧 Options

### Real-time

| Argument          | Type      | Default        | Description                                         |
| ----------------- | --------- | -------------- | --------------------------------------------------- |
| `rated`           | `bool`    | `False`        | Whether the match is rated or not.                  |
| `clock_limit`     | `int`     | `300`          | The time limit in seconds.                          |
| `clock_increment` | `int`     | `0`            | The time increment in seconds.                      |
| `variant`         | `Variant` | `STANDARD`     | The variant of the match (STANDARD, CHESS960, etc.) |
| `fen`             | `str`     | Start position | The FEN string of the starting position.            |
| `name`            | `str`     | `None`         | The name of the match displayed when joining.       |

### Correspondence

| Argument  | Type      | Default        | Description                                         |
| --------- | --------- | -------------- | --------------------------------------------------- |
| `rated`   | `bool`    | `False`        | Whether the match is rated or not.                  |
| `days`    | `int`     | `1`            | The number of days for each player.                 |
| `variant` | `Variant` | `STANDARD`     | The variant of the match (STANDARD, CHESS960, etc.) |
| `fen`     | `str`     | Start position | The FEN string of the starting position.            |
| `name`    | `str`     | `None`         | The name of the match displayed when joining.       |

### Unlimited

| Argument  | Type      | Default        | Description                                         |
| --------- | --------- | -------------- | --------------------------------------------------- |
| `variant` | `Variant` | `STANDARD`     | The variant of the match (STANDARD, CHESS960, etc.) |
| `color`   | `Color`   | `RANDOM`       | The color assigned to the first player that joins   |
| `fen`     | `str`     | Start position | The FEN string of the starting position.            |
| `name`    | `str`     | `None`         | The name of the match displayed when joining.       |

## 🧰 Development

### To run tests (pytest/tox)

```bash
# Install tox
pip install -U tox

# Run tests
tox
```

### To lint (flake8)

```bash
# Install flake8
pip install flake8==3.8.4

# Run linter
python setup.py lint
```
