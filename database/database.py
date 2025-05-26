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
            self.printTime("Error! Cannot create the database connection.")

    def create_connection(self, host="127.0.0.1", database="delcarmencomplaint", user="root", password="password"):
        """ create a database connection to a MySQL database """
        conn = None
        try:
            self.printTime("Connecting")
            conn = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            if conn.is_connected():
                self.printTime("Connected to MySQL database")
            return conn
        except Error as e:
            self.printTime(f"Error: {e}")
        return conn

    def create_table(self):
        """ create tables in the MySQL database """
        try:
            cursor = self.cursor

            # --- Create Resident Table ---
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS residents (
                    resident_id VARCHAR(9) PRIMARY KEY,
                    first_name VARCHAR(64) NOT NULL,
                    last_name VARCHAR(64) NOT NULL,
                    age INT UNSIGNED,
                    birth_date DATE NOT NULL,
                    photo_cred VARCHAR(255) NOT NULL,
                    address VARCHAR(255) NOT NULL,
                    contact VARCHAR(11) NOT NULL,
                    sex ENUM('Male', 'Female') NOT NULL
                );
            ''')

            # --- Create Complaint Table ---
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS complaints (
                    complaint_id VARCHAR(9) PRIMARY KEY,
                    date_time DATETIME NOT NULL,
                    complaint_desc VARCHAR(120) NOT NULL,
                    resident_id VARCHAR(9) NULL,
                    complaint_category VARCHAR(64) NOT NULL,
                    complaint_status ENUM('Completed', 'Pending', 'Cancelled') NOT NULL,
                    location VARCHAR(255),
                    FOREIGN KEY (resident_id) REFERENCES residents(resident_id)
                        ON DELETE SET NULL
                );
            ''')

            # --- Create BarangayOfficials Table ---
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS barangay_officials (
                    barangay_official_id VARCHAR(9) PRIMARY KEY,
                    first_name VARCHAR(64) NOT NULL,
                    last_name VARCHAR(64) NOT NULL,
                    contact VARCHAR(11) NOT NULL,
                    position VARCHAR(64) NOT NULL
                );
            ''')


            # --- Create Accuses Table ---
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accuses (
                    resident_id VARCHAR(9) NOT NULL,
                    complaint_id VARCHAR(9) NOT NULL,
                    PRIMARY KEY (resident_id, complaint_id),
                    FOREIGN KEY (resident_id) REFERENCES residents(resident_id) ON DELETE CASCADE,
                    FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE CASCADE
                );
            ''')


            # --- Handles table ---
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS handles (
                    official_id VARCHAR(9) NOT NULL,
                    complaint_id VARCHAR(9) NOT NULL,
                    handle_datetime DATETIME NOT NULL,
                    PRIMARY KEY (official_id, complaint_id),
                    FOREIGN KEY (official_id) REFERENCES barangay_officials(official_id) ON DELETE CASCADE,
                    FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE CASCADE
                );
            ''')


            self.conn.commit()
        except Error as e:
            self.printTime(f"Error: {e}")


    #--------------------------------------------------------------------------- RESIDENTS TABLE OPERATIONS
    def insert_resident(self, resident):
        """ insert a new resident into the residents table """
        sql = ''' INSERT INTO residents(resident_id, first_name, last_name, age, birth_date, photo_cred, address, contact, sex)
                  VALUES (%s, %s, %s, 0, %s, %s, %s, %s, %s) '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, resident)
            self.conn.commit()
            self.printTime(f"Resident {resident[1]} inserted successfully")
        except Error as e:
            self.printTime(f"Error: {e}")

    def update_resident(self, new_resident):
        """ update an existing resident in the residents table using resident_id """
        sql = ''' UPDATE residents
                  SET first_name = %s, last_name = %s, birth_date = %s, photo_cred = %s, address = %s, contact = %s, sex = %s
                  WHERE resident_id = %s '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (*new_resident[1:8], new_resident[0]))
            self.conn.commit()
            self.printTime(f"Resident {new_resident[0]} updated successfully")
        except Error as e:
            self.printTime(f"Error: {e}")

    def update_resident_age(self, resident_id, age):
        """ update the age of an existing resident in the residents table using resident_id """
        sql = ''' UPDATE residents
                  SET age = %s
                  WHERE resident_id = %s '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (age, resident_id))
            self.conn.commit()
            self.printTime(f"Resident {resident_id} age updated successfully")
        except Error as e:
            self.printTime(f"Error: {e}")

    def remove_resident(self, resident_id):
        """ remove a resident from the residents table """
        sql = ''' DELETE FROM residents WHERE resident_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (resident_id,))
            self.conn.commit()
            self.printTime(f"Resident {resident_id} removed successfully")
        except Error as e:
            self.printTime(f"Error: {e}")

    #--------------------------------------------------------------------------- COMPLAINTS TABLE OPERATIONS
    def insert_complaint(self, complaint):
        """ insert a new complaint into the complaints table """
        sql = ''' INSERT INTO complaints(complaint_id, date_time, complaint_desc, resident_id, complaint_category, complaint_status, location)
                  VALUES (%s, %s, %s, %s, %s, %s, %s) '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, complaint)
            self.conn.commit()
            self.printTime(f"Complaint {complaint[2]} inserted successfully")
        except Error as e:
            self.printTime(f"Error: {e}")

    def update_complaint(self, new_complaint):
        """ update an existing complaint in the complaints table using complaint_id """
        sql = ''' UPDATE complaints
                  SET date_time = %s, complaint_desc = %s, resident_id = %s, complaint_category = %s, complaint_status = %s, location = %s
                  WHERE complaint_id = %s '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (*new_complaint[1:7], new_complaint[0]))
            self.conn.commit()
            self.printTime(f"Complaint {new_complaint[0]} updated successfully")
        except Error as e:
            self.printTime(f"Error: {e}")

    def remove_complaint(self, complaint_id):
        """ remove a complaint from the complaints table """
        sql = ''' DELETE FROM complaints WHERE complaint_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (complaint_id,))
            self.conn.commit()
            self.printTime(f"Complaint {complaint_id} removed successfully")
        except Error as e:
            self.printTime(f"Error: {e}")

    #--------------------------------------------------------------------------- BARANGAY OFFICIALS TABLE OPERATIONS
    def insert_barangay_official(self, official):
        """ insert a new barangay official into the barangay_officials table """
        sql = ''' INSERT INTO barangay_officials(official_id, first_name, last_name, contact, position)
                  VALUES (%s, %s, %s, %s, %s) '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, official)
            self.conn.commit()
            self.printTime(f"Barangay Official {official[1]} inserted successfully")
        except Error as e:
            self.printTime(f"Error: {e}")
    
    def update_barangay_official(self, new_official):
        """ update an existing barangay official in the barangay_officials table using official_id """
        sql = ''' UPDATE barangay_officials
                  SET first_name = %s, last_name = %s, contact = %s, position = %s
                  WHERE official_id = %s '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (*new_official[1:5], new_official[0]))
            self.conn.commit()
            self.printTime(f"Barangay Official {new_official[0]} updated successfully")
        except Error as e:
            self.printTime(f"Error: {e}")

    def remove_barangay_official(self, official_id):
        """ remove a barangay official from the barangay_officials table """
        sql = ''' DELETE FROM barangay_officials WHERE official_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (official_id,))
            self.conn.commit()
            self.printTime(f"Barangay Official {official_id} removed successfully")
        except Error as e:
            self.printTime(f"Error: {e}")

    #--------------------------------------------------------------------------- ACCUSES AND HANDLES TABLE OPERATIONS
    def insert_accuse(self, accuse):
        """
        Probably magamit rani sa definition UI sa isa ka element sa complaint
        Args:
            accuse (tuple): tuple(resident_id, complaint_id)
        """        
        sql = ''' INSERT INTO accuses(resident_id, complaint_id)
                  VALUES (%s, %s) '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, accuse)
            self.conn.commit()
            self.printTime(f"Accuse {accuse[0]} inserted successfully")
        except Error as e:
            self.printTime(f"Error: {e}")

    def remove_accuse(self, resident_id, complaint_id):
        """ remove an accuse from the accuses table """
        sql = ''' DELETE FROM accuses WHERE resident_id = %s AND complaint_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (resident_id, complaint_id))
            self.conn.commit()
            self.printTime(f"Accuse {resident_id} removed successfully")
        except Error as e:
            self.printTime(f"Error: {e}")

    #--------------------------------------------------------------------------- HANDLES TABLE OPERATIONS
    def insert_handle(self, handle):
        """
        Probably magamit rani sa definition UI sa isa ka element sa complaint
        Args:
            handle (tuple): tuple(official_id, complaint_id, handle_datetime)
        """        
        sql = ''' INSERT INTO handles(official_id, complaint_id, handle_datetime)
                  VALUES (%s, %s, %s) '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, handle)
            self.conn.commit()
            self.printTime(f"Handle {handle[0]} inserted successfully")
        except Error as e:
            self.printTime(f"Error: {e}")

    def remove_handle(self, official_id, complaint_id):
        """ remove a handle from the handles table """
        sql = ''' DELETE FROM handles WHERE official_id = %s AND complaint_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (official_id, complaint_id))
            self.conn.commit()
            self.printTime(f"Handle {official_id} removed successfully")
        except Error as e:
            self.printTime(f"Error: {e}")

    def get_barangay_official(self, official_id):
        """ get a single barangay official by their ID """
        self.printTime(f"Fetching barangay official with ID {official_id}")
        sql = ''' SELECT * FROM barangay_officials WHERE official_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (official_id,))
            result = cursor.fetchone()
            if result:
                self.printTime(f"Barangay Official found: {result}")
                return result
            else:
                self.printTime("Barangay Official not found")
                return None
        except Error as e:
            self.printTime(f"Error: {e}")

    def get_element_by_id(self, table, element_id):
        """ get a single element from the specified table by its ID """
        self.printTime(f"Fetching element with ID {element_id} from {table} table")
        sql = f''' SELECT * FROM {table} WHERE {table[:-1]}_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (element_id,))
            result = cursor.fetchone()
            if result:
                self.printTime(f"Element found: {result}")
                return result
            else:
                self.printTime("Element not found")
                return None
        except Error as e:
            self.printTime(f"Error: {e}")

    def count_complaints_status(self):
        """ count the number of complaints with each status """
        values = []
        sql = ''' SELECT COUNT(*) FROM complaints WHERE complaint_status = %s '''
        try:
            cursor = self.cursor
            cursor.execute('SELECT COUNT(*) FROM complaints')
            values.append(cursor.fetchone())
            cursor.execute(sql, ('Completed',))
            values.append(cursor.fetchone())
            cursor.execute(sql, ('Pending',))
            values.append(cursor.fetchone())
            cursor.execute(sql, ('Cancelled',))
            values.append(cursor.fetchone())
            return values
        except Error as e:
            self.printTime(f"Error: {e}")

    # For multiple elements of a given table
    def get_elements(self, table="residents", column="last_name", order="ASC", page=1, limit=15):
        """ get elements from the specified table """

        self.printTime(f"Fetching elements from {table} table, ordered by {column} in {order} order, page {page}, limit {limit}")
        offset = (page - 1) * limit     # Calculate offset for pagination
        sql = f''' SELECT * FROM {table} ORDER BY {column} {order} LIMIT {limit} OFFSET {offset} '''
        try:
            cursor = self.cursor
            cursor.execute(sql)
            results = cursor.fetchall()
            if results:
                self.printTime(f"{len(results)} residents found")
                return results
            else:
                self.printTime("No residents found")
                return []
        except Error as e:
            self.printTime(f"Error: {e}")

    def check_unique_id(self, table, element_id):
        """ check if an ID is unique in the specified table """
        self.printTime(f"Checking uniqueness of ID {element_id} in {table} table")
        sql = f''' SELECT COUNT(*) FROM {table} WHERE {table[:-1]}_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (element_id,))
            count = cursor.fetchone()[0]
            is_unique = count == 0
            self.printTime(f"ID {element_id} is {'unique' if is_unique else 'not unique'}")
            return is_unique
        except Error as e:
            self.printTime(f"Error: {e}")
            return False

    def close_connection(self):
        """ close the database connection """
        if self.conn.is_connected():
            self.conn.close()

    def printTime(self, message):
        """ print the current time with a message """
        now = datetime.datetime.now()
        print(f"[{now.strftime("%H:%M:%S.") + f"{int(now.microsecond/1000):03d}"}]  {message}")