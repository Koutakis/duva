import geopandas as gpd
import polars as pl
from shapely.geometry import Point

from duva.geodata import kommun, regso
from duva.geodata.lan import LAN
from duva.models import RegSO
from duva.validate import validate


def _to_point(x: float, y: float) -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(
        geometry=[Point(x, y)],
        crs="EPSG:4326",
    ).to_crs("EPSG:3006")


def _lookup_point(x: float, y: float) -> dict:
    point = _to_point(x, y)
    kod = regso.lookup(point)

    if kod is None:
        kommunkod, kommunnamn = kommun.lookup(point)
        return {
            "not_on_land": True,
            "offshore": kommunkod is None,
            "kommunkod": kommunkod,
            "kommunnamn": kommunnamn,
        }

    row = dict(regso.KOD_INDEX[kod])
    km = kommun.GDF_GEO[kommun.GDF_GEO["KnKod"] == row["kommunkod"]]
    row["kommunnamn"] = km.iloc[0]["KnNamn"] if not km.empty else None
    row["lansnamn"] = LAN.get(row["lanskod"])
    row["not_on_land"] = False
    row["offshore"] = False
    return row


def locate(x: float, y: float, as_object: bool = False) -> dict | RegSO:
    validate(x, y)
    row = _lookup_point(x, y)
    return RegSO(**row) if as_object else row


def locate_many(
    coords: list[tuple[float, float]],
    as_object: bool = False,
) -> list[dict | RegSO]:
    results = []
    for x, y in coords:
        try:
            validate(x, y)
            row = _lookup_point(x, y)
        except ValueError as e:
            row = {"error": str(e), "not_on_land": None}
        results.append(RegSO(**row) if as_object else row)
    return results


def enrich_df(
    df: pl.DataFrame,
    x_col: str = "lon",
    y_col: str = "lat",
) -> pl.DataFrame:
    pdf = df.to_pandas()
    valid = pdf[x_col].notna() & pdf[y_col].notna()

    gdf = gpd.GeoDataFrame(
        pdf[valid][[x_col, y_col]].copy(),
        geometry=gpd.points_from_xy(
            pdf.loc[valid, x_col].astype(float),
            pdf.loc[valid, y_col].astype(float),
        ),
        crs="EPSG:4326",
    ).to_crs("EPSG:3006")

    joined_regso = gpd.sjoin(gdf, regso.GDF_GEO, how="left", predicate="within")
    joined_kommun = gpd.sjoin(gdf, kommun.GDF_GEO, how="left", predicate="within")

    regsokod_list: list[str | None] = [None] * len(pdf)
    regsonamn_list: list[str | None] = [None] * len(pdf)
    kommunkod_list: list[str | None] = [None] * len(pdf)
    kommunnamn_list: list[str | None] = [None] * len(pdf)
    lanskod_list: list[str | None] = [None] * len(pdf)
    lansnamn_list: list[str | None] = [None] * len(pdf)
    not_on_land_list: list[bool] = [False] * len(pdf)
    offshore_list: list[bool] = [False] * len(pdf)

    for idx in pdf[valid].index:
        regso_match = joined_regso[joined_regso.index == idx]
        kommun_match = joined_kommun[joined_kommun.index == idx]

        kod = regso_match["regsokod"].iloc[0] if len(regso_match) else None
        if kod and not isinstance(kod, float):
            meta = regso.KOD_INDEX.get(kod, {})
            regsokod_list[idx] = kod
            regsonamn_list[idx] = meta.get("regsonamn")
            lanskod_list[idx] = meta.get("lanskod")
            lansnamn_list[idx] = LAN.get(meta.get("lanskod", ""))
            kommunkod_list[idx] = meta.get("kommunkod")
            km = kommun.GDF_GEO[kommun.GDF_GEO["KnKod"] == kommunkod_list[idx]]
            kommunnamn_list[idx] = km.iloc[0]["KnNamn"] if not km.empty else None
        else:
            not_on_land_list[idx] = True
            if len(kommun_match):
                kk = kommun_match["KnKod"].iloc[0]
                kn = kommun_match["KnNamn"].iloc[0]
                kommunkod_list[idx] = None if isinstance(kk, float) else kk
                kommunnamn_list[idx] = None if isinstance(kn, float) else kn
            offshore_list[idx] = kommunkod_list[idx] is None

    return df.with_columns([
        pl.Series("regsokod", regsokod_list, dtype=pl.String),
        pl.Series("regsonamn", regsonamn_list, dtype=pl.String),
        pl.Series("kommunkod", kommunkod_list, dtype=pl.String),
        pl.Series("kommunnamn", kommunnamn_list, dtype=pl.String),
        pl.Series("lanskod", lanskod_list, dtype=pl.String),
        pl.Series("lansnamn", lansnamn_list, dtype=pl.String),
        pl.Series("not_on_land", not_on_land_list, dtype=pl.Boolean),
        pl.Series("offshore", offshore_list, dtype=pl.Boolean),
    ])


def from_code(kod: str, as_object: bool = False) -> dict | RegSO | None:
    row = regso.KOD_INDEX.get(kod)
    if row is None:
        return None
    row = dict(row)
    km = kommun.GDF_GEO[kommun.GDF_GEO["KnKod"] == row["kommunkod"]]
    row["kommunnamn"] = km.iloc[0]["KnNamn"] if not km.empty else None
    row["lansnamn"] = LAN.get(row["lanskod"])
    row["not_on_land"] = False
    row["offshore"] = False
    return RegSO(**row) if as_object else row


def from_name(name: str, as_object: bool = False) -> list[dict | RegSO]:
    matches = regso.GDF[regso.GDF["regsonamn"].str.lower() == name.lower()]
    results = []
    for _, row in matches.iterrows():
        r = dict(row)
        km = kommun.GDF_GEO[kommun.GDF_GEO["KnKod"] == r["kommunkod"]]
        r["kommunnamn"] = km.iloc[0]["KnNamn"] if not km.empty else None
        r["lansnamn"] = LAN.get(r["lanskod"])
        r["not_on_land"] = False
        r["offshore"] = False
        results.append(RegSO(**r) if as_object else r)
    return results


def search(
    name: str,
    kommunnamn: str | None = None,
    lansnamn: str | None = None,
    as_object: bool = False,
) -> list[dict | RegSO]:
    matches = regso.GDF[regso.GDF["regsonamn"].str.lower().str.contains(name.lower())]

    results = []
    for _, row in matches.iterrows():
        r = dict(row)
        km = kommun.GDF_GEO[kommun.GDF_GEO["KnKod"] == r["kommunkod"]]
        r["kommunnamn"] = km.iloc[0]["KnNamn"] if not km.empty else None
        r["lansnamn"] = LAN.get(r["lanskod"])
        r["not_on_land"] = False
        r["offshore"] = False

        if kommunnamn and (r["kommunnamn"] or "").lower() != kommunnamn.lower():
            continue
        if lansnamn and (r["lansnamn"] or "").lower() != lansnamn.lower():
            continue

        results.append(RegSO(**r) if as_object else r)

    return results
