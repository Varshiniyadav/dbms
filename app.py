from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '12345',
    'database': 'event',
    'port': 3306
}

# Function to get database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("✅ Successfully connected to the database.")
            return conn
        else:
            print("❌ Connection failed but no exception raised.")
    except Error as err:
        print(f"❌ Database connection error: {err}")
    return None

@app.route('/')
def index():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("📋 Tables in database:", tables)
        cursor.close()
        conn.close()
        return render_template('index.html', tables=tables)
    return render_template('index.html')

@app.route('/table/<table_name>')
def show_table(table_name):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('table_data.html', table_name=table_name, data=data)
    return "Error connecting to database", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
