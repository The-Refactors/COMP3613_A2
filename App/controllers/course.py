from App.models.course import *
from App.database import db
import csv

# create a course. return the new course object, otherwise return false
def create_course(coursecode, coursename, semester, year):
    course_check = Course.query.filter_by(coursecode=coursecode, coursename=coursename, semester=semester, year=year).first()
    if not course_check:
        newcourse = Course(coursecode=coursecode, coursename=coursename, semester=semester, year=year)
        db.session.add(newcourse)
        db.session.commit()
        return newcourse
    return False

# def get_course_by_name(coursename):
#     course = Course.query.filter_by(coursename=coursename).first()
#     if not course:
#         return None
#     return course
#
# def get_course_by_code(coursecode):
#     course = Course.query.filter_by(coursecode=coursecode).first()
#     if not course:
#         return None
#     return course
#
# def get_courses_by_name(coursename):
#     courses = Course.query.filter_by(coursename=coursename).all()
#     if not courses:
#         return None
#     return courses
#
# def get_courses_by_code(coursecode):
#     courses = Course.query.filter_by(coursecode=coursecode).all()
#     if not courses:
#         return None
#     return courses
#
# def get_courses_by_semester(semester):
#     courses = Course.query.filter_by(semester=semester).all()
#     if not courses:
#         return None
#     return courses
#
# def get_courses_by_year(year):
#     courses = Course.query.filter_by(year=year).all()
#     if not courses:
#         return None
#     return courses

# get the course with specified id. return the found course object, otherwise return None
def get_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return None
    return course

# get course with specified id in json format. return the found course dict, otherwise return None
def get_course_json(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return None
    return course.get_json()

# get the staff list associated with a course id. return the found staff list, otherwise return None
def get_course_staff(course_id):
    course =Course.query.filter_by(id=course_id).first()
    entries = []
    if not course:
        return None
    for entry in course.staffs:
        entries.append(entry.get_json())
    return entries

# get all courses in db in json format. return a dict of entries, otherwise return empty dict
def get_all_courses_json():
    courses = Course.query.all()
    if not courses:
        return []
    courses = [course.get_json() for course in courses]
    return courses

# update the course of given id with given info. return updated course object, otherwise return None
def update_course(course_id, code, name, semester, year):
    course = get_course(course_id)
    if course:
        course.coursecode = code
        course.coursename = name
        course.semester = semester
        course.year = year
        db.session.add(course)
        db.session.commit()
        return course  # Return the updated course object
    return None

# load the db with courses parsed from specified csv file
def parse_courses():
    with open('courses.csv', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)

        for row in csvreader:
            coursecode = row[0]
            coursename = row[1]
            semester = row[2]
            year = row[3]

            course = Course(
                coursecode=coursecode,
                coursename=coursename,
                semester=semester,
                year=year
            )
            db.session.add(course)
        db.session.commit()

