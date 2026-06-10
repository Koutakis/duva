# duva 🕊️

Reverse geocode Swedish coordinates to RegSO areas.

## Install

```bash
pip install duva
```

## Usage

```python
from duva import duva, duva_many, duva_df, duva_from_kod

# Single coordinate (WGS84)
duva(x=17.88, y=59.35)
# {'regsonamn': 'Blackeberg', 'kommunnamn': 'Stockholm', 'lansnamn': 'Stockholms län', ...}

# As object
result = duva(x=17.88, y=59.35, as_object=True)
result.regsonamn  # 'Blackeberg'

# List of coordinates
duva_many([(17.88, 59.35), (18.07, 59.28)])

# Enrich a Polars DataFrame
duva_df(df, x_col="lon", y_col="lat")

# Lookup by RegSO code
duva_from_kod("0180R009")
```

## Notes

- Input coordinates must be WGS84 (standard GPS)
- Raises `ValueError` for invalid coordinates or coordinates outside Sweden
- Returns `not_on_land=True` for water areas, `is_baltic=True` for international water
- Based on SCB's RegSO 2025 and municipality boundaries
