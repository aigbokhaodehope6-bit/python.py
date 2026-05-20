import re
import time
import json
import sqlite3
from collections import defaultdict, deque
from datetime import datetime, timedelta

# =========================
# CONFIG
# =========================
FAILED_THRESHOLD = 5
TIME_WINDOW_MINUTES = 10
DB_FILE = "soc_events.db"

# in-memory sliding window
failed_attempts = defaultdict(deque)

# =========================
# INIT DATABASE (SIEM STYLE LOGGING)
# =========================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user TEXT,
            ip TEXT,
            event_type TEXT,
            raw_event TEXT
        )
    """)

    conn.commit()
    conn.close()


def store_event(event):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO events (timestamp, user, ip, event_type, raw_event)
        VALUES (?, ?, ?, ?, ?)
    """, (
        event["timestamp"],
        event["user"],
        event["ip"],
        event["event_type"],
        json.dumps(event)
    ))

    conn.commit()
    conn.close()


# =========================
# NORMALIZE EVENT (SIEM FORMAT)
# =========================
def create_event(user, ip, event_type, raw):
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "user": user,
        "ip": ip,
        "event_type": event_type,
        "raw_event": raw
    }


# =========================
# DETECTION ENGINE
# =========================
def process_event(user, ip, raw_line):
    now = datetime.utcnow()
    key = (user, ip)

    failed_attempts[key].append(now)

    # sliding window cleanup
    window_start = now - timedelta(minutes=TIME_WINDOW_MINUTES)

    while failed_attempts[key] and failed_attempts[key][0] < window_start:
        failed_attempts[key].popleft()

    # store event (SIEM logging)
    event = create_event(user, ip, "FAILED_LOGIN", raw_line)
    store_event(event)

    # correlation rule
    if len(failed_attempts[key]) >= FAILED_THRESHOLD:
        trigger_alert(user, ip, len(failed_attempts[key]))


# =========================
# ALERT ENGINE (SOC OUTPUT)
# =========================
def trigger_alert(user, ip, count):
    alert = {
        "timestamp": datetime.utcnow().isoformat(),
        "severity": "HIGH",
        "rule": "Multiple Failed Logins (Possible Brute Force)",
        "user": user,
        "ip": ip,
        "count": count
    }

    print("\n🚨 SECURITY ALERT GENERATED 🚨")
    print(json.dumps(alert, indent=2))

    # also write to file (SOC ticket simulation)
    with open("alerts.log", "a") as f:
        f.write(json.dumps(alert) + "\n")


# =========================
# LINUX LOG PARSER
# =========================
linux_pattern = re.compile(
    r"Failed password for (invalid user )?(?P<user>\w+).* from (?P<ip>\d+\.\d+\.\d+\.\d+)"
)


def parse_linux(line):
    match = linux_pattern.search(line)
    if match:
        user = match.group("user")
        ip = match.group("ip")
        process_event(user, ip, line)


# =========================
# REAL-TIME TAIL (LINUX)
# =========================
def follow(file_path):
    with open(file_path, "r", errors="ignore") as file:
        file.seek(0, 2)

        while True:
            line = file.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line


# =========================
# REPORTING (SOC ANALYTICS)
# =========================
def generate_report():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    print("\n📊 SOC REPORT: Top Attack Sources\n")

    cursor.execute("""
        SELECT ip, COUNT(*) as attempts
        FROM events
        WHERE event_type='FAILED_LOGIN'
        GROUP BY ip
        ORDER BY attempts DESC
        LIMIT 5
    """)

    for row in cursor.fetchall():
        print(f"IP: {row[0]} | Attempts: {row[1]}")

    conn.close()


# =========================
# MAINs
# =========================
if __name__ == "__main__":
    init_db()

    log_file = "auth.log"

    print("[*] SOC Enterprise Monitor Started...\n")

    try:
        for line in follow(log_file):
            parse_linux(line)

    except FileNotFoundError:
        print("[INFO] Log file not found. Running demo mode.")

    finally:
        generate_report()