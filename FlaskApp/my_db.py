from flask_sqlalchemy import SQLAlchemy

from .__init__ import db

class user_table(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(4096))
    user_id = db.Column(db.Integer)
    authkey = db.Column(db.String(4096))
    login = db.Column(db.Integer)
    read_access = db.Column(db.Integer)
    write_access = db.Column(db.Integer)

    def __init__(self, name, user_id, authkey, login, read_access, write_access):
        self.name = name
        self.user_id = user_id
        self.authkey = authkey
        self.login = login
        self.read_access = read_access
        self.write_access = write_access

def delete_all():
    try:
        db.session.query(user_table).delete()
        db.session.commit()
        print("Delete all done")
    except Exception as e:
        print("Failed " + str(e))
        db.session.rollback()

def get_user_row_if_exits(user_id):
    get_user_row = user_table.query.filter_by(user_id=user_id).first()
    if get_user_row != None:
        return get_user_row
    else:
        print("User doesn't exist")
        return False


def add_user_and_login(name, user_id):
    row = get_user_row_if_exits(user_id)
    if(row != False):
        row.login = 1
        db.session.commit()
    else:
        print("Adding user " + name)
        new_user = user_table(name, user_id, None, 1, 0, 0)
        db.session.add(new_user)
        db.session.commit()
    print("user " + name + " login added")

def user_logout(user_id):
    row = get_user_row_if_exits(user_id)
    if row != False:
        row.login = 0
        db.session.commit()
        print("user " + row.name + " logged out")


def add_auth_key(user_id, auth):
    row = get_user_row_if_exits(user_id)
    if row != False:
        row.authkey = auth
        db.session.commit()
        print("user " + row.name + " authkey added")


def view_all():
    row = user_table.query.all()
    for n in range(0, len(row)):
        print(str(row[n].id) + ' | ' + row[n].name + ' | ' + str(row[n].user_id) + ' | ' + str(row[n].authkey) + ' | ' + str(row[n].login))


def get_all_logged_in_users():
    row = user_table.query.filter_by(login=1).all()
    print("Logged in users: ")
    for n in range(0, len(row)):
        print(str(row[n].id) + ' | ' + row[n].name + ' | ' + str(row[n].user_id) + ' | ' + str(row[n].authkey) + ' | ' + str(row[n].login))