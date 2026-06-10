import polars as pl
import pytest
from duva import duva_df


@pytest.fixture
def sample_df() -> pl.DataFrame:
    return pl.DataFrame({
        "lon": [17.88, 20.5, 18.07, None],
        "lat": [59.35, 57.5, 59.28, None],
    })


def test_returns_polars_dataframe(sample_df: pl.DataFrame):
    result = duva_df(sample_df)
    assert isinstance(result, pl.DataFrame)


def test_adds_regsonamn_column(sample_df: pl.DataFrame):
    result = duva_df(sample_df)
    assert "regsonamn" in result.columns


def test_adds_kommunkod_column(sample_df: pl.DataFrame):
    result = duva_df(sample_df)
    assert "kommunkod" in result.columns


def test_adds_kommunnamn_column(sample_df: pl.DataFrame):
    result = duva_df(sample_df)
    assert "kommunnamn" in result.columns


def test_adds_lanskod_column(sample_df: pl.DataFrame):
    result = duva_df(sample_df)
    assert "lanskod" in result.columns


def test_adds_lansnamn_column(sample_df: pl.DataFrame):
    result = duva_df(sample_df)
    assert "lansnamn" in result.columns


def test_adds_not_on_land_column(sample_df: pl.DataFrame):
    result = duva_df(sample_df)
    assert "not_on_land" in result.columns


def test_adds_is_baltic_column(sample_df: pl.DataFrame):
    result = duva_df(sample_df)
    assert "is_baltic" in result.columns


def test_row_count_unchanged(sample_df: pl.DataFrame):
    result = duva_df(sample_df)
    assert len(result) == len(sample_df)


def test_correct_regsonamn_for_land(sample_df: pl.DataFrame):
    result = duva_df(sample_df)
    assert result["regsonamn"][0] == "Blackeberg"


def test_not_on_land_false_for_land(sample_df: pl.DataFrame):
    result = duva_df(sample_df)
    assert result["not_on_land"][0] is False


def test_not_on_land_true_for_baltic(sample_df: pl.DataFrame):
    result = duva_df(sample_df)
    assert result["not_on_land"][1] is True


def test_is_baltic_true_for_baltic(sample_df: pl.DataFrame):
    result = duva_df(sample_df)
    assert result["is_baltic"][1] is True


def test_null_coords_produce_null_regso(sample_df: pl.DataFrame):
    result = duva_df(sample_df)
    assert result["regsonamn"][3] is None


def test_custom_column_names():
    df = pl.DataFrame({"x": [17.88], "y": [59.35]})
    result = duva_df(df, x_col="x", y_col="y")
    assert result["regsonamn"][0] == "Blackeberg"


def test_lansnamn_correct(sample_df: pl.DataFrame):
    result = duva_df(sample_df)
    assert result["lansnamn"][0] == "Stockholms län"
