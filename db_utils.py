import mysql.connector
from config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def print_bool(ok: bool):
    print(True if ok else False)


def normalize_arg(arg: str):
    return None if arg == "NULL" else arg


def execute_ddl_from_file(conn, ddl_path: str):
    with open(ddl_path, "r", encoding="utf-8") as f:
        sql_text = f.read()
    cursor = conn.cursor()
    for statement in sql_text.split(";"):
        stmt = statement.strip()
        if stmt:
            cursor.execute(stmt)
    cursor.close()


def print_table_rows(rows):
    for row in rows:
        printable = ["NULL" if v is None else str(v) for v in row]
        print(",".join(printable))

