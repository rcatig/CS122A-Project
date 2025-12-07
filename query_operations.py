import csv
from mysql.connector import Error
from db_utils import get_connection, normalize_arg, print_table_rows
from config import NL2SQL_RESULTS_FILE


def list_internet_service(bmid: int):
    try:
        conn = get_connection()
        cur = conn.cursor()

        sql = """
            SELECT s.sid, s.endpoints, s.provider
            FROM InternetService AS s
            JOIN ModelServices AS ms ON s.sid = ms.sid
            WHERE ms.bmid = %s
            ORDER BY s.provider ASC
        """
        cur.execute(sql, (bmid,))
        rows = cur.fetchall()
        print_table_rows(rows)

        cur.close()
        conn.close()
    except Error as e:
        print("Fail")


def count_customized_model(bmids):
    if not bmids:
        return

    ids = [int(b) for b in bmids]
    placeholders = ",".join(["%s"] * len(ids))

    try:
        conn = get_connection()
        cur = conn.cursor()

        sql = f"""
            SELECT b.bmid, b.description, COUNT(c.mid) AS customizedModelCount
            FROM BaseModel AS b
            LEFT JOIN CustomizedModel AS c ON b.bmid = c.bmid
            WHERE b.bmid IN ({placeholders})
            GROUP BY b.bmid, b.description
            ORDER BY b.bmid ASC
        """
        cur.execute(sql, ids)
        rows = cur.fetchall()
        print_table_rows(rows)

        cur.close()
        conn.close()
    except Error as e:
        print("Fail")


def top_n_duration_config(uid: int, N: int):
    try:
        conn = get_connection()
        cur = conn.cursor()

        sql = """
            SELECT c.client_uid, mc.cid, c.labels, c.content, mc.duration
            FROM ModelConfigurations AS mc
            JOIN Configuration AS c ON mc.cid = c.cid
            WHERE c.client_uid = %s
            ORDER BY mc.duration DESC
            LIMIT %s
        """
        cur.execute(sql, (uid, N))
        rows = cur.fetchall()
        print_table_rows(rows)

        cur.close()
        conn.close()
    except Error as e:
        print("Fail")


def list_base_model_keyword(keyword: str):
    try:
        conn = get_connection()
        cur = conn.cursor()

        sql = """
            SELECT DISTINCT b.bmid, s.sid, s.provider, l.domain
            FROM BaseModel AS b
            JOIN ModelServices AS ms ON b.bmid = ms.bmid
            JOIN InternetService AS s ON ms.sid = s.sid
            JOIN LLMService AS l ON s.sid = l.sid
            WHERE l.domain LIKE %s
            ORDER BY b.bmid ASC
            LIMIT 5
        """
        like_pattern = f"%{keyword}%"
        cur.execute(sql, (like_pattern,))
        rows = cur.fetchall()
        print_table_rows(rows)

        cur.close()
        conn.close()
    except Error as e:
        print("Fail")


def print_nl2sql_result():
    try:
        with open(NL2SQL_RESULTS_FILE, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                print(",".join(row))
    except Exception as e:
        print("Fail")

