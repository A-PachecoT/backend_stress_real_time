import mysql.connector
from tabulate import tabulate
from typing import Dict, List, Any


class DatabaseExplorer:
    def __init__(self, host: str, user: str, password: str):
        self.host = host
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self, database: str = None):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=database,
            )
            self.cursor = self.connection.cursor(dictionary=True)
            return True
        except mysql.connector.Error as e:
            print(f"Error connecting to database: {e}")
            return False

    def get_databases(self) -> List[str]:
        """Get all databases"""
        self.cursor.execute("SHOW DATABASES;")
        return [db["Database"] for db in self.cursor.fetchall()]

    def get_table_info(self, table: str) -> Dict[str, Any]:
        """Get detailed information about a table"""
        # Get column information
        self.cursor.execute(f"DESCRIBE {table};")
        columns = self.cursor.fetchall()

        # Get create table statement
        self.cursor.execute(f"SHOW CREATE TABLE {table};")
        create_statement = self.cursor.fetchone()["Create Table"]

        # Get row count
        self.cursor.execute(f"SELECT COUNT(*) as count FROM {table};")
        row_count = self.cursor.fetchone()["count"]

        return {
            "columns": columns,
            "create_statement": create_statement,
            "row_count": row_count,
        }

    def get_table_sample(self, table: str, limit: int = 5) -> List[Dict]:
        """Get sample data from table"""
        self.cursor.execute(f"SELECT * FROM {table} LIMIT {limit};")
        return self.cursor.fetchall()

    def get_foreign_keys(self, table: str) -> List[Dict]:
        """Get foreign key relationships"""
        self.cursor.execute(
            f"""
            SELECT 
                COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
            FROM
                INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE
                TABLE_NAME = '{table}'
                AND REFERENCED_TABLE_NAME IS NOT NULL
                AND TABLE_SCHEMA = DATABASE();
        """
        )
        return self.cursor.fetchall()

    def explore_database(self, database: str):
        """Main method to explore a database"""
        if not self.connect(database):
            return

        print(f"\n{'='*80}")
        print(f"DATABASE: {database}")
        print(f"{'='*80}")

        # Get all tables
        self.cursor.execute("SHOW TABLES;")
        tables = [list(table.values())[0] for table in self.cursor.fetchall()]

        for table in tables:
            print(f"\n{'='*40} TABLE: {table} {'='*40}")

            # Get table information
            table_info = self.get_table_info(table)

            # Print column information
            print("\nCOLUMN STRUCTURE:")
            print(tabulate(table_info["columns"], headers="keys", tablefmt="grid"))

            # Print row count
            print(f"\nTotal rows: {table_info['row_count']}")

            # Print foreign keys
            foreign_keys = self.get_foreign_keys(table)
            if foreign_keys:
                print("\nFOREIGN KEY RELATIONSHIPS:")
                print(tabulate(foreign_keys, headers="keys", tablefmt="grid"))

            # Print sample data
            sample_data = self.get_table_sample(table)
            if sample_data:
                print(f"\nSAMPLE DATA (up to 5 rows):")
                print(tabulate(sample_data, headers="keys", tablefmt="grid"))

            print(f"\nCREATE TABLE STATEMENT:")
            print(table_info["create_statement"])
            print("\n" + "-" * 80)

    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


def main():
    # Database connection parameters
    HOST = "stress-prueba1.cna4icyokmxm.us-east-2.rds.amazonaws.com"
    USER = "admin1"
    PASSWORD = "stressminderprueba1"

    explorer = DatabaseExplorer(HOST, USER, PASSWORD)

    # First, show all available databases
    explorer.connect()
    print("Available databases:")
    databases = explorer.get_databases()
    for i, db in enumerate(databases, 1):
        print(f"{i}. {db}")

    # Let user choose which database to explore
    while True:
        try:
            choice = input("\nEnter database number to explore (or 'q' to quit): ")
            if choice.lower() == "q":
                break
            db_index = int(choice) - 1
            if 0 <= db_index < len(databases):
                explorer.explore_database(databases[db_index])
            else:
                print("Invalid database number")
        except ValueError:
            print("Please enter a valid number")
        except Exception as e:
            print(f"An error occurred: {e}")

    explorer.close()


if __name__ == "__main__":
    main()
