# type: ignore
"""
# Searching
"""

# %%
# Search a STAC API with `stacrs.search`:
import contextily
import pandas
import stacrs
from geopandas import GeoDataFrame

items = await stacrs.search(
    "https://stac.eoapi.dev",
    collections="MAXAR_Marshall_Fire_21_Update"
)
data_frame = GeoDataFrame.from_features(items)
data_frame["datetime"] = pandas.to_datetime(data_frame["datetime"])
axis = data_frame.set_crs(epsg=4326).to_crs(epsg=3857).plot(alpha=0.5, edgecolor="k")
contextily.add_basemap(axis, source=contextily.providers.CartoDB.Positron)
axis.set_axis_off()

# %%
# Search [stac-geoparquet](https://github.com/stac-utils/stac-geoparquet/blob/main/spec/stac-geoparquet-spec.md) with [DuckDB](https://duckdb.org/), no servers required!

items = await stacrs.search(
    "../../data/100-sentinel-2-items.parquet",
    datetime="2024-12-01T00:00:00Z/..",
)
data_frame = GeoDataFrame.from_features(items)
data_frame["datetime"] = pandas.to_datetime(data_frame["datetime"])
data_frame[["datetime", "geometry"]]

# %%
# If you know you're going to a [geopandas.GeoDataFrame][] (or something else that speaks
# arrow), you can use the `arrow` optional dependency for **stacrs** (`pip
# install 'stacrs[arrow]'`) and search directly to arrow, which can be more
# efficient than going through JSON dictionaries:

from stacrs import DuckdbClient

client = DuckdbClient()
table = client.search_to_arrow(
    "../../data/100-sentinel-2-items.parquet",
    datetime="2024-12-01T00:00:00Z/..",
)
data_frame = GeoDataFrame.from_arrow(table)
data_frame[["datetime", "geometry"]]
