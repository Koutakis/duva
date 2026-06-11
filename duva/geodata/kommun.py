from pathlib import Path

import geopandas as gpd

_KOMMUN_PATH = Path(__file__).parent / "Kommun_Sweref99TM.TAB"

GDF_GEO: gpd.GeoDataFrame = gpd.read_file(_KOMMUN_PATH)[["KnKod", "KnNamn", "geometry"]].set_crs("EPSG:3006", allow_override=True)


def lookup(point: gpd.GeoDataFrame) -> tuple[str | None, str | None]:
    match = GDF_GEO[GDF_GEO.contains(point.geometry.iloc[0])]
    if match.empty:
        return None, None
    return match.iloc[0]["KnKod"], match.iloc[0]["KnNamn"]
