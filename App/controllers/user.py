from App.models.user import *
from App.database import db

def create_user(username, password, role):
    if (role=='admin'):
        newuser = Admin(username=username, password=password)
    else:
        newuser = Staff(username=username, password=password, role=role)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_staff():
    return Staff.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def get_single_user_json(id):
    s_user = User.query.get(id)
    if not s_user:
        return []
    s_user = s_user.get_json()
    return s_user

def update_user_name(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        db.session.commit()
        return True
    return False

def update_user_role(id, newrole):
    user = get_user(id)
    if user:
        user.role = newrole
        db.session.add(user)
        db.session.commit()
        return True
    return False
