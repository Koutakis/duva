from duva import from_name, RegSO


def test_returns_list():
    assert isinstance(from_name("Blackeberg"), list)


def test_unique_name_returns_one_result():
    assert len(from_name("Blackeberg")) == 1


def test_duplicate_name_returns_multiple():
    assert len(from_name("Östermalm")) > 1


def test_correct_regsokod():
    result = from_name("Blackeberg")
    assert result[0]["regsokod"] == "0180R009"


def test_correct_kommunnamn():
    result = from_name("Blackeberg")
    assert result[0]["kommunnamn"] == "Stockholm"


def test_correct_lansnamn():
    result = from_name("Blackeberg")
    assert result[0]["lansnamn"] == "Stockholms län"


def test_case_insensitive():
    assert from_name("blackeberg")[0]["regsonamn"] == "Blackeberg"
    assert from_name("BLACKEBERG")[0]["regsonamn"] == "Blackeberg"


def test_not_found_returns_empty_list():
    assert from_name("DoesNotExist") == []


def test_returns_regso_objects():
    result = from_name("Blackeberg", as_object=True)
    assert all(isinstance(r, RegSO) for r in result)


def test_not_on_land_false():
    result = from_name("Blackeberg")
    assert result[0]["not_on_land"] is False


def test_offshore_false():
    result = from_name("Blackeberg")
    assert result[0]["offshore"] is False


def test_duplicate_results_have_different_kommunnamn():
    results = from_name("Östermalm")
    kommuner = [r["kommunnamn"] for r in results]
    assert len(set(kommuner)) > 1
