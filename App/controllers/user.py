from App.models.user import *
from App.database import db
import csv

# create a user. return the new user object, otherwise return false
def create_user(username, password, type):
    if get_user_by_username(username):
        return False
    if type == 'admin':
        newuser = Admin(username=username, password=password)
    elif type == 'staff':
        newuser = Staff(username=username, password=password)
    else:
        return False
    db.session.add(newuser)
    db.session.commit()
    return newuser

# get user with specified username. return user object, otherwise return None
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return None
    return user

# get user with specified id. return user object, otherwise return None
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return None
    return user

# get all users. return list of entries, otherwise return None
def get_all_users():
    users = User.query.all()
    if not users:
        return None
    return users

# get all staff. return list of entries, otherwise return None
def get_all_staff():
    staff = Staff.query.all()
    if not staff:
        return None
    return staff

# get all staff in json format. return dict of entries, otherwise return empty dict
def get_all_staff_json():
    staff = Staff.query.all()
    if not staff:
        return []
    staff = [staff.get_json() for staff in staff]
    return staff

# get all users in json format. return dict of entries, otherwise return empty dict
def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

# get user with specified id in json format. return the found user dict, otherwise return none
def get_single_user_json(user_id):
    s_user = User.query.get(user_id)
    if not s_user:
        return []
    s_user = s_user.get_json()
    return s_user

# update the fname of given user with given info. return True
def update_user_fname(user, fname):
    user.fname = fname
    db.session.add(user)
    db.session.commit()
    return True

# update the lname of given user with given info. return True
def update_user_lname(user, lname):
    user.lname = lname
    db.session.add(user)
    db.session.commit()
    return True

# update the fname and lname of given user id with given info. return True if updated, otherwise return False
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

# update the password of given user id with given info. return True if updated, otherwise return False
def update_user_password(id, password):
    user = get_user(id)
    flag = False
    if user:
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flag = user.check_password(password)
    return flag

# update the username of given id with given info. return True if updated, otherwise return False
def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        db.session.commit()
        return user
    return None

# get the courses associated with a staff id in json format. return the found course dict, otherwise return empty dict
def get_staff_courses(staff_id):
    staff = User.query.filter_by(id=staff_id).first()
    entries = []
    if not staff:
        return None
    for entry in staff.courses:
        entries.append(entry.get_json())
    return entries

# load the db with users parsed from specified csv file. only supports loading staff users
def parse_users():
    with open('users.csv', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)

        for row in csvreader:
            username = row[0]
            password = row[1]
            type = row[2]
            fname = row[3]
            lname = row[4]

            if type == 'staff':
                user = Staff(
                    username=username,
                    password=password
                )
                db.session.add(user)
                user = get_user_by_username(username)
                name = (fname, lname)
                update_user_name(user.id, name)
        db.session.commit()
