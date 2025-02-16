import mysql.connector
from mysql.connector import Error

def check_database():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Mano@123",
            charset='utf8'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Check if database exists
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print("\nAvailable databases:")
            for db in databases:
                print(f"- {db[0]}")
                if db[0] == 'ecowaste':
                    print("\n[OK] ecowaste database exists!")
            
            # Switch to ecowaste database
            cursor.execute("USE ecowaste")
            
            # Check tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("\nTables in ecowaste database:")
            for table in tables:
                print(f"\n[TABLE] {table[0]}")
                # Show table structure
                cursor.execute(f"DESCRIBE {table[0]}")
                columns = cursor.fetchall()
                print("Columns:")
                for column in columns:
                    print(f"  - {column[0]}: {column[1]}")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\nMySQL connection closed")

if __name__ == "__main__":
    check_database()
