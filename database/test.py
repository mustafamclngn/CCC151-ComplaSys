# Dari ko mag test sa DB

import database as db
if __name__ == '__main__':
    DB = db.Database()

    DB.remove_resident("02020202")




    DB.close_connection()
