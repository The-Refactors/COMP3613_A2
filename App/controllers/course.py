from App.models.course import *
from App.database import db

def create_course(courseCode, courseName, semester, year):
    newcourse = Course(courseCode=courseCode, courseName=courseName, semester=semester, year=year)
    db.session.add(newcourse)
    db.session.commit()
    return newcourse

def get_course_by_name(courseName):
    return Course.query.filter_by(courseName=courseName).first()

def get_course_by_code(courseCode):
    return Course.query.filter_by(courseCode=courseCode).first()

def get_user(id):
    return User.query.get(id)
