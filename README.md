# duva 🕊️
Reverse geocode Swedish coordinates to RegSO areas.

## Install
```bash
pip install duva
```

## Usage
```python
from duva import locate, locate_many, enrich_df, from_code

# Single coordinate (WGS84)
locate(x=17.88, y=59.35)
# {'regsonamn': 'Blackeberg', 'kommunnamn': 'Stockholm', 'lansnamn': 'Stockholms län', ...}

# As object
result = locate(x=17.88, y=59.35, as_object=True)
result.regsonamn  # 'Blackeberg'

# List of coordinates
locate_many([(17.88, 59.35), (18.07, 59.28)])

# Enrich a Polars DataFrame
enrich_df(df, x_col="lon", y_col="lat")

# Lookup by RegSO code
from_code("0180R009")
```

## Notes
- Input coordinates must be WGS84 (standard GPS)
- Raises `ValueError` for invalid coordinates or coordinates outside Sweden
- Returns `not_on_land=True` for water areas, `offshore=True` for international water
- Based on SCB's RegSO 2025 and municipality boundaries
