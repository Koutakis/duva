from duva import locate_many, RegSO

BLACKEBERG = (17.88, 59.35)
BALTIC = (20.5, 57.5)
OUTSIDE_SWEDEN = (10.0, 50.0)
INVALID_LON = (200.0, 59.0)


def test_returns_list():
    assert isinstance(locate_many([BLACKEBERG]), list)


def test_returns_correct_length():
    assert len(locate_many([BLACKEBERG, BALTIC, OUTSIDE_SWEDEN])) == 3


def test_returns_dicts_by_default():
    assert all(isinstance(r, dict) for r in locate_many([BLACKEBERG, BALTIC]))


def test_returns_regso_objects():
    assert all(isinstance(r, RegSO) for r in locate_many([BLACKEBERG, BALTIC], as_object=True))


def test_correct_result_for_land():
    assert locate_many([BLACKEBERG])[0]["regsonamn"] == "Blackeberg"


def test_water_returns_not_on_land():
    assert locate_many([BALTIC])[0]["not_on_land"] is True


def test_invalid_coords_returns_error_key():
    assert "error" in locate_many([OUTSIDE_SWEDEN])[0]


def test_invalid_coords_not_on_land_is_none():
    assert locate_many([OUTSIDE_SWEDEN])[0]["not_on_land"] is None


def test_mixed_coords():
    result = locate_many([BLACKEBERG, BALTIC, OUTSIDE_SWEDEN])
    assert result[0]["regsonamn"] == "Blackeberg"
    assert result[1]["not_on_land"] is True
    assert "error" in result[2]


def test_empty_list():
    assert locate_many([]) == []


def test_invalid_lon_returns_error():
    assert "error" in locate_many([INVALID_LON])[0]
