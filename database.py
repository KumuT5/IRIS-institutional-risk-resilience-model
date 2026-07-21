import sqlite3
import os

# -------------------------------
# DATABASE CONNECTION
# -------------------------------
def get_connection():
    import sqlite3
    import os

    DB_PATH = os.path.join(os.path.dirname(__file__), "risk_management.db")
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------------
# CREATE TABLES
# -------------------------------
def save_risk_config(positive_words, negative_words):
    import sqlite3
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS risk_config (
        id INTEGER PRIMARY KEY,
        positive_words TEXT,
        negative_words TEXT
    )
    """)

    cursor.execute("DELETE FROM risk_config")

    cursor.execute(
        "INSERT INTO risk_config (positive_words, negative_words) VALUES (?, ?)",
        (positive_words, negative_words)
    )

    conn.commit()
    conn.close()


def load_risk_config():
    import sqlite3
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT positive_words, negative_words FROM risk_config")
    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0].split(","), row[1].split(",")
    else:
        return ["good", "great"], ["bad", "error"]

def update_thresholds(low, med, high):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE scoring_config
        SET low_threshold = ?, medium_threshold = ?, high_threshold = ?
        WHERE id = 1
    """, (low, med, high))

    conn.commit()
    conn.close()

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
# --------- RISK CONFIG TABLE ---------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS risk_config (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        positive_words TEXT,
        negative_words TEXT
    )
    """)

    cursor.execute("SELECT COUNT(*) as count FROM risk_config")
    risk_exists = cursor.fetchone()

    if risk_exists["count"] == 0:
        cursor.execute("""
            INSERT INTO risk_config (positive_words, negative_words)
            VALUES ('good,great,excellent', 'bad,error,poor')
        """)


    # --------- ADMIN TABLE (ONLY ONE ADMIN) ---------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scoring_config (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        low_threshold REAL,
        medium_threshold REAL,
        high_threshold REAL
    )
    """)
    cursor.execute("""
    INSERT OR IGNORE INTO scoring_config (id, low_threshold, medium_threshold, high_threshold)
    VALUES (1, 30, 60, 80)
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        username TEXT UNIQUE NOT NULL,
        password BLOB NOT NULL
    );
    """)

    # --------- LOGINS TABLE (MAIN USER TABLE) ---------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT UNIQUE NOT NULL,
        username TEXT UNIQUE NOT NULL,
        email  TEXT UNIQUE NOT NULL,
        password BLOB NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # --------- COMPANY STATS (ADMIN VIEW ONLY) ---------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS company_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login_id INTEGER UNIQUE,
        company_name TEXT NOT NULL,
        usage_count INTEGER DEFAULT 0,
        last_active TIMESTAMP,

        FOREIGN KEY (login_id) REFERENCES logins(id)
    );
    """)

    # --------- ASSESSMENTS TABLE ---------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        login_id INTEGER,
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

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (login_id) REFERENCES logins(id)
    );
    """)

    # --------- SCORES TABLE ---------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assessment_id INTEGER,
        score INTEGER,
        risk_level TEXT,

        FOREIGN KEY (assessment_id) REFERENCES assessments(id)
    );
    """)

    # --------- CONTACT / REVIEWS TABLE ---------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login_id INTEGER,
        company_name TEXT NOT NULL,
        message TEXT NOT NULL,
        type TEXT CHECK(type IN ('review','contact')),

        FOREIGN KEY (login_id) REFERENCES logins(id)
    );
    """)
    
    cursor.execute("SELECT COUNT(*) as count FROM admin")
    result = cursor.fetchone()

    if result["count"] == 0:
        cursor.execute("""
            INSERT INTO admin (id, username, password)
            VALUES (1, 'admin', 'admin123')
        """)

    conn.commit()
    conn.close()


# -------------------------------
# ADMIN REGISTRATION (ONLY ONE)
# -------------------------------

def register_admin(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if admin already exists
    cursor.execute("SELECT COUNT(*) as count FROM admin")
    result = cursor.fetchone()

    if result["count"] > 0:
        conn.close()
        return False  # Admin already exists

    # Insert first and only admin
    cursor.execute("""
        INSERT INTO admin (id, username, password)
        VALUES (1, ?, ?)
    """, (username, password))

    conn.commit()
    conn.close()

    return True

# -------------------------------
# USER REGISTRATION
# -------------------------------

def register_user(company_name, username,email, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO logins (company_name, username,email, password)
            VALUES (?, ?, ?,?)
        """, (company_name, username,email, password))

        login_id = cursor.lastrowid

        # Create company stats entry
        cursor.execute("""
            INSERT INTO company_stats (login_id, company_name)
            VALUES (?, ?)
        """, (login_id, company_name))

        conn.commit()
        return "User registered successfully"

    except sqlite3.IntegrityError:
        return "Company or Username already exists"

    finally:
        conn.close()


# -------------------------------
# LOGIN FUNCTIONS
# -------------------------------

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM logins
        WHERE username = ?  AND password = ? 
    """, (username, password))

    user = cursor.fetchone()
    conn.close()

    return user


def login_admin(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM admin LIMIT 1")
    admin = cursor.fetchone()

    conn.close()

    if admin and admin["username"] == username and admin["password"] == password:
        return admin

    return None

def admin_exists():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as count FROM admin")
    result = cursor.fetchone()

    conn.close()
    return result["count"] > 0

# -------------------------------
# TRACK USER ACTIVITY
# -------------------------------

def update_usage(login_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE company_stats
        SET usage_count = usage_count + 1,
            last_active = CURRENT_TIMESTAMP
        WHERE login_id = ?
    """, (login_id,))

    conn.commit()
    conn.close()


# -------------------------------
# INSERT ASSESSMENT
# -------------------------------

def insert_assessment(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO assessments (
        login_id, username, company_name, sector,
        breaches, patch_delay, firewall_score,
        training_hours, turnover_rate, policy_violations,
        debt_ratio, revenue_decline, reserve_months,
        audit_findings, compliance_issues, board_meetings,
        digital_score, human_score, financial_score, governance_score,
        overall_score, assessment_date, risk_level
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()


# -------------------------------
# GET USER HISTORY (ISOLATED)
# -------------------------------

def get_user_history(login_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM assessments
        WHERE login_id = ?
        ORDER BY created_at DESC
    """, (login_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows


# -------------------------------
# GET PREVIOUS SCORE (TREND)
# -------------------------------

def get_previous_score(login_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT overall_score
        FROM assessments
        WHERE login_id = ?
        ORDER BY created_at DESC
        LIMIT 1 OFFSET 1
    """, (login_id,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return result["overall_score"]
    return None


# -------------------------------
# STORE MESSAGE / REVIEW
# -------------------------------

def insert_message(login_id, company_name, message, msg_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages (login_id, company_name, message, type)
        VALUES (?, ?, ?, ?)
    """, (login_id, company_name, message, msg_type))

    conn.commit()
    conn.close()


# -------------------------------
# ADMIN FUNCTIONS
# -------------------------------
def get_all_company_stats():
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT 
        l.id AS company_id,
        l.company_name AS company_name,

        COUNT(DISTINCT a.id) AS usage_count,

        GROUP_CONCAT(m.message, ' || ') AS reviews

    FROM logins l

    LEFT JOIN assessments a 
        ON l.id = a.login_id

    LEFT JOIN messages m 
        ON l.id = m.login_id
        AND m.type = 'review'

    GROUP BY l.id
    """)
    rows = cursor.fetchall()
    result = []

    for row in rows:
        result.append({
            "company_id": row["company_id"],
            "company_name": row["company_name"],
            "usage_count": row["usage_count"] or 0,
            "reviews": row["reviews"] or ""
        })

    return result

    

def get_all_messages():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT company_name, message, type
        FROM messages
        ORDER BY id DESC
    """)

    data = cursor.fetchall()
    conn.close()
    return data


def save_contact_message(company_name, message, msg_type="contact"):

    conn = get_connection()
    cursor = conn.cursor()

    # FIND MATCHING COMPANY
    cursor.execute(
        "SELECT id FROM logins WHERE LOWER(company_name)=LOWER(?)",
        (company_name,)
    )

    row = cursor.fetchone()

    login_id = row["id"] if row else None

    cursor.execute("""
        INSERT INTO messages (
            login_id,
            company_name,
            message,
            type
        )
        VALUES (?, ?, ?, ?)
    """, (
        login_id,
        company_name,
        message,
        msg_type
    ))

    conn.commit()
    conn.close()


def get_all_messages():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT company_name, message, type
        FROM messages
        ORDER BY id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    return data
