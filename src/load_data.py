import argparse
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from parse_data import parse_all


CORE_TABLE_ORDER = [
    "competitions",
    "seasons",
    "countries",
    "teams",
    "managers",
    "players",
    "matches",
    "team_managers",
    "lineups",
    "player_positions",
    "cards",
]


# Events must be loaded before the subtype tables because
# passes, shots, carries, dribbles, and duels reference events.
EVENT_TABLE_ORDER = [
    "events",
    "passes",
    "shots",
    "carries",
    "dribbles",
    "duels",
]


def get_table_row_count(engine, table_name):
    """Return the current number of rows in a MySQL table."""

    query = text(f"SELECT COUNT(*) FROM `{table_name}`")
    with engine.connect() as connection:
        return connection.execute(query).scalar_one()


def ensure_table_is_empty(engine, table_name):
    """
    Prevent the loader from accidentally inserting the same data twice.
    """
    row_count = get_table_row_count(engine, table_name)
    if row_count > 0:
        raise RuntimeError(f"Table '{table_name}' already contains "
            f"{row_count:,} rows.")


def load_dataframe(dataframe, table_name, engine, chunksize):
    """Load one DataFrame into an existing MySQL table."""

    if dataframe.empty:
        print(f"{table_name}: no rows to load")
        return 0

    dataframe.to_sql(name=table_name, con=engine, if_exists="append", index=False, chunksize=chunksize)

    loaded_rows = len(dataframe)

    print(f"{table_name}: loaded {loaded_rows:,} rows")

    return loaded_rows


def load_core_tables(raw_data_dir, engine, chunksize):
    """
    Parse and load the smaller core datasets
    """

    print("\nParsing core data files...")
    tables = parse_all(raw_data_dir)
    print("Core files parsed successfully.\n")

    expected_counts = {}

    for table_name in CORE_TABLE_ORDER:
        ensure_table_is_empty(engine, table_name)
        dataframe = tables[table_name]
        expected_counts[table_name] = load_dataframe(dataframe=dataframe, table_name=table_name, engine=engine, chunksize=chunksize)

    return expected_counts


def load_parquet_table(parquet_dir, table_name, engine, chunksize):
    """
    Load all Parquet batches belonging to one event table.
    """

    parquet_files = sorted(parquet_dir.glob(f"{table_name}_*.parquet"))

    if not parquet_files:
        raise FileNotFoundError(f"No Parquet files found for '{table_name}' in " f"{parquet_dir.resolve()}")

    ensure_table_is_empty(engine, table_name)

    total_loaded = 0

    for parquet_file in parquet_files:
        dataframe = pd.read_parquet(parquet_file)
        dataframe.to_sql(name=table_name, con=engine, if_exists="append", index=False, chunksize=chunksize)
        batch_rows = len(dataframe)
        total_loaded += batch_rows

        print(f"{table_name}: {parquet_file.name} — " f"{batch_rows:,} rows loaded")

        # The next batch can be read without retaining this one.
        del dataframe

    print(f"{table_name}: {total_loaded:,} total rows loaded\n")

    return total_loaded


def load_event_tables(parquet_dir, engine, chunksize):
    """Load events first, followed by every event subtype table."""

    expected_counts = {}

    for table_name in EVENT_TABLE_ORDER:
        expected_counts[table_name] = load_parquet_table(parquet_dir=parquet_dir, table_name=table_name, engine=engine, chunksize=chunksize)

    return expected_counts


def verify_row_counts(engine, expected_counts):
    """
    Compare each source row count with its final MySQL row count.
    """

    print("\nVerifying loaded row counts...\n")

    mismatches = []

    for table_name, expected_rows in expected_counts.items():
        database_rows = get_table_row_count(engine, table_name)

        if database_rows == expected_rows:
            status = "OK"
        else:
            status = "MISMATCH"
            mismatches.append(table_name)

        print(f"{table_name}: " f"source={expected_rows:,}, " f"database={database_rows:,}, " f"status={status}")

    if mismatches:
        raise RuntimeError("Row-count verification failed for: " + ", ".join(mismatches))

    print("\nAll source and database row counts match.")


def main():
    parser = argparse.ArgumentParser(description="Load football data into MySQL")

    parser.add_argument("--raw-data-dir", required=True, help=("Path containing competitions.json, matches/, and lineups/"))
    parser.add_argument("--parquet-dir", required=True, help=("Path containing events_*.parquet, passes_*.parquet, shots_*.parquet, etc."))
    parser.add_argument("--database-url", default=os.getenv("DATABASE_URL"), help=("SQLAlchemy MySQL connection URL. This can also be supplied through the DATABASE_URL environment variable."))
    parser.add_argument("--chunksize", type=int, default=5000, help="Number of rows loaded into MySQL at a time")

    args = parser.parse_args()

    if not args.database_url:
        raise ValueError("Provide --database-url or set the DATABASE_URL environment variable.")

    if args.chunksize <= 0:
        raise ValueError("--chunksize must be greater than zero.")

    raw_data_dir = Path(args.raw_data_dir)
    parquet_dir = Path(args.parquet_dir)

    if not raw_data_dir.is_dir():
        raise FileNotFoundError(f"Raw data directory not found: {raw_data_dir.resolve()}")

    if not parquet_dir.is_dir():
        raise FileNotFoundError(f"Parquet directory not found: {parquet_dir.resolve()}")

    engine = create_engine(args.database_url, pool_pre_ping=True)

    try:
        core_counts = load_core_tables(raw_data_dir=raw_data_dir, engine=engine, chunksize=args.chunksize)
        event_counts = load_event_tables(parquet_dir=parquet_dir, engine=engine, chunksize=args.chunksize)

        expected_counts = {**core_counts, **event_counts}
        verify_row_counts(engine=engine, expected_counts=expected_counts)

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
