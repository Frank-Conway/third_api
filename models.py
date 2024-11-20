import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="zhihe"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return None

def create_tables():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS request_records (
        id INT AUTO_INCREMENT PRIMARY KEY,
        url VARCHAR(255) NOT NULL,
        data TEXT NOT NULL,
        status VARCHAR(50) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INT AUTO_INCREMENT PRIMARY KEY,
        request_id INT,
        result TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (request_id) REFERENCES request_records(id)
    )
    """)
    connection.commit()
    cursor.close()
    connection.close()

def save_result_to_db(result, request_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO results (request_id, result) VALUES (%s, %s)", (request_id, str(result)))
    connection.commit()
    cursor.close()
    connection.close()

def save_request_record(url, data, status):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO request_records (url, data, status) VALUES (%s, %s, %s)", (url, str(data), status))
    request_id = cursor.lastrowid
    connection.commit()
    cursor.close()
    connection.close()
    return request_id