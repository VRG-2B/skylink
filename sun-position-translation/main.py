"""Convert Open-Meteo sunrise/sunset datetimes into Minecraft ticks.

This module provides functions to parse ISO 8601 datetimes returned by
Open-Meteo (UTC by default) and convert the local solar times into
Minecraft ticks. It also exposes a small CLI to read JSON from a file
or a URL and print tick values for sunrise and sunset.

Minecraft time reference used:
- 0 ticks = 06:00 (sunrise)
- 6000 ticks = 12:00 (noon)
- 12000 ticks = 18:00 (sunset)
- 18000 ticks = 00:00 (midnight)

Conversion details:
- We'll compute the fraction of the 24-hour day for a given time of day
  then multiply by 24000 and round to nearest int. This maps 06:00 to 0.

Note: Open-Meteo returns times in ISO 8601; the caller must ensure the
times are in the desired timezone or converted appropriately before
passing. This module treats input datetimes as naive local times (no
timezone adjustment) unless an explicit timezone offset is present in
the string (ISO format). If timezone-aware strings are passed, they
will be parsed accordingly.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
from typing import Tuple, Dict, Any

import requests


def time_of_day_to_ticks(dt: _dt.time) -> int:
	"""Convert a time-of-day to Minecraft ticks.

	Inputs:
	- dt: datetime.time object (can include tzinfo)

	Output: integer ticks in range [0, 23999]
	"""
	# Convert time to seconds since midnight
	seconds = dt.hour * 3600 + dt.minute * 60 + dt.second + dt.microsecond / 1e6
	# Minecraft defines 0 ticks at 06:00. Compute seconds since 06:00.
	seconds_since_6 = (seconds - 6 * 3600) % (24 * 3600)
	ticks = int(round((seconds_since_6 / (24 * 3600)) * 24000)) % 24000
	return ticks


def iso_to_time(iso_str: str) -> _dt.time:
	"""Parse an ISO 8601 datetime string to a time object.

	Handles timezone-aware strings by converting to local naive time
	(i.e., the wall-clock time represented by the timestamp). If the
	string has a timezone offset, the returned time will be the UTC
	time adjusted to that offset (so it's the actual local clock time
	expressed by the timestamp).
	"""
	# Use fromisoformat for robust parsing (Python 3.11+ handles Z)
	# But ensure we support trailing Z (Zulu) by replacing it with +00:00
	s = iso_str.replace("Z", "+00:00") if iso_str.endswith("Z") else iso_str
	dt = _dt.datetime.fromisoformat(s)
	# If timezone-aware, convert to that tz's wall-time and drop tzinfo
	if dt.tzinfo is not None:
		# Normalize to the timezone's local time (astimezone to same tz returns same offset)
		local = dt.astimezone(dt.tzinfo)
		return local.timetz().replace(tzinfo=None)
	return dt.time()


def parse_open_meteo_json(data: Dict[str, Any]) -> Tuple[int, int]:
	"""Extract sunrise and sunset from Open-Meteo daily JSON and return ticks.

	Expects the JSON structure with keys like data['daily']['sunrise'] and
	data['daily']['sunset'] containing ISO datetime strings. Returns
	(sunrise_ticks, sunset_ticks) for the first day in the arrays.
	"""
	daily = data.get("daily")
	if not daily:
		raise ValueError("JSON missing 'daily' key")
	sunrises = daily.get("sunrise") or daily.get("sunrise_iso")
	sunsets = daily.get("sunset") or daily.get("sunset_iso")
	if not sunrises or not sunsets:
		raise ValueError("JSON 'daily' missing 'sunrise' or 'sunset' arrays")
	# Take first entry
	sr_iso = sunrises[0]
	ss_iso = sunsets[0]
	sr_time = iso_to_time(sr_iso)
	ss_time = iso_to_time(ss_iso)
	return time_of_day_to_ticks(sr_time), time_of_day_to_ticks(ss_time)


def fetch_open_meteo(url: str) -> Dict[str, Any]:
	resp = requests.get(url)
	resp.raise_for_status()
	return resp.json()


def main(argv: list | None = None) -> int:
	p = argparse.ArgumentParser(description="Convert Open-Meteo sunrise/sunset to Minecraft ticks")
	p.add_argument("source", help="Path to JSON file or full URL to fetch Open-Meteo JSON")
	args = p.parse_args(argv)
	src = args.source
	if src.startswith("http://") or src.startswith("https://"):
		data = fetch_open_meteo(src)
	else:
		with open(src, "r", encoding="utf8") as f:
			data = json.load(f)
	sr_ticks, ss_ticks = parse_open_meteo_json(data)
	print(f"sunrise_ticks: {sr_ticks}")
	print(f"sunset_ticks: {ss_ticks}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
