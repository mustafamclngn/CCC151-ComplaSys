# Dari ko mag test sa DB

import database as db
if __name__ == '__main__':
    DB = db.Database()


    # DB.insert_complaint(("02304530", "2022-10-01 12:00:00", "Test complaint", "03030303", "Noise", "Open", "Location D"))
    DB.remove_complaint("02304530")
    DB.close_connection()
