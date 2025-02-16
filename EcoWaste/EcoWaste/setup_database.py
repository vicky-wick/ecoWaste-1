import mysql.connector
from mysql.connector import Error

def setup_database():
    connection = None
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Mano@123"  # Updated password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS ecowaste")
            print("Database 'ecowaste' created successfully")
            
            # Switch to ecowaste database
            cursor.execute("USE ecowaste")
            
            # Create tables if they don't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    password VARCHAR(120) NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    user_type VARCHAR(20) NOT NULL,
                    full_name VARCHAR(100),
                    phone VARCHAR(20),
                    address VARCHAR(200),
                    eco_points INT DEFAULT 0,
                    store_name VARCHAR(100),
                    business_license VARCHAR(50),
                    company_name VARCHAR(100),
                    industry_type VARCHAR(50),
                    employee_count VARCHAR(20)
                )
            """)
            print("User table created successfully")
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS product (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_type VARCHAR(100) NOT NULL,
                    brand VARCHAR(100) NOT NULL,
                    usage_pattern VARCHAR(50) NOT NULL,
                    predicted_expiry FLOAT NOT NULL,
                    predicted_price FLOAT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_id INT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user(id)
                )
            """)
            print("Product table created successfully")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    setup_database()
