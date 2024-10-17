from App.models.user import *
from App.database import db
import csv

def create_user(username, password, position):
    if get_user_by_username(username):
        return False
    if position== 'admin':
        newuser = Admin(username=username, password=password, position=position)
    elif position == 'staff':
        newuser = Staff(username=username, password=password, position=position)
    else:
        return False
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return None
    return user

def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return None
    return user

def get_all_users():
    users = User.query.all()
    if not users:
        return None
    return users

def get_all_staff():
    staff = Staff.query.all()
    if not staff:
        return None
    return staff

def get_all_staff_json():
    staff = Staff.query.all()
    if not staff:
        return []
    staff = [staff.get_json() for staff in staff]
    return staff

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def get_single_user_json(user_id):
    s_user = User.query.get(user_id)
    if not s_user:
        return []
    s_user = s_user.get_json()
    return s_user

def update_user_fname(user, fname):
    user.fname = fname
    db.session.add(user)
    db.session.commit()
    return True

def update_user_lname(user, lname):
    user.lname = lname
    db.session.add(user)
    db.session.commit()
    return True

def update_user_name(user_id, name):
    user = get_user(user_id)
    flag = False
    if user:
        fname = name[0]
        lname = name[1]
        if fname:
            flag = update_user_fname(user, fname)
        if lname:
            flag = update_user_lname(user, lname)
    return flag

def update_user_password(id, password):
    user = get_user(id)
    flag = False
    if user:
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flag = user.check_password(password)
    return flag

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        db.session.commit()
        return user
    return None

def get_staff_courses(staff_id):
    staff = User.query.filter_by(id=staff_id).first()
    entries = []
    if not staff:
        return None
    for entry in staff.courses:
        entries.append(entry.get_json())
    return entries


def parse_users():
    with open('users.csv', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)

        for row in csvreader:
            username = row[0]
            password = row[1]
            position = row[2]
            fname = row[3]
            lname = row[4]

            user = Staff(
                username=username,
                password=password,
                position=position
            )
            db.session.add(user)
            user = get_user_by_username(username)
            name = (fname, lname)
            update_user_name(user.id, name)
        db.session.commit()
