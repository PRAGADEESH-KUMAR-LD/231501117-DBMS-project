import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',  # Or your MySQL server host
        user='root',       # Replace with your MySQL user
        password='pragadeeshluck2005',  # Replace with your MySQL password
        database='book_recommendation'  # Replace with your database name
    )
    return connection
