import mysql.connector
import datetime
from mysql.connector import Error
from PyQt5.QtWidgets import QMessageBox

def printTime(message):
    """ print the current time with a message """
    now = datetime.datetime.now()
    print(f"[{now.strftime("%H:%M:%S.") + f"{int(now.microsecond/1000):03d}"}]  {message}")

def warnMessageBox(parent=None, title="Message", message="", ):
    """ Display a message box with the given message and title """
    printTime(f"  WARNING [{title}]: {message}")
    QMessageBox.warning(parent, title, message)

def infoMessageBox(parent=None, title="Message", message="", ):
    """ Display a message box with the given message and title """
    printTime(f"  INFO    [{title}]: {message}")
    QMessageBox.information(parent, title, message)

def errorMessageBox(parent=None, title="Error", message="", ):
    """ Display an error message box with the given message and title """
    printTime(f"  ERROR   [{title}]: {message}")
    QMessageBox.critical(parent, title, message)

class Database:
    def __init__(self):
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor()

        if self.conn is not None:
            self.create_table()
        else:
            printTime("Error! Cannot create the database connection.")

    def create_connection(self, host="127.0.0.1", database="delcarmencomplaint", user="root", password="password"):
        """ create a database connection to a MySQL database """
        conn = None
        try:
            printTime("Connecting")
            conn = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            if conn.is_connected():
                printTime("Connected to MySQL database")
            return conn
        except Error as e:
            printTime(f"DATABASE    Error: {e}")
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
                    FOREIGN KEY (resident_id) REFERENCES residents(resident_id) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE CASCADE ON UPDATE CASCADE
                );
            ''')


            # --- Handles table ---
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS handles (
                    barangay_official_id VARCHAR(9) NOT NULL,
                    complaint_id VARCHAR(9) NOT NULL,
                    handle_datetime DATETIME NOT NULL,
                    PRIMARY KEY (barangay_official_id, complaint_id),
                    FOREIGN KEY (barangay_official_id) REFERENCES barangay_officials(barangay_official_id) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id) ON DELETE CASCADE ON UPDATE CASCADE
                );
            ''')


            self.conn.commit()
        except Error as e:
            printTime(f"DATABASE    Error: {e}")


    #--------------------------------------------------------------------------- RESIDENTS TABLE OPERATIONS
    def insert_resident(self, resident):
        """ insert a new resident into the residents table """
        sql = ''' INSERT INTO residents(resident_id, first_name, last_name, age, birth_date, photo_cred, address, contact, sex)
                  VALUES (%s, %s, %s, 0, %s, %s, %s, %s, %s) '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, resident)
            self.conn.commit()
            printTime(f"DATABASE    Resident {resident[1]} inserted successfully")
        except Error as e:
            printTime(f"DATABASE    Error: {e}")

    def update_resident(self, res_id, new_resident):
        """ update an existing resident in the residents table using resident_id """
        sql = ''' UPDATE residents
                  SET resident_id = %s, first_name = %s, last_name = %s, birth_date = %s, photo_cred = %s, address = %s, contact = %s, sex = %s
                  WHERE resident_id = %s '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (*new_resident, res_id))
            self.conn.commit()
            printTime(f"DATABASE    Resident {res_id} updated successfully")
        except Error as e:
            printTime(f"DATABASE    Error: {e}")

    def update_resident_age(self, resident_id, age, messageAlert=True):
        """ update the age of an existing resident in the residents table using resident_id """
        sql = ''' UPDATE residents
                  SET age = %s
                  WHERE resident_id = %s '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (age, resident_id))
            self.conn.commit()
            if messageAlert:
                printTime(f"DATABASE    Resident {resident_id} age updated successfully")
        except Error as e:
            printTime(f"DATABASE    Error: {e}")

    def remove_resident(self, resident_id):
        """ remove a resident from the residents table """
        sql = ''' DELETE FROM residents WHERE resident_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (resident_id,))
            self.conn.commit()
            printTime(f"DATABASE    Resident {resident_id} removed successfully")
        except Error as e:
            printTime(f"DATABASE    Error: {e}")

    #--------------------------------------------------------------------------- COMPLAINTS TABLE OPERATIONS
    def insert_complaint(self, complaint):
        """ insert a new complaint into the complaints table """
        sql = ''' INSERT INTO complaints(complaint_id, date_time, complaint_desc, resident_id, complaint_category, complaint_status, location)
                  VALUES (%s, %s, %s, %s, %s, %s, %s) '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, complaint)
            self.conn.commit()
            printTime(f"DATABASE    Complaint {complaint[2]} inserted successfully")
        except Error as e:
            printTime(f"DATABASE    Error: {e}")

    def update_complaint(self, com_id, new_complaint):
        """ update an existing complaint in the complaints table using complaint_id """
        sql = ''' UPDATE complaints
                  SET complaint_id = %s, date_time = %s, complaint_desc = %s, resident_id = %s, complaint_category = %s, complaint_status = %s, location = %s
                  WHERE complaint_id = %s '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (*new_complaint, com_id))
            self.conn.commit()
            printTime(f"DATABASE    Complaint {com_id} updated successfully")
        except Error as e:
            printTime(f"DATABASE    Error: {e}")

    def remove_complaint(self, complaint_id):
        """ remove a complaint from the complaints table """
        sql = ''' DELETE FROM complaints WHERE complaint_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (complaint_id,))
            self.conn.commit()
            printTime(f"DATABASE    Complaint {complaint_id} removed successfully")
        except Error as e:
            printTime(f"DATABASE    Error: {e}")

    def get_pending_complaints(self):
        """ get all pending complaints from the complaints table """
        printTime("DATABSE    Fetching pending complaints")
        sql = ''' SELECT * FROM complaints WHERE complaint_status = 'Pending' '''
        try:
            cursor = self.cursor
            cursor.execute(sql)
            results = cursor.fetchall()
            if results:
                printTime(f"DATABASE    {len(results)} pending complaints found")
                return results
            else:
                printTime("DATABASE    No pending complaints found")
                return []
        except Error as e:
            printTime(f"DATABASE    Error: {e}")

    #--------------------------------------------------------------------------- BARANGAY OFFICIALS TABLE OPERATIONS
    def insert_barangay_official(self, official):
        """ insert a new barangay official into the barangay_officials table """
        sql = ''' INSERT INTO barangay_officials(barangay_official_id, first_name, last_name, contact, position)
                  VALUES (%s, %s, %s, %s, %s) '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, official)
            self.conn.commit()
            printTime(f"DATABASE    Barangay Official {official[1]} inserted successfully")
        except Error as e:
            printTime(f"DATABASE    Error: {e}")
    
    def update_barangay_official(self, off_id, new_official):
        """ update an existing barangay official in the barangay_officials table using barangay_official_id """
        sql = ''' UPDATE barangay_officials
                  SET barangay_official_id = %s, first_name = %s, last_name = %s, contact = %s, position = %s
                  WHERE barangay_official_id = %s '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (*new_official, off_id))
            self.conn.commit()
            printTime(f"DATABASE    Barangay Official {off_id} updated successfully")
        except Error as e:
            printTime(f"DATABASE    Error: {e}")

    def remove_barangay_official(self, barangay_official_id):
        """ remove a barangay official from the barangay_officials table """
        sql = ''' DELETE FROM barangay_officials WHERE barangay_official_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (barangay_official_id,))
            self.conn.commit()
            printTime(f"DATABASE    Barangay Official {barangay_official_id} removed successfully")
        except Error as e:
            printTime(f"DATABASE    Error: {e}")

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
            printTime(f"DATABASE    Accuse [{accuse[0]}:{accuse[1]}] inserted successfully")
        except Error as e:
            printTime(f"DATABASE    Error: {e}")

    def remove_accuse(self, accuse):
        """ remove an accuse from the accuses table 
        Args:
            accuse (tuple): tuple(resident_id, complaint_id)
        """
        sql = ''' DELETE FROM accuses WHERE resident_id = %s AND complaint_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, accuse)
            self.conn.commit()
            printTime(f"DATABASE    Accuse [{accuse[0]}:{accuse[1]}] removed successfully")
        except Error as e:
            printTime(f"DATABASE    Error: {e}")

    def check_unique_accuse(self, IDs):
        """ check if an accuse is unique in the accuses table """
        printTime(f"DATABASE    Checking uniqueness of accuse {IDs}")
        sql = ''' SELECT COUNT(*) FROM accuses WHERE resident_id = %s AND complaint_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, IDs)
            count = cursor.fetchone()[0]
            is_unique = count == 0
            printTime(f"DATABASE    Accuse {IDs} is {'unique' if is_unique else 'not unique'}")
            return is_unique
        except Error as e:
            printTime(f"DATABASE    Error: {e}")
            return False

    def get_accuses_elements(self, complaint_id):
        """ get all accuses for a specific complaint """
        printTime(f"DATABASE    Fetching accuses for complaint {complaint_id}")
        sql = ''' SELECT resident_id FROM accuses WHERE complaint_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (complaint_id,))
            results = cursor.fetchall()
            if results:
                printTime(f"DATABASE    {len(results)} accuses found for complaint {complaint_id}")
                return results
            else:
                printTime("DATABASE    No accuses found")
                return []
        except Error as e:
            printTime(f"DATABASE    Error: {e}")

    def check_if_resident_accused(self, resident_id):
        """ check if a resident is accused in any complaint """
        printTime(f"DATABASE    Checking if resident {resident_id} is accused in any complaint")
        sql = ''' SELECT COUNT(*) FROM accuses WHERE resident_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (resident_id,))
            count = cursor.fetchone()[0]
            is_accused = count > 0
            printTime(f"DATABASE    Resident {resident_id} is {'accused' if is_accused else 'not accused'} in any complaint")
            return is_accused
        except Error as e:
            printTime(f"DATABASE    Error: {e}")
            return False

    #--------------------------------------------------------------------------- HANDLES TABLE OPERATIONS
    def insert_handle(self, handle):
        """
        Probably magamit rani sa definition UI sa isa ka element sa complaint
        Args:
            handle (tuple): tuple(barangay_official_id, complaint_id, handle_datetime)
        """        
        sql = ''' INSERT INTO handles(barangay_official_id, complaint_id, handle_datetime)
                  VALUES (%s, %s, %s) '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, handle)
            self.conn.commit()
            printTime(f"DATABASE    Handle [{handle[0]}:{handle[1]}] inserted successfully")
        except Error as e:
            printTime(f"DATABASE    Error: {e}")

    def remove_handle(self, handle):
        """ remove a handle from the handles table 
        Args:
            handle (tuple): tuple(barangay_official_id, complaint_id)
        """
        sql = ''' DELETE FROM handles WHERE barangay_official_id = %s AND complaint_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, handle)
            self.conn.commit()
            printTime(f"DATABASE    Handle [{handle[0]}:{handle[1]} ]removed successfully")
        except Error as e:
            printTime(f"DATABASE    Error: {e}")

    def check_unique_handle(self, IDs):
        """ check if a handle is unique in the handles table """
        printTime(f"DATABASE    Checking uniqueness of handle {IDs}")
        sql = ''' SELECT COUNT(*) FROM handles WHERE barangay_official_id = %s AND complaint_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, IDs)
            count = cursor.fetchone()[0]
            is_unique = count == 0
            printTime(f"DATABASE    Handle {IDs} is {'unique' if is_unique else 'not unique'}")
            return is_unique
        except Error as e:
            printTime(f"DATABASE    Error: {e}")
            return False

    def get_handles_elements(self, attribute='complaint_id', id=None):
        """ get all handles for a specific complaint """
        printTime(f"DATABASE    Fetching handles for complaint {id}")
        sql = f''' SELECT * FROM handles WHERE {attribute} = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (id,))
            results = cursor.fetchall()
            if results:
                printTime(f"DATABASE    {len(results)} handles found for {attribute} {id}")
                return results
            else:
                printTime("DATABASE    No handles found")
                return []
        except Error as e:
            printTime(f"DATABASE    Error: {e}")


    def get_barangay_official(self, barangay_official_id):
        """ get a single barangay official by their ID """
        printTime(f"DATABASE    Fetching barangay official with ID {barangay_official_id}")
        sql = ''' SELECT * FROM barangay_officials WHERE barangay_official_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (barangay_official_id,))
            result = cursor.fetchone()
            if result:
                printTime(f"DATABASE    Barangay Official found: {result}")
                return result
            else:
                printTime("Barangay Official not found")
                return None
        except Error as e:
            printTime(f"DATABASE    Error: {e}")

    def get_element_by_id(self, table, element_id):
        """ get a single element from the specified table by its ID """
        printTime(f"DATABASE    Fetching element with ID {element_id} from {table} table")
        sql = f''' SELECT * FROM {table} WHERE {table[:-1]}_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (element_id,))
            result = cursor.fetchone()
            if result:
                printTime(f"DATABASE    Element found: {result}")
                return result
            else:
                printTime("Element not found")
                return None
        except Error as e:
            printTime(f"DATABASE    Error: {e}")

    def count_complaints_status(self, date=None):
        """ count the number of complaints with each status
         If date is provided, only count complaints in that month.
         Args:
            date (datetime.date or str): If provided, filter by this month.
         Returns:
            list: [total_complaints, completed, pending, cancelled]
        """
        values = []
        try:
            cursor = self.cursor
            if date is not None:
                if isinstance(date, str):
                    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                year = date.year
                month = date.month
                date_filter = "WHERE YEAR(date_time) = %s AND MONTH(date_time) = %s"
                params = (year, month)
            else:
                date_filter = ""
                params = ()

            # Total complaints
            sql_total = f"SELECT COUNT(*) FROM complaints {date_filter}"
            cursor.execute(sql_total, params)
            values.append(cursor.fetchone()[0])

            # By status
            for status in ('Completed', 'Pending', 'Cancelled'):
                sql_status = f"SELECT COUNT(*) FROM complaints {date_filter} AND complaint_status = %s" if date_filter else \
                             "SELECT COUNT(*) FROM complaints WHERE complaint_status = %s"
                status_params = params + (status,) if date_filter else (status,)
                cursor.execute(sql_status, status_params)
                values.append(cursor.fetchone()[0])

            return values
        except Error as e:
            printTime(f"DATABASE    Error: {e}")
            return []

    def count_elements(self, table):
        """ count the number of elements in the specified table """
        printTime(f"DATABASE    Counting elements in {table} table")
        sql = f''' SELECT COUNT(*) FROM {table} '''
        try:
            cursor = self.cursor
            cursor.execute(sql)
            count = cursor.fetchone()[0]
            printTime(f"DATABASE    {count} elements found in {table} table")
            return count
        except Error as e:
            printTime(f"DATABASE    Error: {e}")
            return 0

    # For multiple elements of a given table
    def get_elements(self, table="residents", column="last_name", order="ASC", page=1, limit=15):
        """ get elements from the specified table """

        printTime(f"DATABASE    Fetching elements from {table} table, ordered by {column} in {order} order, page {page}, limit {limit}")
        offset = (page - 1) * limit     # Calculate offset for pagination
        sql = f''' SELECT * FROM {table} ORDER BY {column} {order} LIMIT {limit} OFFSET {offset} '''
        try:
            cursor = self.cursor
            cursor.execute(sql)
            results = cursor.fetchall()
            if results:
                printTime(f"DATABASE    {len(results)} {table} found")
                return results
            else:
                printTime(f"DATABASE    No {table} found")
                return []
        except Error as e:
            printTime(f"DATABASE    Error: {e}")
            return []

    def check_unique_id(self, table, element_id):
        """ check if an ID is unique in the specified table """
        printTime(f"DATABASE    Checking uniqueness of ID {element_id} in {table} table")
        sql = f''' SELECT COUNT(*) FROM {table} WHERE {table[:-1]}_id = %s '''
        try:
            cursor = self.cursor
            cursor.execute(sql, (element_id,))
            count = cursor.fetchone()[0]
            is_unique = count == 0
            printTime(f"DATABASE    ID {element_id} is {'unique' if is_unique else 'not unique'}")
            return is_unique
        except Error as e:
            printTime(f"DATABASE    Error: {e}")
            return False
            
    def generate_id(self, table):
    #Generate an ID based on the table:
    #residents: YYYY-##### (e.g., 2024-00001)
    #complaints: ####-#### (e.g., 0001-0001)
    #barangay_officials: ####-YYYY (e.g., 0001-2024)

        from datetime import datetime
        year = datetime.now().year
        cursor = self.conn.cursor()

        if table == "residents":
            sql = "SELECT resident_id FROM residents WHERE resident_id LIKE %s ORDER BY resident_id DESC LIMIT 1"
            like_pattern = f"{year}-%"
            cursor.execute(sql, (like_pattern,))
            last_id = cursor.fetchone()
            if last_id:
                last_num = int(last_id[0].split('-')[1])
                new_num = last_num + 1
            else:
                new_num = 1
            return f"{year}-{new_num:04d}"

        elif table == "complaints":
            sql = "SELECT complaint_id FROM complaints ORDER BY complaint_id DESC LIMIT 1"
            cursor.execute(sql)
            last_id = cursor.fetchone()
            if last_id:
                left, right = map(int, last_id[0].split('-'))
                if right < 9999:
                    right += 1
                else:
                    left += 1
                    right = 1
            else:
                left, right = 1, 1
            return f"{left:04d}-{right:04d}"

        elif table == "barangay_officials":
            sql = "SELECT barangay_official_id FROM barangay_officials WHERE barangay_official_id LIKE %s ORDER BY barangay_official_id DESC LIMIT 1"
            like_pattern = f"%-{year}"
            cursor.execute(sql, (like_pattern,))
            last_id = cursor.fetchone()
            if last_id:
                left = int(last_id[0].split('-')[0])
                new_left = left + 1
            else:
                new_left = 1
            return f"{new_left:04d}-{year}"

        else:
            raise ValueError("Unknown table for ID generation")

        
    def universal_search(self, table, query, column=None, order="ASC", limit=100, offset=0):
        cursor = self.cursor
        param = f"%{query}%"

        if table == "residents":
            if column is None:
                column = "last_name"
            sql = f"""
                SELECT * FROM residents
                WHERE resident_id LIKE %s OR first_name LIKE %s OR last_name LIKE %s OR sex LIKE %s OR contact LIKE %s 
                ORDER BY {column} {order} LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (param, param, param, param, param, limit, offset))

        elif table == "complaints":
            # Default sort column for complaints
            if column is None:
                column = "date_time"
            sql = f"""
                SELECT * FROM complaints
                WHERE complaint_id LIKE %s OR resident_id LIKE %s OR complaint_category LIKE %s OR date_time LIKE %s OR complaint_status LIKE %s 
                ORDER BY {column} {order} LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (param, param, param, param, param, limit, offset))

        elif table == "barangay_officials":
            # Default sort column for officials
            if column is None:
                column = "last_name"
            sql = f"""
                SELECT * FROM barangay_officials
                WHERE barangay_official_id LIKE %s OR position LIKE %s OR first_name LIKE %s OR last_name LIKE %s OR contact LIKE %s
                ORDER BY {column} {order} LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (param, param, param, param, param, limit, offset))
        else:
            return []
        return cursor.fetchall()

    def calculate_age(self, birth_date):
        """ calculate age from birth date """
        if isinstance(birth_date, str):
            birth_date = datetime.datetime.strptime(birth_date, "%Y-%m-%d").date()
        today = datetime.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

    def close_connection(self):
        """ close the database connection """
        if self.conn.is_connected():
            self.conn.close()



