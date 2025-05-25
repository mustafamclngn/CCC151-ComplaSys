# Dari ko mag test sa DB

import database as db
import datetime
import random 
if __name__ == '__main__':
    DB = db.Database()

    DB.insert_barangay_official(("30000001", "Juan", "Dela Cruz", "09123457001", "Captain"))
    DB.insert_barangay_official(("30000002", "Maria", "Santos", "09123457002", "Kagawad"))
    DB.insert_barangay_official(("30000003", "Jose", "Reyes", "09123457003", "Secretary"))
    DB.insert_barangay_official(("30000004", "Ana", "Garcia", "09123457004", "Treasurer"))
    DB.insert_barangay_official(("30000005", "Pedro", "Mendoza", "09123457005", "Kagawad"))

    DB.close_connection()
