"""Conversion utilities for time-of-day to Minecraft ticks.

Minecraft time reference:
- 0 ticks = 06:00 (sunrise)
- 6000 ticks = 12:00 (noon)
- 12000 ticks = 18:00 (sunset)
- 18000 ticks = 00:00 (midnight)
"""

from __future__ import annotations

import datetime as _dt


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


def interpolate_ticks(sunrise_time: _dt.time, sunset_time: _dt.time, current_time: _dt.time) -> int:
    """
    Interpolate current time to Minecraft ticks based on sunrise and sunset.
    
    Minecraft day cycle (standard mapping):
    - 0 ticks = 6:00 AM (dawn/sunrise start)
    - 1000 ticks = 7:00 AM (day starts)
    - 6000 ticks = 12:00 PM (noon)
    - 12000 ticks = 6:00 PM (sunset)
    - 13000 ticks = 7:00 PM (night starts)
    - 18000 ticks = 12:00 AM (midnight)
    - 23000 ticks = 5:00 AM (dawn begins)
    
    This function maps real-world time proportionally:
    - Maps sunrise→sunset to ticks 0→12000 (day phase)
    - Maps sunset→sunrise to ticks 12000→24000 (night phase)
    
    Args:
        sunrise_time: Time of sunrise
        sunset_time: Time of sunset
        current_time: Current time to convert
        
    Returns:
        int: Minecraft ticks (0-23999)
    """
    def time_to_seconds(t: _dt.time) -> float:
        return t.hour * 3600 + t.minute * 60 + t.second + t.microsecond / 1e6
    
    sunrise_sec = time_to_seconds(sunrise_time)
    sunset_sec = time_to_seconds(sunset_time)
    current_sec = time_to_seconds(current_time)
    
    # Day duration (sunrise to sunset)
    day_duration = sunset_sec - sunrise_sec
    # Night duration (sunset to next sunrise) 
    night_duration = 24 * 3600 - day_duration
    
    if sunrise_sec <= current_sec < sunset_sec:
        # Daytime: sunrise (0 ticks) to sunset (12000 ticks)
        progress = (current_sec - sunrise_sec) / day_duration
        ticks = int(progress * 12000)
    elif current_sec >= sunset_sec:
        # Evening/Night after sunset (same day): 12000 ticks towards 24000
        time_since_sunset = current_sec - sunset_sec
        progress = time_since_sunset / night_duration
        ticks = int(12000 + progress * 12000)
    else:
        # Early morning before sunrise (before sunrise on current day)
        # We're in the "night" period that started at yesterday's sunset
        # Time elapsed since yesterday's sunset = (24h - sunset_sec) + current_sec
        time_since_sunset = (24 * 3600 - sunset_sec) + current_sec
        progress = time_since_sunset / night_duration
        ticks = int(12000 + progress * 12000)
    
    return ticks % 24000
