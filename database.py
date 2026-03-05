import sqlite3
import os

# -------------------------------
# DATABASE CONNECTION
# -------------------------------

def get_connection():
    DB_PATH = os.path.join(os.path.dirname(__file__), "risk_management.db") 
    conn = sqlite3.connect("risk_management.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------------
# CREATE TABLES
# -------------------------------

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # -------- LOGINS TABLE --------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS LOGINS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # -------- ASSESSMENTS TABLE --------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,
        company_name TEXT,
        sector TEXT,

        breaches INTEGER,
        patch_delay INTEGER,
        firewall_score INTEGER,

        training_hours INTEGER,
        turnover_rate REAL,
        policy_violations INTEGER,

        debt_ratio REAL,
        revenue_decline REAL,
        reserve_months INTEGER,

        audit_findings INTEGER,
        compliance_issues INTEGER,
        board_meetings INTEGER,

        digital_score REAL,
        human_score REAL,
        financial_score REAL,
        governance_score REAL,
        overall_score REAL,
        assessment_date TEXT,
        risk_level TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


# -------------------------------
# USER REGISTRATION
# -------------------------------

def register_user(company_name, username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO logins (company_name, username, password)
        VALUES (?, ?, ?)
    """, (company_name, username, password))

    conn.commit()
    conn.close()


# -------------------------------
# USER LOGIN VALIDATION
# -------------------------------

def validate_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM LOGINS
        WHERE username = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()
    conn.close()
    return user


# -------------------------------
# INSERT NEW ASSESSMENT
# -------------------------------

def insert_assessment(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO assessments (
        username, company_name, sector,
        breaches, patch_delay, firewall_score,
        training_hours, turnover_rate, policy_violations,
        debt_ratio, revenue_decline, reserve_months,
        audit_findings, compliance_issues, board_meetings,
        digital_score, human_score, financial_score, governance_score,
        overall_score, risk_level
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()


# -------------------------------
# GET PREVIOUS SCORE (TREND)
# -------------------------------

def get_previous_score(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT overall_score
        FROM assessments
        WHERE username = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (company_name,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return result["overall_score"]
    return None


# -------------------------------
# GET USER HISTORY (ISOLATED)
# -------------------------------

def get_user_history(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM assessments
        WHERE username = ?
        ORDER BY created_at DESC
    """, (username,))

    rows = cursor.fetchall()
    conn.close()
    return rows