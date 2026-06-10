from duva import duva_many, RegSO

BLACKEBERG = (17.88, 59.35)
BALTIC = (20.5, 57.5)
OUTSIDE_SWEDEN = (10.0, 50.0)
INVALID_LON = (200.0, 59.0)


def test_returns_list():
    result = duva_many([BLACKEBERG])
    assert isinstance(result, list)


def test_returns_correct_length():
    coords = [BLACKEBERG, BALTIC, OUTSIDE_SWEDEN]
    result = duva_many(coords)
    assert len(result) == 3


def test_returns_dicts_by_default():
    result = duva_many([BLACKEBERG, BALTIC])
    assert all(isinstance(r, dict) for r in result)


def test_returns_regso_objects():
    result = duva_many([BLACKEBERG, BALTIC], as_object=True)
    assert all(isinstance(r, RegSO) for r in result)


def test_correct_result_for_land():
    result = duva_many([BLACKEBERG])
    assert result[0]["regsonamn"] == "Blackeberg"


def test_water_returns_not_on_land():
    result = duva_many([BALTIC])
    assert result[0]["not_on_land"] is True


def test_invalid_coords_returns_error_key():
    result = duva_many([OUTSIDE_SWEDEN])
    assert "error" in result[0]


def test_invalid_coords_not_on_land_is_none():
    result = duva_many([OUTSIDE_SWEDEN])
    assert result[0]["not_on_land"] is None


def test_mixed_coords():
    result = duva_many([BLACKEBERG, BALTIC, OUTSIDE_SWEDEN])
    assert result[0]["regsonamn"] == "Blackeberg"
    assert result[1]["not_on_land"] is True
    assert "error" in result[2]


def test_empty_list():
    result = duva_many([])
    assert result == []


def test_invalid_lon_returns_error():
    result = duva_many([INVALID_LON])
    assert "error" in result[0]
