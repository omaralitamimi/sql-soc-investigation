"""Build and query a tiny SQLite authentication dataset for SOC practice."""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

SCHEMA = """CREATE TABLE events(timestamp TEXT, username TEXT, source_ip TEXT, result TEXT, asset TEXT);"""


def build(database: Path, events: list[dict]) -> None:
    with sqlite3.connect(database) as connection:
        connection.executescript("DROP TABLE IF EXISTS events;" + SCHEMA)
        connection.executemany("INSERT INTO events VALUES (:timestamp,:username,:source_ip,:result,:asset)", events)


def suspicious(database: Path, threshold: int = 3) -> list[dict]:
    query = """SELECT source_ip, COUNT(*) AS failures, COUNT(DISTINCT username) AS targeted_users
               FROM events WHERE result='failure' GROUP BY source_ip
               HAVING COUNT(*) >= ? ORDER BY failures DESC, source_ip"""
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        return [dict(row) for row in connection.execute(query, (threshold,))]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("events", type=Path)
    parser.add_argument("--database", type=Path, default=Path("soc_lab.db"))
    parser.add_argument("--threshold", type=int, default=3)
    args = parser.parse_args()
    build(args.database, json.loads(args.events.read_text(encoding="utf-8")))
    print(json.dumps(suspicious(args.database, args.threshold), indent=2))


if __name__ == "__main__":
    main()
