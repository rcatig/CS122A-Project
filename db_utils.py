"""
Database utility functions for the CS122A Project
"""

import mysql.connector
from config import DB_CONFIG


def get_connection():
    """Create a new MySQL connection using DB_CONFIG."""
    return mysql.connector.connect(**DB_CONFIG)


def print_bool(ok: bool):
    """Print boolean result as required."""
    print(True if ok else False)


def normalize_arg(arg: str):
    """Convert 'NULL' to None, leave everything else as-is."""
    return None if arg == "NULL" else arg


def execute_ddl_from_file(conn, ddl_path: str):
    """Execute all statements from a .sql file, splitting on ';'."""
    with open(ddl_path, "r", encoding="utf-8") as f:
        sql_text = f.read()
    cursor = conn.cursor()
    for statement in sql_text.split(";"):
        stmt = statement.strip()
        if stmt:
            cursor.execute(stmt)
    cursor.close()


def print_table_rows(rows):
    """Print rows as comma-separated values, one line per row."""
    for row in rows:
        # Convert None to 'NULL' for printing (optional; spec doesn't forbid)
        printable = ["NULL" if v is None else str(v) for v in row]
        print(",".join(printable))

