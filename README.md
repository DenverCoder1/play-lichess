# play-lichess

[![build](https://img.shields.io/github/workflow/status/DenverCoder1/play-lichess/Python%20application/main)](https://github.com/DenverCoder1/play-lichess/actions/workflows/python-app.yml)
[![version](https://img.shields.io/pypi/v/play-lichess)](https://pypi.org/project/play-lichess/)
[![license](https://img.shields.io/pypi/l/play-lichess)](https://github.com/DenverCoder1/play-lichess/blob/main/LICENSE)
[![Discord](https://img.shields.io/discord/819650821314052106?color=7289DA&logo=discord&logoColor=white "Dev Pro Tips Discussion & Support Server")](https://discord.gg/fPrdqh3Zfu)

Python module for creating match links on Lichess that two players can join

- [play-lichess](#play-lichess)
  - [📥 Installation](#-installation)
  - [🧑‍💻 Usage](#-usage)
    - [Start a real-time match](#start-a-real-time-match)
    - [Start a correspondence match](#start-a-correspondence-match)
    - [Start an unlimited time match](#start-an-unlimited-time-match)
    - [Specify game options](#specify-game-options)
    - [Alternate syntax](#alternate-syntax)
  - [🔧 Options](#-options)
    - [Real-time](#real-time)
    - [Correspondence](#correspondence)
    - [Unlimited](#unlimited)
  - [🧰 Development](#-development)


## 📥 Installation

``pip install play-lichess``


## 🧑‍💻 Usage

### Start a real-time match

```py
import play_lichess

match = play_lichess.real_time()

print(match.link)  # eg. https://lichess.org/8KbWoJyU
print(match.title)  # Rapid (5+8) casual Chess • Open challenge • lichess.org
print(match.variant)  # Standard
print(match.color)  # Random
print(match.time_mode)  # Real-time
```

### Start a correspondence match

```py
import play_lichess

match = play_lichess.correspondence()

print(match.link)  # eg. https://lichess.org/8KbWoJyU
print(match.title)  # Correspondence casual Chess • Open challenge • lichess.org
print(match.variant)  # Standard
print(match.color)  # Random
print(match.time_mode)  # Correspondence
```

### Start an unlimited time match

```py
import play_lichess

match = play_lichess.unlimited()

print(match.link)  # eg. https://lichess.org/8KbWoJyU
print(match.title)  # Correspondence casual Chess • Open challenge • lichess.org
print(match.variant)  # Standard
print(match.color)  # Random
print(match.time_mode)  # Unlimited
```

### Specify game options

```py
import play_lichess
from play_lichess.constants import Variant, Color

match = play_lichess.real_time(
    minutes=6, 
    increment=0, 
    variant=Variant.ANTICHESS, 
    color=Color.WHITE
)

print(match.link)  # eg. https://lichess.org/8KbWoJyU
print(match.title)  # Blitz (6+0) casual Chess • Open challenge • lichess.org
print(match.variant)  # Antichess
print(match.color)  # White
print(match.time_mode)  # Real-time
```

### Alternate syntax

```py
import play_lichess
from play_lichess.constants import TimeMode, Variant, Color

match1 = play_lichess.create(time_mode=TimeMode.REALTIME, minutes=6, increment=0)

match2 = play_lichess.create(time_mode=TimeMode.CORRESPONDENCE, days=3)

match3 = play_lichess.create(TimeMode.UNLIMITED)
```

## 🔧 Options

### Real-time

| Argument    | Type      | Default    | Description                                         |
| ----------- | --------- | ---------- | --------------------------------------------------- |
| `minutes`   | `int`     | `5`        | The number of minutes for the match                 |
| `increment` | `int`     | `8`        | Amount of seconds to increment the clock each turn  |
| `variant`   | `Variant` | `STANDARD` | The variant of the match (STANDARD, CHESS960, etc.) |
| `color`     | `Color`   | `RANDOM`   | The color assigned to the first player that joins   |

### Correspondence

| Argument  | Type      | Default    | Description                                         |
| --------- | --------- | ---------- | --------------------------------------------------- |
| `days`    | `int`     | `2`        | The number of days for the match                    |
| `variant` | `Variant` | `STANDARD` | The variant of the match (STANDARD, CHESS960, etc.) |
| `color`   | `Color`   | `RANDOM`   | The color assigned to the first player that joins   |

### Unlimited

| Argument  | Type      | Default    | Description                                         |
| --------- | --------- | ---------- | --------------------------------------------------- |
| `variant` | `Variant` | `STANDARD` | The variant of the match (STANDARD, CHESS960, etc.) |
| `color`   | `Color`   | `RANDOM`   | The color assigned to the first player that joins   |

## 🧰 Development

To run tests (pytest)

``python setup.py test``

To lint (flake8):

``pip install flake8==3.8.4 pytest``

``python setup.py lint``

