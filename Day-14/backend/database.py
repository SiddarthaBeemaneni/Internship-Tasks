"""
database.py
SQLite persistence layer for TicketSense.
Handles schema creation and all read/write queries used by app.py.
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ticketsense.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create tables if they don't already exist."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_ref TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            customer_name TEXT,
            customer_email TEXT,
            subject TEXT NOT NULL,
            body TEXT NOT NULL,
            language TEXT,
            predicted_queue TEXT,
            predicted_priority TEXT,
            predicted_type TEXT,
            status TEXT DEFAULT 'open',
            created_at TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # --- migration: older DB files created before tickets had a user_id column.
    # Without this, upgrading in place would leave a table Flask can't insert into.
    existing_cols = {row["name"] for row in cur.execute("PRAGMA table_info(tickets)").fetchall()}
    if "user_id" not in existing_cols:
        cur.execute("ALTER TABLE tickets ADD COLUMN user_id INTEGER")
        # Old rows have no owner and predate per-account isolation; they're not
        # attributable to any single account, so we drop them rather than
        # guess an owner (which would just recreate the original bug).
        cur.execute("DELETE FROM tickets WHERE user_id IS NULL")

    conn.commit()
    conn.close()


def insert_ticket(ticket_ref, user_id, customer_name, customer_email, subject, body,
                   language, predicted_queue, predicted_priority, predicted_type):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tickets (ticket_ref, user_id, customer_name, customer_email, subject, body,
                              language, predicted_queue, predicted_priority, predicted_type,
                              status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'open', ?)
    """, (ticket_ref, user_id, customer_name, customer_email, subject, body, language,
          predicted_queue, predicted_priority, predicted_type,
          datetime.utcnow().isoformat()))
    conn.commit()
    ticket_id = cur.lastrowid
    conn.close()
    return ticket_id


def get_all_tickets(user_id, status=None, queue=None, priority=None, search=None):
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT * FROM tickets WHERE user_id = ?"
    params = [user_id]
    if status and status != "all":
        query += " AND status = ?"
        params.append(status)
    if queue and queue != "all":
        query += " AND predicted_queue = ?"
        params.append(queue)
    if priority and priority != "all":
        query += " AND predicted_priority = ?"
        params.append(priority)
    if search:
        query += " AND (subject LIKE ? OR body LIKE ? OR ticket_ref LIKE ?)"
        like = f"%{search}%"
        params.extend([like, like, like])
    query += " ORDER BY created_at DESC"
    cur.execute(query, params)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def get_ticket_by_ref(ticket_ref, user_id=None):
    conn = get_connection()
    cur = conn.cursor()
    if user_id is None:
        cur.execute("SELECT * FROM tickets WHERE ticket_ref = ?", (ticket_ref,))
    else:
        cur.execute("SELECT * FROM tickets WHERE ticket_ref = ? AND user_id = ?", (ticket_ref, user_id))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def update_ticket_status(ticket_ref, user_id, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE tickets SET status = ? WHERE ticket_ref = ? AND user_id = ?",
        (status, ticket_ref, user_id),
    )
    conn.commit()
    changed = cur.rowcount
    conn.close()
    return changed > 0


def get_stats(user_id):
    conn = get_connection()
    cur = conn.cursor()
    stats = {}

    cur.execute("SELECT COUNT(*) AS c FROM tickets WHERE user_id = ?", (user_id,))
    stats["total"] = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) AS c FROM tickets WHERE user_id = ? AND status = 'open'", (user_id,))
    stats["open"] = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) AS c FROM tickets WHERE user_id = ? AND status = 'resolved'", (user_id,))
    stats["resolved"] = cur.fetchone()["c"]

    cur.execute(
        "SELECT predicted_priority AS k, COUNT(*) AS c FROM tickets WHERE user_id = ? GROUP BY predicted_priority",
        (user_id,),
    )
    stats["by_priority"] = {r["k"]: r["c"] for r in cur.fetchall() if r["k"]}

    cur.execute(
        "SELECT predicted_queue AS k, COUNT(*) AS c FROM tickets WHERE user_id = ? GROUP BY predicted_queue ORDER BY c DESC",
        (user_id,),
    )
    stats["by_queue"] = {r["k"]: r["c"] for r in cur.fetchall() if r["k"]}

    cur.execute(
        "SELECT language AS k, COUNT(*) AS c FROM tickets WHERE user_id = ? GROUP BY language",
        (user_id,),
    )
    stats["by_language"] = {r["k"]: r["c"] for r in cur.fetchall() if r["k"]}

    conn.close()
    return stats


def create_user(name, email, password_hash):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (name, email, password_hash, created_at)
        VALUES (?, ?, ?, ?)
    """, (name, email.lower(), password_hash, datetime.utcnow().isoformat()))
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id


def get_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email.lower(),))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def insert_contact_message(name, email, message):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO contact_messages (name, email, message, created_at)
        VALUES (?, ?, ?, ?)
    """, (name, email, message, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
