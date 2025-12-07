"""
Data operations (insert, delete, update) for the CS122A Project
"""

import sys
import os
import csv
from mysql.connector import Error
from db_utils import get_connection, normalize_arg, execute_ddl_from_file
from config import DDL_FILE


def import_data(folder_name: str) -> bool:
    """
    Q1: Import data from CSV files
    1. Run ddl.sql to recreate all tables.
    2. For each CSV in folder_name:
       - Use the first row as header (column names)
       - Insert remaining rows as data
    """
    conn = None
    try:
        conn = get_connection()
        conn.start_transaction()

        # 1) Rebuild schema
        execute_ddl_from_file(conn, DDL_FILE)

        cursor = conn.cursor()

        folder_path = os.path.abspath(folder_name)

        # Map table name -> csv path
        csv_files = {}
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".csv"):
                table_name = os.path.splitext(filename)[0]
                csv_files[table_name] = os.path.join(folder_path, filename)

        # Explicit import order to satisfy foreign keys
        import_order = [
            "User",
            "AgentCreator",
            "AgentClient",
            "BaseModel",
            "CustomizedModel",
            "Configuration",
            "InternetService",
            "LLMService",
            "DataStorage",
            "ModelServices",
            "ModelConfigurations",
        ]

        for table_name in import_order:
            if table_name not in csv_files:
                continue  # no CSV for this table in the folder

            csv_path = csv_files[table_name]

            with open(csv_path, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)

                # First row is header (column names)
                header = next(reader, None)
                if header is None:
                    continue  # empty file

                rows = list(reader)
                if not rows:
                    continue  # no data rows

            col_list = ", ".join(f"`{c}`" for c in header)
            placeholders = ", ".join(["%s"] * len(header))
            insert_sql = f"INSERT INTO `{table_name}` ({col_list}) VALUES ({placeholders})"

            cursor.executemany(insert_sql, rows)

        conn.commit()
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print("ERROR in import_data:", e)
        if conn is not None:
            try:
                conn.rollback()
                conn.close()
            except Exception:
                pass
        return False


def insert_agent_client(args) -> bool:
    """
    Q2: Insert Agent Client
    python3 main.py insertAgentClient [uid:int] [username:str] [email:str]
        [card_number:int] [card_holder:str] [expiration_date:date]
        [cvv:int] [zip:int] [interests:str]
    """
    if len(args) != 9:
        return False

    uid = int(args[0])
    username = normalize_arg(args[1])
    email = normalize_arg(args[2])
    card_number = int(args[3])
    card_holder = normalize_arg(args[4])
    expiration_date = normalize_arg(args[5])  # 'YYYY-MM-DD' string
    cvv = int(args[6])
    zip_code = int(args[7])
    interests = normalize_arg(args[8])

    try:
        conn = get_connection()
        conn.start_transaction()
        cur = conn.cursor()

        # Insert into User table
        cur.execute(
            "INSERT INTO User (uid, username, email) VALUES (%s, %s, %s)",
            (uid, username, email)
        )

        # Insert into AgentClient table (includes payment info)
        cur.execute(
            "INSERT INTO AgentClient (uid, interests, cardholder, expire, cardno, cvv, zip) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (uid, interests, card_holder, expiration_date, card_number, cvv, zip_code)
        )

        conn.commit()
        cur.close()
        conn.close()
        return True
    except Error as e:
        print("ERROR in insertAgentClient:", e, file=sys.stderr)
        try:
            conn.rollback()
        except Exception:
            pass
        return False


def add_customized_model(mid: int, bmid: int) -> bool:
    """
    Q3: Add Customized Model
    python3 main.py addCustomizedModel [mid:int] [bmid:int]
    """
    try:
        conn = get_connection()
        conn.start_transaction()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO CustomizedModel (MID, BMID) VALUES (%s, %s)",
            (mid, bmid)
        )

        conn.commit()
        cur.close()
        conn.close()
        return True
    except Error as e:
        print("ERROR in addCustomizedModel:", e, file=sys.stderr)
        try:
            conn.rollback()
        except Exception:
            pass
        return False


def delete_base_model(bmid: int) -> bool:
    """
    Q4: Delete Base Model
    python3 main.py deleteBaseModel [bmid:int]
    """
    try:
        conn = get_connection()
        conn.start_transaction()
        cur = conn.cursor()

        # Assumes ON DELETE CASCADE or foreign keys are satisfied
        cur.execute("DELETE FROM BaseModel WHERE BMID = %s", (bmid,))

        conn.commit()
        cur.close()
        conn.close()
        # check rowcount?
        return cur.rowcount > 0
    except Error as e:
        print("ERROR in deleteBaseModel:", e, file=sys.stderr)
        try:
            conn.rollback()
        except Exception:
            pass
        return False

