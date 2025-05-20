# Dari ko mag test sa DB

import database as db
if __name__ == '__main__':
    DB = db.Database()


    # Replace the following with actual values required by insert_barangay_official
    DB.insert_barangay_official(('27384930', 'John', 'Doe', '09123456789', 'Barangay Captain'))
    DB.insert_barangay_official(('27384931', 'Jane', 'Smith', '09123456788', 'Barangay Secretary'))
    DB.insert_barangay_official(('27384932', 'Alice', 'Johnson', '09123456787', 'Barangay Treasurer'))
    DB.insert_barangay_official(('27384933', 'Bob', 'Brown', '09123456786', 'Barangay Councilor'))
    DB.close_connection()
