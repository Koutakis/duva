import polars as pl
import pytest
from duva import enrich_df


@pytest.fixture
def sample_df() -> pl.DataFrame:
    return pl.DataFrame({
        "lon": [17.88, 20.5, 18.07, None],
        "lat": [59.35, 57.5, 59.28, None],
    })


def test_returns_polars_dataframe(sample_df: pl.DataFrame):
    assert isinstance(enrich_df(sample_df), pl.DataFrame)


def test_adds_regsonamn_column(sample_df: pl.DataFrame):
    assert "regsonamn" in enrich_df(sample_df).columns


def test_adds_kommunkod_column(sample_df: pl.DataFrame):
    assert "kommunkod" in enrich_df(sample_df).columns


def test_adds_kommunnamn_column(sample_df: pl.DataFrame):
    assert "kommunnamn" in enrich_df(sample_df).columns


def test_adds_lanskod_column(sample_df: pl.DataFrame):
    assert "lanskod" in enrich_df(sample_df).columns


def test_adds_lansnamn_column(sample_df: pl.DataFrame):
    assert "lansnamn" in enrich_df(sample_df).columns


def test_adds_not_on_land_column(sample_df: pl.DataFrame):
    assert "not_on_land" in enrich_df(sample_df).columns


def test_adds_offshore_column(sample_df: pl.DataFrame):
    assert "offshore" in enrich_df(sample_df).columns


def test_row_count_unchanged(sample_df: pl.DataFrame):
    assert len(enrich_df(sample_df)) == len(sample_df)


def test_correct_regsonamn_for_land(sample_df: pl.DataFrame):
    assert enrich_df(sample_df)["regsonamn"][0] == "Blackeberg"


def test_not_on_land_false_for_land(sample_df: pl.DataFrame):
    assert enrich_df(sample_df)["not_on_land"][0] is False


def test_not_on_land_true_for_baltic(sample_df: pl.DataFrame):
    assert enrich_df(sample_df)["not_on_land"][1] is True


def test_offshore_true_for_baltic(sample_df: pl.DataFrame):
    assert enrich_df(sample_df)["offshore"][1] is True


def test_null_coords_produce_null_regso(sample_df: pl.DataFrame):
    assert enrich_df(sample_df)["regsonamn"][3] is None


def test_custom_column_names():
    df = pl.DataFrame({"x": [17.88], "y": [59.35]})
    assert enrich_df(df, x_col="x", y_col="y")["regsonamn"][0] == "Blackeberg"


def test_lansnamn_correct(sample_df: pl.DataFrame):
    assert enrich_df(sample_df)["lansnamn"][0] == "Stockholms län"
