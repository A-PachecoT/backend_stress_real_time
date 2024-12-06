import mysql.connector

try:
    connection = mysql.connector.connect(
        host="stress-prueba1.cna4icyokmxm.us-east-2.rds.amazonaws.com",
        user="admin1",
        password="stressminderprueba1",
        database="sensores_db",
    )

    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Connected to MariaDB Server version ", db_info)
        cursor = connection.cursor()

        # Show all tables in the database
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("\nTables in sensores_db:")
        for table in tables:
            print(table[0])
            # Show the contents of each table
            cursor.execute(f"SELECT * FROM {table[0]};")
            rows = cursor.fetchall()
            print(f"\nContents of table {table[0]}:")
            for row in rows:
                print(row)
            print("\n" + "-" * 50)

except mysql.connector.Error as e:
    print("Error connecting to MariaDB Platform:", e)

finally:
    if "connection" in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MariaDB connection is closed")
