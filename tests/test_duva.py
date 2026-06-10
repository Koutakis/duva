import pytest
from duva import duva, RegSO

BLACKEBERG = (17.88, 59.35)
GAMLA_ENSKEDE = (18.07, 59.28)
BALTIC = (20.5, 57.5)


def test_returns_dict_by_default():
    result = duva(*BLACKEBERG)
    assert isinstance(result, dict)


def test_returns_regso_object():
    result = duva(*BLACKEBERG, as_object=True)
    assert isinstance(result, RegSO)


def test_correct_regsonamn():
    result = duva(*BLACKEBERG)
    assert result["regsonamn"] == "Blackeberg"


def test_correct_kommunkod():
    result = duva(*BLACKEBERG)
    assert result["kommunkod"] == "0180"


def test_correct_kommunnamn():
    result = duva(*BLACKEBERG)
    assert result["kommunnamn"] == "Stockholm"


def test_correct_lansnamn():
    result = duva(*BLACKEBERG)
    assert result["lansnamn"] == "Stockholms län"


def test_not_on_land_false_for_land():
    result = duva(*BLACKEBERG)
    assert result["not_on_land"] is False


def test_is_baltic_false_for_land():
    result = duva(*BLACKEBERG)
    assert result["is_baltic"] is False


def test_not_on_land_true_for_water():
    result = duva(*BALTIC)
    assert result["not_on_land"] is True


def test_is_baltic_true_for_baltic():
    result = duva(*BALTIC)
    assert result["is_baltic"] is True


def test_water_has_no_regsonamn():
    result = duva(*BALTIC)
    assert result.get("regsonamn") is None


def test_object_attributes_match_dict():
    d = duva(*GAMLA_ENSKEDE)
    obj = duva(*GAMLA_ENSKEDE, as_object=True)
    assert obj.regsonamn == d["regsonamn"]
    assert obj.kommunkod == d["kommunkod"]
    assert obj.lansnamn == d["lansnamn"]


def test_invalid_longitude_raises():
    with pytest.raises(ValueError, match="longitude"):
        duva(x=200.0, y=59.0)


def test_invalid_latitude_raises():
    with pytest.raises(ValueError, match="latitude"):
        duva(x=17.0, y=100.0)


def test_outside_sweden_raises():
    with pytest.raises(ValueError, match="outside Sweden"):
        duva(x=10.0, y=50.0)
