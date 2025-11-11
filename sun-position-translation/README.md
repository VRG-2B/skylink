# Sun position -> Minecraft ticks

Small utility to convert Open-Meteo sunrise/sunset ISO datetimes into
Minecraft ticks.

Usage
-----

From the `sun-position-translation` folder:

1. Install dependencies (preferably in a venv):

```bash
pip install -r requirements.txt
```

2. Run against a local JSON file:

```bash
python main.py /path/to/open_meteo.json
```

3. Or run against a URL returned by Open-Meteo:

```bash
python main.py "https://api.open-meteo.com/v1/forecast?latitude=54.6892&longitude=25.2798&daily=sunrise,sunset"
```

Tests
-----

Run pytest from the `sun-position-translation` folder:

```bash
pytest -q
```
