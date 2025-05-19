# Dari ko mag test sa DB

import database as db
if __name__ == '__main__':
    DB = db.Database()
    DB.get_elements("residents", "last_name", "ASC", 1, 15)
    DB.close_connection()
