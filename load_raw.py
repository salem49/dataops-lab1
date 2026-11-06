import duckdb
import sys

WAREHOUSE = "warehouse.duckdb"


def main(path):
    """Extract + Load: copy the raw file into the warehouse."""
    con = duckdb.connect(WAREHOUSE)

    con.execute("CREATE SCHEMA IF NOT EXISTS raw")

    con.execute(
        """
        CREATE OR REPLACE TABLE raw.orders AS
        SELECT
            *,
            row_number() OVER () AS _row_number,
            ? AS _source_file,
            current_timestamp AS _loaded_at
        FROM read_csv_auto(?, all_varchar = true, header = true)
        """,
        [path, path]
    )

    n = con.execute("SELECT count(*) FROM raw.orders").fetchone()[0]

    print(f"Loaded {n} rows from {path} into raw.orders")

    con.close()


if __name__ == "__main__":
    main(sys.argv[1])