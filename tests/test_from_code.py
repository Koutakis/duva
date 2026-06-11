from duva import from_code, RegSO

BLACKEBERG_KOD = "0180R009"
INVALID_KOD = "INVALID"


def test_returns_dict_by_default():
    assert isinstance(from_code(BLACKEBERG_KOD), dict)


def test_returns_regso_object():
    assert isinstance(from_code(BLACKEBERG_KOD, as_object=True), RegSO)


def test_correct_regsonamn():
    assert from_code(BLACKEBERG_KOD)["regsonamn"] == "Blackeberg"


def test_correct_kommunkod():
    assert from_code(BLACKEBERG_KOD)["kommunkod"] == "0180"


def test_correct_kommunnamn():
    assert from_code(BLACKEBERG_KOD)["kommunnamn"] == "Stockholm"


def test_correct_lansnamn():
    assert from_code(BLACKEBERG_KOD)["lansnamn"] == "Stockholms län"


def test_not_on_land_false():
    assert from_code(BLACKEBERG_KOD)["not_on_land"] is False


def test_offshore_false():
    assert from_code(BLACKEBERG_KOD)["offshore"] is False


def test_invalid_kod_returns_none():
    assert from_code(INVALID_KOD) is None


def test_invalid_kod_as_object_returns_none():
    assert from_code(INVALID_KOD, as_object=True) is None


def test_object_attributes_match_dict():
    d = from_code(BLACKEBERG_KOD)
    obj = from_code(BLACKEBERG_KOD, as_object=True)
    assert obj.regsonamn == d["regsonamn"]
    assert obj.kommunkod == d["kommunkod"]
    assert obj.lansnamn == d["lansnamn"]
