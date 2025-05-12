import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.conn = self.create_connection()
        if self.conn is not None:
            self.create_table()
        else:
            print("Error! Cannot create the database connection.")

    def create_connection(self, host="127.0.0.1", database="ssis", user="root", password="admin"):
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
            cursor = self.conn.cursor()

            # --- Create Resident Table ---
            cursor.execute('''
                CREATE TABLE Resident (
                    resident_id VARCHAR(10) PRIMARY KEY,
                    first_name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255) NOT NULL,
                    birth_date DATE NOT NULL,
                    photo_cred VARCHAR(255) NOT NULL,
                    address VARCHAR(255) NOT NULL,
                    contact VARCHAR(11) NOT NULL,
                    sex ENUM('Male', 'Female') NOT NULL
                );
            ''')

            # --- Create Complaint Table ---
            cursor.execute('''
                CREATE TABLE Complaint (
                    complaint_id INT PRIMARY KEY,
                    date_time DATETIME NOT NULL,
                    complaint_desc VARCHAR(120) NOT NULL,
                    resident_id VARCHAR(10) NULL,
                    complaint_category VARCHAR(64) NOT NULL,
                    complaint_status VARCHAR(8) NOT NULL,
                    location VARCHAR(255),
                    FOREIGN KEY (resident_id) REFERENCES Resident(resident_id)
                        ON DELETE SET NULL
                );
            ''')

            # --- Create BarangayOfficials Table ---
            cursor.execute('''
                CREATE TABLE BarangayOfficials (
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
        """ insert a new resident into the Resident table """
        sql = ''' INSERT INTO Resident(resident_id, first_name, last_name, birth_date, photo_cred, address, contact, sex)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s) '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, resident)
            self.conn.commit()
        except Error as e:
            print(f"Error: {e}")

    def close_connection(self):
        """ close the database connection """
        if self.conn.is_connected():
            self.conn.close()

if __name__ == '__main__':
    db = Database()
    # Example resident data
    resident_data = ('R001', 'John', 'Doe', '1990-01-01', 'path/to/photo.jpg', '123 Main St', '0912342')