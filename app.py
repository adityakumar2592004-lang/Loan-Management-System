# pyrefly: ignore[missing-import]
from dotenv import load_dotenv
import os
from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
import psycopg2

load_dotenv()

app = Flask(__name__)
CORS(app)


# =====================================
# 1. POSTGRESQL DATABASE CONNECTION
# =====================================

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="Financial_DB",
        user="postgres",
        password=os.getenv("DATABASE_PASSWORD")
    )


# =====================================
# 2. HOME ROUTE
# =====================================

@app.route("/")
def home():
    return send_file("dashboard.html")


@app.route("/<path:filename>")
def serve_files(filename):
    return send_from_directory(".", filename)


# =====================================
# 3. DATABASE CONNECTION TEST API
# =====================================

@app.route("/api/db-test")
def db_test():
    connection = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM customers;")
        total_customers = cursor.fetchone()[0]

        cursor.close()

        return jsonify({
            "message": "PostgreSQL connected successfully!",
            "total_customers": total_customers,
            "status": "Success"
        })

    except Exception as error:
        return jsonify({
            "message": "Database connection failed",
            "error": str(error),
            "status": "Error"
        }), 500

    finally:
        if connection:
            connection.close()


# =====================================
# 4. DASHBOARD API
# =====================================

@app.route("/api/dashboard")
def dashboard():
    connection = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM customers;")
        total_customers = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM applications;")
        total_applications = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM applications
            WHERE status = 'Approved';
        """)
        approved_loans = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM applications
            WHERE status = 'Pending';
        """)
        pending_loans = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(SUM(loan_amount), 0)
            FROM applications;
        """)
        total_loan_amount = float(cursor.fetchone()[0])

        cursor.close()

        return jsonify({
            "total_customers": total_customers,
            "total_applications": total_applications,
            "approved_loans": approved_loans,
            "pending_loans": pending_loans,
            "total_loan_amount": total_loan_amount
        })

    except Exception as error:
        return jsonify({
            "message": "Dashboard data fetch failed",
            "error": str(error)
        }), 500

    finally:
        if connection:
            connection.close()


@app.route("/api/recent-applications")
def recent_applications():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT a.application_id, c.full_name,
               c.pan_number, a.loan_amount,
               a.loan_type, a.application_date, a.status
        FROM applications a
        JOIN customers c
        ON a.customer_id = c.customer_id
        ORDER BY a.application_id DESC
        LIMIT 10
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    applications = []

    for row in rows:
        applications.append({
            "application_id": row[0],
            "customer_name": row[1],
            "pan_number": row[2],
            "loan_amount": float(row[3]),
            "loan_type": row[4],
            "application_date": str(row[5]),
            "status": row[6]
        })

    return jsonify(applications)

@app.route("/api/customers")
def get_customers():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT full_name, phone, email, pan_number
        FROM customers
        ORDER BY customer_id DESC
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    customers = []

    for row in rows:
        customers.append({
            "name": row[0],
            "phone": row[1],
            "email": row[2],
            "pan_number": row[3]
        })

    return jsonify(customers)


# =====================================
# 5. ADD LOAN APPLICATION API
# =====================================

@app.route("/api/applications", methods=["POST"])
def add_application():
    connection = None

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No application data received"}), 400

        name = data["customer_name"].strip()
        phone = data["phone"].strip()
        email = data["email"].strip().lower()
        pan = data["pan_number"].strip().upper()
        amount = float(data["loan_amount"])
        loan_type = data["loan_type"].strip()

        if not all([name, phone, email, pan, loan_type]) or amount <= 0:
            return jsonify({"error": "Invalid application details"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        # Find existing customer using PAN
        cursor.execute("""
            SELECT customer_id
            FROM customers
            WHERE UPPER(pan_number) = %s;
        """, (pan,))

        customer = cursor.fetchone()

        if customer:
            customer_id = customer[0]

            # Update existing customer details
            cursor.execute("""
                UPDATE customers
                SET full_name = %s, phone = %s, email = %s
                WHERE customer_id = %s;
            """, (name, phone, email, customer_id))

        else:
            # Create new customer
            cursor.execute("""
                INSERT INTO customers
                (full_name, phone, email, pan_number)
                VALUES (%s, %s, %s, %s)
                RETURNING customer_id;
            """, (name, phone, email, pan))

            customer_id = cursor.fetchone()[0]

        # Create loan application
        cursor.execute("""
            INSERT INTO applications
            (customer_id, loan_amount, loan_type, status)
            VALUES (%s, %s, %s, 'Pending')
            RETURNING application_id;
        """, (customer_id, amount, loan_type))

        application_id = cursor.fetchone()[0]

        connection.commit()
        cursor.close()

        return jsonify({
            "message": "Application submitted successfully!",
            "application_id": application_id,
            "customer_id": customer_id
        }), 201

    except Exception as error:
        if connection:
            connection.rollback()

        return jsonify({"error": str(error)}), 500

    finally:
        if connection:
            connection.close()


# =====================================
# 6. RUN FLASK SERVER
# =====================================

if __name__ == "__main__":
    app.run(debug=True)
