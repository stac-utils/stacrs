# type: ignore
"""
# Reading and plotting
"""

# %%
# Reading is done via a top-level async function.
import stacrs

items = await stacrs.read("https://github.com/stac-utils/stacrs/raw/refs/heads/main/data/100-sentinel-2-items.parquet")
items

# %%
# Let's take a look some of the attributes of the STAC items.
import pandas
from geopandas import GeoDataFrame

data_frame = GeoDataFrame.from_features(items)
data_frame["datetime"] = pandas.to_datetime(data_frame["datetime"])
data_frame[["geometry", "datetime", "s2:snow_ice_percentage"]]

# %%
# How does the snow and ice percentage vary over the year?
from matplotlib.dates import DateFormatter

axis = data_frame.plot(x="datetime", y="s2:snow_ice_percentage", kind="scatter")
axis.xaxis.set_major_formatter(DateFormatter("%b"))
