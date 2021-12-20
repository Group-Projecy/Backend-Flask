from flask_sqlalchemy import SQLAlchemy

from .__init__ import db

class room_reading_table(db.Model):
    __tablename__ = "room_reading"
    room_reading_id = db.Column(db.Integer, primary_key = True)
    room_id = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    room_date_time = db.Column(db.DateTime)

    def __init__(self, room_id, temperature, room_date_time):
        self.room_id = room_id
        self.temperature = temperature
        self.room_date_time = room_date_time

def delete_all():
    try:
        db.session.query(room_reading_table).delete()
        db.session.commit()
        print("Delete all rooms done")
    except Exception as e:
        print("Failed " + str(e))
        db.session.rollback()

def get_room_reading_row_if_exits(room_reading_id):
    get_room_reading_row = room_reading_table.query.filter_by(room_reading_id=room_reading_id).first()
    if get_room_reading_row != None:
        return get_room_reading_row
    else:
        print("Room reading doesn't exist")
        return False

#
# def add_user_and_login(name, user_id):
#     row = get_room_reading_row_if_exits(room_reading_id)
#     if(row != False):
#         row.login = 1
#         db.session.commit()
#     else:
#         print("Adding user " + name)
#         new_user = user_table(name, user_id, None, 1, 0, 0)
#         db.session.add(new_user)
#         db.session.commit()
#     print("user " + name + " login added")
#
# def user_logout(user_id):
#     row = get_user_row_if_exits(user_id)
#     if row != False:
#         row.login = 0
#         db.session.commit()
#         print("user " + row.name + " logged out")
#
#
# def add_auth_key(user_id, auth):
#     row = get_user_row_if_exits(user_id)
#     if row != False:
#         row.authkey = auth
#         db.session.commit()
#         print("user " + row.name + " authkey added")
#
#
# def view_all():
#     row = user_table.query.all()
#     for n in range(0, len(row)):
#         print(str(row[n].id) + ' | ' + row[n].name + ' | ' + str(row[n].user_id) + ' | ' + str(row[n].authkey) + ' | ' + str(row[n].login))
#
#
# def get_all_logged_in_users():
#     row = user_table.query.filter_by(login=1).all()
#     print("Logged in users: ")
#     for n in range(0, len(row)):
#         print(str(row[n].id) + ' | ' + row[n].name + ' | ' + str(row[n].user_id) + ' | ' + str(row[n].authkey) + ' | ' + str(row[n].login))
#