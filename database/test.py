# Dari ko mag test sa DB

import database as db
if __name__ == '__main__':
    DB = db.Database()
    # Example resident data
    resident_data = [
        ('06060606', 'Charlie', 'Brown', '1995-09-10', 'path/to/photo5.jpg', '654 Maple St', '09112223334', 'Male'),
        ('07070707', 'Diana', 'Evans', '1991-11-20', 'path/to/photo6.jpg', '987 Cedar St', '09223334445', 'Female'),
        ('08080808', 'Ethan', 'Clark', '1987-04-18', 'path/to/photo7.jpg', '159 Spruce St', '09334445556', 'Male'),
        ('09090909', 'Fiona', 'Garcia', '1993-08-25', 'path/to/photo8.jpg', '753 Birch St', '09445556667', 'Female'),
        ('10101010', 'George', 'Martinez', '1989-12-30', 'path/to/photo9.jpg', '852 Willow St', '09556667778', 'Male'),
        ('11111111', 'Hannah', 'Lee', '1994-06-05', 'path/to/photo10.jpg', '951 Aspen St', '09667778889', 'Female')
    ]
    for resident in resident_data:
        DB.insert_resident(resident)
