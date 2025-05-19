# Dari ko mag test sa DB

import database as db
if __name__ == '__main__':
    DB = db.Database()
    # Example get resident data
    for i in DB.get_elements(column="first_name"):
        print(i)


    DB.close_connection()
