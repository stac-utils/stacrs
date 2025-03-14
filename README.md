# stacrs

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/stac-utils/stacrs/ci.yaml?branch=main&style=for-the-badge)](https://github.com/stac-utils/stacrs/actions/workflows/ci.yaml)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/stac-utils/stacrs/docs.yaml?branch=main&style=for-the-badge&label=Docs)](https://stac-utils.github.io/stacrs/latest/)
[![PyPI - Version](https://img.shields.io/pypi/v/stacrs?style=for-the-badge)](https://pypi.org/project/stacrs)
[![Conda Downloads](https://img.shields.io/conda/d/conda-forge/stacrs?style=for-the-badge)](https://anaconda.org/conda-forge/stacrs)
![PyPI - License](https://img.shields.io/pypi/l/stacrs?style=for-the-badge)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg?style=for-the-badge)](./CODE_OF_CONDUCT)

A Python package for [STAC](https://stacspec.org/) using Rust under the hood.

## Why?

Q: We already have [PySTAC](https://github.com/stac-utils/pystac), so why **stacrs**?

A: **stacrs** can

- Read, write, and search [stac-geoparquet](https://github.com/stac-utils/stac-geoparquet)
- Go to and from [arrow](https://arrow.apache.org/) tables, allowing easy interoperability with (e.g.) [GeoPandas](https://geopandas.org/en/stable/)
- `async`

If you don't need those things, **stacrs** probably isn't for you — use **pystac** and its friend, [pystac-client](https://github.com/stac-utils/pystac-client).

## Usage

Install via **pip**:

```shell
# basic
python -m pip install stacrs

# support arrow tables
python -m pip install 'stacrs[arrow]'
```

Or via **conda**:

```shell
conda install conda-forge::stacrs
```

Then:

```python exec="on" source="above"
import asyncio
import stacrs

async def main() -> None:
    # Search a STAC API
    items = await stacrs.search(
        "https://landsatlook.usgs.gov/stac-server",
        collections="landsat-c2l2-sr",
        intersects={"type": "Point", "coordinates": [-105.119, 40.173]},
        sortby="-properties.datetime",
        max_items=100,
    )

    # If you installed with `pystac[arrow]`:
    from geopandas import GeoDataFrame

    table = stacrs.to_arrow(items)
    data_frame = GeoDataFrame.from_arrow(table)
    items = stacrs.from_arrow(data_frame.to_arrow())

    # Write items to a stac-geoparquet file
    await stacrs.write("/tmp/items.parquet", items)

    # Read items from a stac-geoparquet file as an item collection
    item_collection = await stacrs.read("/tmp/items.parquet")

    # Use `search_to` for better performance if you know you'll be writing the items
    # to a file
    await stacrs.search_to(
        "/tmp/items.parquet",
        "https://landsatlook.usgs.gov/stac-server",
        collections="landsat-c2l2-sr",
        intersects={"type": "Point", "coordinates": [-105.119, 40.173]},
        sortby="-properties.datetime",
        max_items=100,
    )

asyncio.run(main())
```

See [the documentation](https://stac-utils.github.io/stacrs) for details.
In particular, our [examples](https://stac-utils.github.io/stacrs/latest/examples/) demonstrate some of the more interesting features.

## CLI

**stacrs** comes with a CLI:

```bash exec="on" source="above" result="text"
stacrs -h
```

> [!NOTE]
> Before **stacrs** v0.5.4, the CLI was its own PyPI package named **stacrs-cli**, which is no longer needed.

## stac-geoparquet

**stacrs** replicates much of the behavior in the [stac-geoparquet](https://github.com/stac-utils/stac-geoparquet) library, and even uses some of the same Rust dependencies.
We believe there are a couple of issues with **stac-geoparquet** that make **stacrs** a worthy replacement:

- The **stac-geoparquet** repo includes Python dependencies
- It doesn't have a nice one-shot API for reading and writing
- It includes some leftover code and logic from its genesis as a tool for the [Microsoft Planetary Computer](https://planetarycomputer.microsoft.com/)

We test to ensure [compatibility](https://github.com/stac-utils/stac-rs/blob/main/scripts/validate-stac-geoparquet) between the two libraries, and we intend to consolidate to a single "stac-geoparquet" library at some point in the future.

## Development

Get [Rust](https://rustup.rs/), [uv](https://docs.astral.sh/uv/getting-started/installation/), and (optionally) [libduckdb](https://duckdb.org/docs/installation/index).
Then:

```shell
git clone git@github.com:stac-utils/stacrs.git
cd stacrs
scripts/test
```

See [CONTRIBUTING.md](./CONTRIBUTING.md) for more information about contributing to this project.

### DuckDB

By default, this package expects **libduckdb** to be present on your system.
If you get this sort of error when building:

```shell
  = note: ld: library 'duckdb' not found
```

Set your `DUCKDB_LIB_DIR` to point to your **libduckdb**.
If you're using [homebrew](https://brew.sh/), that might look like this:

```shell
export DUCKDB_LIB_DIR=/opt/homebrew/lib
```

Alternatively, you can use the `duckdb-bundled` feature to build DuckDB bindings into the Rust library:

```shell
maturin dev --uv -F duckdb-bundled && pytest
```

> [!WARNING]
> Building DuckDB [bundled](https://github.com/duckdb/duckdb-rs?tab=readme-ov-file#notes-on-building-duckdb-and-libduckdb-sys) takes a long while.

## License

**stacrs** is dual-licensed under both the MIT license and the Apache license (Version 2.0).
See [LICENSE-APACHE](./LICENSE-APACHE) and [LICENSE-MIT](./LICENSE-MIT) for details.
