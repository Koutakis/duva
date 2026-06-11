from duva import search, RegSO


def test_returns_list():
    assert isinstance(search("östermalm"), list)


def test_partial_match():
    assert len(search("östermalm")) > 1


def test_case_insensitive():
    assert len(search("ÖSTERMALM")) == len(search("östermalm"))


def test_filter_by_kommunnamn():
    all_results = search("östermalm")
    filtered = search("östermalm", kommunnamn="Borlänge")
    assert len(filtered) < len(all_results)
    assert all(r["kommunnamn"] == "Borlänge" for r in filtered)


def test_filter_by_lansnamn():
    results = search("centrum", lansnamn="Stockholms län")
    assert len(results) > 0
    assert all(r["lansnamn"] == "Stockholms län" for r in results)


def test_filter_by_both():
    results = search("centrum", kommunnamn="Sollentuna", lansnamn="Stockholms län")
    assert len(results) > 0
    assert all(r["kommunnamn"] == "Sollentuna" for r in results)
    assert all(r["lansnamn"] == "Stockholms län" for r in results)


def test_no_match_returns_empty_list():
    assert search("xyznonexistent") == []


def test_returns_regso_objects():
    results = search("östermalm", as_object=True)
    assert all(isinstance(r, RegSO) for r in results)


def test_kommunnamn_filter_case_insensitive():
    upper = search("östermalm", kommunnamn="BORLÄNGE")
    lower = search("östermalm", kommunnamn="borlänge")
    assert len(upper) == len(lower)


def test_result_has_kommunnamn():
    results = search("blackeberg")
    assert results[0]["kommunnamn"] == "Stockholm"


def test_result_has_lansnamn():
    results = search("blackeberg")
    assert results[0]["lansnamn"] == "Stockholms län"


def test_not_on_land_false():
    results = search("blackeberg")
    assert results[0]["not_on_land"] is False
