from pathlib import Path

import geopandas as gpd

_GPKG_PATH = Path(__file__).parent / "RegSO_2025.gpkg"

GDF: gpd.GeoDataFrame = gpd.read_file(_GPKG_PATH).drop(columns=["objectid", "geometry"])
GDF_GEO: gpd.GeoDataFrame = gpd.read_file(_GPKG_PATH)[["regsokod", "geometry"]]
KOD_INDEX: dict[str, dict] = {
    row["regsokod"]: row
    for row in GDF.to_dict(orient="records")
}


def lookup(point: gpd.GeoDataFrame) -> str | None:
    match = GDF_GEO[GDF_GEO.contains(point.geometry.iloc[0])]
    if match.empty:
        return None
    return match.iloc[0]["regsokod"]
