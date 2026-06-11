import pytest
from duva import locate, RegSO

BLACKEBERG = (17.88, 59.35)
GAMLA_ENSKEDE = (18.07, 59.28)
BALTIC = (20.5, 57.5)


def test_returns_dict_by_default():
    assert isinstance(locate(*BLACKEBERG), dict)


def test_returns_regso_object():
    assert isinstance(locate(*BLACKEBERG, as_object=True), RegSO)


def test_correct_regsonamn():
    assert locate(*BLACKEBERG)["regsonamn"] == "Blackeberg"


def test_correct_kommunkod():
    assert locate(*BLACKEBERG)["kommunkod"] == "0180"


def test_correct_kommunnamn():
    assert locate(*BLACKEBERG)["kommunnamn"] == "Stockholm"


def test_correct_lansnamn():
    assert locate(*BLACKEBERG)["lansnamn"] == "Stockholms län"


def test_not_on_land_false_for_land():
    assert locate(*BLACKEBERG)["not_on_land"] is False


def test_offshore_false_for_land():
    assert locate(*BLACKEBERG)["offshore"] is False


def test_not_on_land_true_for_water():
    assert locate(*BALTIC)["not_on_land"] is True


def test_offshore_true_for_baltic():
    assert locate(*BALTIC)["offshore"] is True


def test_water_has_no_regsonamn():
    assert locate(*BALTIC).get("regsonamn") is None


def test_object_attributes_match_dict():
    d = locate(*GAMLA_ENSKEDE)
    obj = locate(*GAMLA_ENSKEDE, as_object=True)
    assert obj.regsonamn == d["regsonamn"]
    assert obj.kommunkod == d["kommunkod"]
    assert obj.lansnamn == d["lansnamn"]


def test_invalid_longitude_raises():
    with pytest.raises(ValueError, match="longitude"):
        locate(x=200.0, y=59.0)


def test_invalid_latitude_raises():
    with pytest.raises(ValueError, match="latitude"):
        locate(x=17.0, y=100.0)


def test_outside_sweden_raises():
    with pytest.raises(ValueError, match="outside Sweden"):
        locate(x=10.0, y=50.0)
