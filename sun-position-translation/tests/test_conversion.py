import sys
from pathlib import Path

# Ensure parent directory is on sys.path so we can import main.py
sys.path.append(str(Path(__file__).resolve().parents[1]))

from main import time_of_day_to_ticks, iso_to_time, parse_open_meteo_json


def test_time_of_day_to_ticks_canonical():
    # 06:00 -> 0 ticks
    from datetime import time

    assert time_of_day_to_ticks(time(6, 0)) == 0
    # 12:00 -> 6000 ticks
    assert time_of_day_to_ticks(time(12, 0)) == 6000
    # 18:00 -> 12000 ticks
    assert time_of_day_to_ticks(time(18, 0)) == 12000
    # 00:00 -> 18000 ticks
    assert time_of_day_to_ticks(time(0, 0)) == 18000


def test_iso_parsing_and_open_meteo_json():
    # ISO with Z should parse to the same wall-clock time
    t = iso_to_time("2025-10-17T06:00:00Z")
    assert t.hour == 6 and t.minute == 0

    sample = {
        "daily": {
            "sunrise": ["2025-10-17T06:00:00Z"],
            "sunset": ["2025-10-17T18:00:00Z"],
        }
    }
    sr, ss = parse_open_meteo_json(sample)
    assert sr == 0
    assert ss == 12000
