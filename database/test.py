# Dari ko mag test sa DB

import database as db
import datetime
import random 
if __name__ == '__main__':
    DB = db.Database()

    DB.check_unique_id('residents', '1211-1111')

    DB.close_connection()
