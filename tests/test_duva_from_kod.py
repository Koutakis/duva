from duva import duva_from_kod, RegSO

BLACKEBERG_KOD = "0180R009"
INVALID_KOD = "INVALID"


def test_returns_dict_by_default():
    result = duva_from_kod(BLACKEBERG_KOD)
    assert isinstance(result, dict)


def test_returns_regso_object():
    result = duva_from_kod(BLACKEBERG_KOD, as_object=True)
    assert isinstance(result, RegSO)


def test_correct_regsonamn():
    result = duva_from_kod(BLACKEBERG_KOD)
    assert result["regsonamn"] == "Blackeberg"


def test_correct_kommunkod():
    result = duva_from_kod(BLACKEBERG_KOD)
    assert result["kommunkod"] == "0180"


def test_correct_kommunnamn():
    result = duva_from_kod(BLACKEBERG_KOD)
    assert result["kommunnamn"] == "Stockholm"


def test_correct_lansnamn():
    result = duva_from_kod(BLACKEBERG_KOD)
    assert result["lansnamn"] == "Stockholms län"


def test_not_on_land_false():
    result = duva_from_kod(BLACKEBERG_KOD)
    assert result["not_on_land"] is False


def test_is_baltic_false():
    result = duva_from_kod(BLACKEBERG_KOD)
    assert result["is_baltic"] is False


def test_invalid_kod_returns_none():
    result = duva_from_kod(INVALID_KOD)
    assert result is None


def test_invalid_kod_as_object_returns_none():
    result = duva_from_kod(INVALID_KOD, as_object=True)
    assert result is None


def test_object_attributes_match_dict():
    d = duva_from_kod(BLACKEBERG_KOD)
    obj = duva_from_kod(BLACKEBERG_KOD, as_object=True)
    assert obj.regsonamn == d["regsonamn"]
    assert obj.kommunkod == d["kommunkod"]
    assert obj.lansnamn == d["lansnamn"]
