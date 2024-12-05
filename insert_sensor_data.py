import mysql.connector
from datetime import datetime
import random
import time


class SensorDataInserter:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.connection = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )
        self.cursor = self.connection.cursor()

    def insert_sensor_data(self, temperatura: float, ritmo_cardiaco: float):
        """Insert a single sensor reading"""
        query = """
        INSERT INTO sensores (temperatura, ritmo_cardiaco)
        VALUES (%s, %s)
        """
        self.cursor.execute(query, (temperatura, ritmo_cardiaco))
        self.connection.commit()
        print(
            f"Inserted: Temperatura={temperatura}°C, Ritmo Cardíaco={ritmo_cardiaco} BPM"
        )

    def generate_random_data(self, num_readings: int = 1, interval: float = 0):
        """Generate and insert random sensor readings"""
        try:
            for _ in range(num_readings):
                # Generate realistic random values
                temperatura = round(
                    random.uniform(35.5, 38.5), 1
                )  # Normal body temperature range
                ritmo_cardiaco = round(
                    random.uniform(60, 100), 1
                )  # Normal heart rate range

                self.insert_sensor_data(temperatura, ritmo_cardiaco)

                if interval > 0 and _ < num_readings - 1:
                    time.sleep(interval)

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("\nDatabase connection closed")


def main():
    # Database connection parameters
    HOST = "stress-prueba1.cna4icyokmxm.us-east-2.rds.amazonaws.com"
    USER = "admin1"
    PASSWORD = "stressminderprueba1"
    DATABASE = "sensores_db"

    inserter = SensorDataInserter(HOST, USER, PASSWORD, DATABASE)

    while True:
        print("\nSensor Data Insertion Menu:")
        print("1. Insert single reading")
        print("2. Generate multiple random readings")
        print("3. Start continuous monitoring (with interval)")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            try:
                temp = float(input("Enter temperature (°C): "))
                heart_rate = float(input("Enter heart rate (BPM): "))
                inserter.insert_sensor_data(temp, heart_rate)
            except ValueError:
                print("Please enter valid numbers")

        elif choice == "2":
            try:
                num = int(input("How many readings to generate? "))
                inserter.generate_random_data(num)
            except ValueError:
                print("Please enter a valid number")

        elif choice == "3":
            try:
                interval = float(input("Enter interval between readings (seconds): "))
                num_readings = int(input("Enter number of readings (0 for infinite): "))

                if num_readings == 0:
                    print("Press Ctrl+C to stop...")
                    try:
                        while True:
                            inserter.generate_random_data(1)
                            time.sleep(interval)
                    except KeyboardInterrupt:
                        print("\nMonitoring stopped")
                else:
                    inserter.generate_random_data(num_readings, interval)
            except ValueError:
                print("Please enter valid numbers")

        elif choice == "4":
            break

        else:
            print("Invalid choice. Please try again.")

    inserter.close()


if __name__ == "__main__":
    main()
