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

def get_course(id):
    return Course.query.get(id)

def get_all_courses_json():
    courses = Course.query.all()
    if not courses:
        return []
    courses = [course.get_json() for course in courses]
    return courses

def update_course(id, attribute, content):
    course = get_course(id)
    if course:
        if attribute in [1]:
            course.courseCode = content
        elif attribute in [2]:
            course.courseName = content
        elif attribute in [3]:
            course.semester = content
        elif attribute in [4]:
            course.year = content
        db.session.add(course)
        return db.session.commit()
    return None