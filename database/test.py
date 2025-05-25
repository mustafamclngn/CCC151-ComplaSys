# Dari ko mag test sa DB

import database as db
import datetime
import random 
if __name__ == '__main__':
    DB = db.Database()

    print(DB.count_complaints_status())

    DB.close_connection()
