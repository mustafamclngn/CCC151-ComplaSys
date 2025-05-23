import mysql.connector
import datetime
from mysql.connector import Error

class Database:
    def __init__(self):
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor()


        if self.conn is not None:
            self.create_table()
        else:
            print("Error! Cannot create the database connection.")

    def create_connection(self, host="127.0.0.1", database="delcarmencomplaintmanagement", user="root", password="hello1234"):
        """ create a database connection to a MySQL database """
        conn = None
        try:
            conn = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            if conn.is_connected():
                print("Connected to MySQL database")
            return conn
        except Error as e:
            print(f"Error: {e}")
        return conn

    def create_table(self):
        """ create tables in the MySQL database """
        try:
            cursor = self.cursor

            # --- Create Resident Table ---
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Resident (
                    resident_id VARCHAR(8) PRIMARY KEY,
                    first_name VARCHAR(64) NOT NULL,
                    last_name VARCHAR(64) NOT NULL,
                    birth_date DATE NOT NULL,
                    photo_cred VARCHAR(255) NOT NULL,
                    address VARCHAR(255) NOT NULL,
                    contact VARCHAR(11) NOT NULL,
                    sex ENUM('Male', 'Female') NOT NULL
                );
            ''')

            # # --- Create Complaint Table ---
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Complaint (
                    complaint_id VARCHAR(8) PRIMARY KEY,
                    date_time DATETIME NOT NULL,
                    complaint_desc VARCHAR(120) NOT NULL,
                    resident_id VARCHAR(8),
                    complaint_category VARCHAR(64) NOT NULL,
                    complaint_status VARCHAR(8) NOT NULL,
                    location VARCHAR(255),
                    FOREIGN KEY (resident_id) REFERENCES residents(resident_id)
                         ON DELETE SET NULL
                 );
             ''')

            # # --- Create BarangayOfficials Table ---
            cursor.execute('''
             CREATE TABLE IF NOT EXISTS BarangayOfficials (
                    official_id INT PRIMARY KEY,
                    first_name VARCHAR(64) NOT NULL,
                     last_name VARCHAR(64) NOT NULL,
                     contact VARCHAR(11) NOT NULL,
                     position VARCHAR(64) NOT NULL
                 );
             ''')

            self.conn.commit()
        except Error as e:
            print(f"Error: {e}")

    def insert_resident(self, resident):
        """ insert a new resident into the residents table """
        sql = ''' INSERT INTO residents(resident_id, first_name, last_name, birth_date, photo_cred, address, contact, sex)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s) '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, resident)
            self.conn.commit()
            print(f"Resident {resident[1]} inserted successfully")
        except Error as e:
            print(f"Error: {e}")

    def remove_resident(self, resident_id):
        """ remove a resident from the residents table """
        sql = ''' DELETE FROM residents WHERE resident_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (resident_id,))
            self.conn.commit()
            print(f"Resident {resident_id} removed successfully")
        except Error as e:
            print(f"Error: {e}")

    def get_resident(self, resident_id):
        """ get a resident from the residents table """
        sql = ''' SELECT * FROM residents WHERE resident_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (resident_id,))
            result = cursor.fetchone()
            if result:
                print(f"Resident {resident_id} found: {result}")
                return result
            else:
                print(f"Resident {resident_id} not found")
                return None
        except Error as e:
            print(f"Error: {e}")


    def close_connection(self):
        """ close the database connection """
        if self.conn.is_connected():
            self.conn.close()

