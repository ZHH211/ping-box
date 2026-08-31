import sqlite3
from datetime import datetime

import config


def connect():
    conn = sqlite3.connect(config.SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_id INTEGER,
            ok INTEGER NOT NULL,
            status TEXT,
            ms INTEGER,
            msg TEXT,
            created_at TEXT NOT NULL
        );
        """
    )
    conn.commit()
    cur = conn.execute("SELECT COUNT(*) AS n FROM targets")
    if cur.fetchone()["n"] == 0:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn.execute(
            "INSERT INTO targets (name, url, created_at) VALUES (?,?,?)",
            ("示例：百度", "https://www.baidu.com", now),
        )
        conn.commit()
    conn.close()


def list_targets():
    conn = connect()
    rows = conn.execute("SELECT * FROM targets ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_target(name, url):
    conn = connect()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    cur = conn.execute(
        "INSERT INTO targets (name, url, created_at) VALUES (?,?,?)",
        (name, url, now),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def delete_target(target_id):
    conn = connect()
    conn.execute("DELETE FROM targets WHERE id=?", (target_id,))
    conn.commit()
    conn.close()


def add_log(target_id, ok, status, ms, msg):
    conn = connect()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "INSERT INTO logs (target_id, ok, status, ms, msg, created_at) VALUES (?,?,?,?,?,?)",
        (target_id, 1 if ok else 0, str(status) if status is not None else "", int(ms), msg, now),
    )
    conn.commit()
    conn.close()


def recent_logs(limit=20):
    conn = connect()
    rows = conn.execute(
        """
        SELECT logs.*, targets.name, targets.url
        FROM logs LEFT JOIN targets ON targets.id = logs.target_id
        ORDER BY logs.id DESC LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
