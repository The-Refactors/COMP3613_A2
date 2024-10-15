from App.models.course import *
from App.database import db

def create_course(courseCode, courseName, semester, year):
    newcourse = Course(courseCode=courseCode, courseName=courseName, semester=semester, year=year)
    db.session.add(newcourse)
    db.session.commit()
    return newcourse

def get_course_by_name(courseName):
    course = Course.query.filter_by(courseName=courseName).first()
    if not course:
        return None
    return course

def get_course_by_code(courseCode):
    course = Course.query.filter_by(courseCode=courseCode).first()
    if not course:
        return None
    return course

def get_courses_by_name(courseName):
    courses = Course.query.filter_by(courseName=courseName).all()
    if not courses:
        return None
    return courses

def get_courses_by_code(courseCode):
    courses = Course.query.filter_by(courseCode=courseCode).all()
    if not courses:
        return None
    return courses

def get_courses_by_semester(semester):
    courses = Course.query.filter_by(semester=semester).all()
    if not courses:
        return None
    return courses

def get_courses_by_year(year):
    courses = Course.query.filter_by(year=year).all()
    if not courses:
        return None
    return courses

def get_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return None
    return course

def get_course_json(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return None
    return course.get_json()

def get_course_staff(course_id):
    course =Course.query.filter_by(id=course_id).first()
    entries = []
    if not course:
        return None
    for entry in course.staffs:
        entries.append(entry.get_json())
    return entries

def get_all_courses_json():
    courses = Course.query.all()
    if not courses:
        return []
    courses = [course.get_json() for course in courses]
    return courses

def update_course(course_id, code, name, semester, year):
    course = get_course(course_id)
    if course:
        course.courseCode = code
        course.courseName = name
        course.semester = semester
        course.year = year
        db.session.add(course)
        db.session.commit()
        return course  # Return the updated course object
    return None