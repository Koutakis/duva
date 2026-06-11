_LON_MIN, _LAT_MIN, _LON_MAX, _LAT_MAX = 10.59, 55.13, 24.18, 69.06


def validate(x: float, y: float) -> None:
    if not (-180 <= x <= 180):
        raise ValueError(f"Invalid longitude: {x}. Must be between -180 and 180.")
    if not (-90 <= y <= 90):
        raise ValueError(f"Invalid latitude: {y}. Must be between -90 and 90.")
    if not (_LON_MIN <= x <= _LON_MAX and _LAT_MIN <= y <= _LAT_MAX):
        raise ValueError(f"Coordinates ({x}, {y}) are outside Sweden.")
