from pathlib import Path

import geopandas as gpd
import polars as pl
from shapely.geometry import Point

_GPKG_PATH = Path(__file__).parent / "RegSO_2025.gpkg"
_KOMMUN_PATH = Path(__file__).parent / "Kommun_Sweref99TM.TAB"

_GDF: gpd.GeoDataFrame = gpd.read_file(_GPKG_PATH).drop(
    columns=["objectid", "geometry"]
)
_GDF_GEO: gpd.GeoDataFrame = gpd.read_file(_GPKG_PATH)[["regsokod", "geometry"]]
_KOMMUN_GEO: gpd.GeoDataFrame = gpd.read_file(_KOMMUN_PATH)[
    ["KnKod", "KnNamn", "geometry"]
].set_crs("EPSG:3006", allow_override=True)
_KOD_INDEX: dict[str, dict] = {
    row["regsokod"]: row for row in _GDF.to_dict(orient="records")
}

_LAN: dict[str, str] = {
    "01": "Stockholms län",
    "03": "Uppsala län",
    "04": "Södermanlands län",
    "05": "Östergötlands län",
    "06": "Jönköpings län",
    "07": "Kronobergs län",
    "08": "Kalmar län",
    "09": "Gotlands län",
    "10": "Blekinge län",
    "12": "Skåne län",
    "13": "Hallands län",
    "14": "Västra Götalands län",
    "17": "Värmlands län",
    "18": "Örebro län",
    "19": "Västmanlands län",
    "20": "Dalarnas län",
    "21": "Gävleborgs län",
    "22": "Västernorrlands län",
    "23": "Jämtlands län",
    "24": "Västerbottens län",
    "25": "Norrbottens län",
}

_LON_MIN, _LAT_MIN, _LON_MAX, _LAT_MAX = 10.59, 55.13, 24.18, 69.06


class RegSO:
    def __init__(
        self,
        not_on_land: bool,
        is_baltic: bool = False,
        objektidentitet: str | None = None,
        objekttyp: str | None = None,
        regsokod: str | None = None,
        regsonamn: str | None = None,
        lanskod: str | None = None,
        lansnamn: str | None = None,
        kommunkod: str | None = None,
        kommunnamn: str | None = None,
        version: str | None = None,
        ansvarig_organisation: str | None = None,
        referensdatum: str | None = None,
    ) -> None:
        self.not_on_land = not_on_land
        self.is_baltic = is_baltic
        self.objektidentitet = objektidentitet
        self.objekttyp = objekttyp
        self.regsokod = regsokod
        self.regsonamn = regsonamn
        self.lanskod = lanskod
        self.lansnamn = lansnamn
        self.kommunkod = kommunkod
        self.kommunnamn = kommunnamn
        self.version = version
        self.ansvarig_organisation = ansvarig_organisation
        self.referensdatum = referensdatum

    def __repr__(self) -> str:
        return (
            f"RegSO(regsokod={self.regsokod!r}, regsonamn={self.regsonamn!r}, "
            f"kommunkod={self.kommunkod!r}, kommunnamn={self.kommunnamn!r}, "
            f"lansnamn={self.lansnamn!r}, not_on_land={self.not_on_land}, "
            f"is_baltic={self.is_baltic})"
        )


def _validate(x: float, y: float) -> None:
    if not (-180 <= x <= 180):
        raise ValueError(f"Invalid longitude: {x}. Must be between -180 and 180.")
    if not (-90 <= y <= 90):
        raise ValueError(f"Invalid latitude: {y}. Must be between -90 and 90.")
    if not (_LON_MIN <= x <= _LON_MAX and _LAT_MIN <= y <= _LAT_MAX):
        raise ValueError(f"Coordinates ({x}, {y}) are outside Sweden.")


def _lookup_kommun(point_3006: gpd.GeoDataFrame) -> tuple[str | None, str | None]:
    match = _KOMMUN_GEO[_KOMMUN_GEO.contains(point_3006.geometry.iloc[0])]
    if match.empty:
        return None, None
    return match.iloc[0]["KnKod"], match.iloc[0]["KnNamn"]


def _lookup_point(x: float, y: float) -> dict:
    point = gpd.GeoDataFrame(
        geometry=[Point(x, y)],
        crs="EPSG:4326",
    ).to_crs("EPSG:3006")

    match = _GDF_GEO[_GDF_GEO.contains(point.geometry.iloc[0])]

    if match.empty:
        kommunkod, kommunnamn = _lookup_kommun(point)
        return {
            "not_on_land": True,
            "is_baltic": kommunkod is None,
            "kommunkod": kommunkod,
            "kommunnamn": kommunnamn,
        }

    row = dict(_KOD_INDEX[match.iloc[0]["regsokod"]])
    km = _KOMMUN_GEO[_KOMMUN_GEO["KnKod"] == row["kommunkod"]]
    row["kommunnamn"] = km.iloc[0]["KnNamn"] if not km.empty else None
    row["lansnamn"] = _LAN.get(row["lanskod"])
    row["not_on_land"] = False
    row["is_baltic"] = False
    return row


def duva(x: float, y: float, as_object: bool = False) -> dict | RegSO:
    _validate(x, y)
    row = _lookup_point(x, y)
    return RegSO(**row) if as_object else row


def duva_many(
    coords: list[tuple[float, float]],
    as_object: bool = False,
) -> list[dict | RegSO]:
    results = []
    for x, y in coords:
        try:
            _validate(x, y)
            row = _lookup_point(x, y)
        except ValueError as e:
            row = {"error": str(e), "not_on_land": None}
        results.append(RegSO(**row) if as_object else row)
    return results


def duva_df(
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

    joined_regso = gpd.sjoin(gdf, _GDF_GEO, how="left", predicate="within")
    joined_kommun = gpd.sjoin(gdf, _KOMMUN_GEO, how="left", predicate="within")

    regsokod_list: list[str | None] = [None] * len(pdf)
    regsonamn_list: list[str | None] = [None] * len(pdf)
    kommunkod_list: list[str | None] = [None] * len(pdf)
    kommunnamn_list: list[str | None] = [None] * len(pdf)
    lanskod_list: list[str | None] = [None] * len(pdf)
    lansnamn_list: list[str | None] = [None] * len(pdf)
    not_on_land_list: list[bool] = [False] * len(pdf)
    is_baltic_list: list[bool] = [False] * len(pdf)

    for idx in pdf[valid].index:
        regso_match = joined_regso[joined_regso.index == idx]
        kommun_match = joined_kommun[joined_kommun.index == idx]

        kod = regso_match["regsokod"].iloc[0] if len(regso_match) else None
        if kod and not isinstance(kod, float):
            meta = _KOD_INDEX.get(kod, {})
            regsokod_list[idx] = kod
            regsonamn_list[idx] = meta.get("regsonamn")
            lanskod_list[idx] = meta.get("lanskod")
            lansnamn_list[idx] = _LAN.get(meta.get("lanskod", ""))
            kommunkod_list[idx] = meta.get("kommunkod")
            km = _KOMMUN_GEO[_KOMMUN_GEO["KnKod"] == kommunkod_list[idx]]
            kommunnamn_list[idx] = km.iloc[0]["KnNamn"] if not km.empty else None
        else:
            not_on_land_list[idx] = True
            if len(kommun_match):
                kk = kommun_match["KnKod"].iloc[0]
                kn = kommun_match["KnNamn"].iloc[0]
                kommunkod_list[idx] = None if isinstance(kk, float) else kk
                kommunnamn_list[idx] = None if isinstance(kn, float) else kn
            is_baltic_list[idx] = kommunkod_list[idx] is None

    return df.with_columns(
        [
            pl.Series("regsokod", regsokod_list, dtype=pl.String),
            pl.Series("regsonamn", regsonamn_list, dtype=pl.String),
            pl.Series("kommunkod", kommunkod_list, dtype=pl.String),
            pl.Series("kommunnamn", kommunnamn_list, dtype=pl.String),
            pl.Series("lanskod", lanskod_list, dtype=pl.String),
            pl.Series("lansnamn", lansnamn_list, dtype=pl.String),
            pl.Series("not_on_land", not_on_land_list, dtype=pl.Boolean),
            pl.Series("is_baltic", is_baltic_list, dtype=pl.Boolean),
        ]
    )


def duva_from_kod(kod: str, as_object: bool = False) -> dict | RegSO | None:
    row = _KOD_INDEX.get(kod)
    if row is None:
        return None
    row = dict(row)
    km = _KOMMUN_GEO[_KOMMUN_GEO["KnKod"] == row["kommunkod"]]
    row["kommunnamn"] = km.iloc[0]["KnNamn"] if not km.empty else None
    row["lansnamn"] = _LAN.get(row["lanskod"])
    row["not_on_land"] = False
    row["is_baltic"] = False
    return RegSO(**row) if as_object else row
