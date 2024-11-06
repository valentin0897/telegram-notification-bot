import os
import logging

import sqlite3

from config import Config

def connect_db() -> sqlite3.Connection:
    if Config.DB_PATH:
        db_path = Config.DB_PATH
    else:
        os.makedirs("data", exist_ok=True)
        db_path = "data/users.db"

    try:
        con = sqlite3.connect(db_path)
    except sqlite3.Error as e:
        logging.error(f"Connection to sqlite3 failed: {e.sqlite_errorname}")
        raise ConnectionError(f"Connection to '{db_path}' database failed")

    return con

def execute_sql(cur: sqlite3.Cursor, sql: str, params=None) -> sqlite3.Cursor: 
    try:
        if params is None:
            return cur.execute(sql)
        else:
            return cur.execute(sql, params)
    except sqlite3.Error as e:
        logging.error(f"Error occured while execute query {sql}: {e}")
        raise Exception(e)

def create_db(con: sqlite3.Connection):
    cur = con.cursor()
    sql = "CREATE TABLE IF NOT EXISTS users(user_id, timezone)"
    execute_sql(cur, sql) 

def get_user(con: sqlite3.Connection, user_id: str):
    cur = con.cursor()
    sql = f"SELECT user_id, timezone FROM users WHERE user_id=?"
    res = execute_sql(cur, sql, (user_id,))
    user = res.fetchone()
    return user

def get_timezone_by_user_id(con: sqlite3.Connection, user_id: str):
    cur = con.cursor()
    sql = f"SELECT timezone FROM users WHERE user_id=?"
    res = execute_sql(cur, sql, (user_id,))
    timezone = res.fetchone()
    if timezone:
        return timezone[0]
    else:
        return None

def create_user(con: sqlite3.Connection, user_id: str, timezone: str):
    cur = con.cursor()
    sql = f"INSERT INTO users VALUES (?, ?)"
    execute_sql(cur, sql, (user_id, timezone))

    if cur.rowcount > 0:
        return
    else:
        logging.error("Create user failed")

def update_timezone(con: sqlite3.Connection, user_id: str, timezone: str):
    cur = con.cursor()
    sql = f"UPDATE users SET timezone = ? WHERE user_id=?"
    execute_sql(cur, sql, (timezone, user_id))

    if cur.rowcount > 0:
        return
    else:
        logging.error("Update timzone failed")
