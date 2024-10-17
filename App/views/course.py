from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from .index import index_views

from App.controllers import (
    create_course,
    get_all_courses_json,
    update_course,
    get_course_json,
    get_allocates_by_course_json,
    get_course_staff
)

# Create a Blueprint for the course routes
course_views = Blueprint('course_views', __name__, template_folder='../templates')

# Route to retrieve page for creating a new course
@course_views.route('/coursecreate', methods=['GET'])
@jwt_required()
def get_create_course_view():
    return jsonify({'message':'User at course creation page'}), 200


# Route to create a new course with inputted form data
@course_views.route('/coursecreate', methods=['POST'])
@jwt_required()
def create_new_course():
    data = request.form
    coursecode = data['coursecode']
    coursename = data['coursename']
    semester = data['semester']
    year = data['year']
    check = create_course(coursecode, coursename, semester, year)
    if check:
        return jsonify({'message': 'Course created successfully.', 'courseId': check.id}), 201
    else:
        return jsonify({'message': 'Course could not be created.'}), 400

# Route to retrieve page for updating a course's info
@course_views.route('/courseedit', methods=['GET'])
@jwt_required()
def get_edit_course_view():
    return jsonify({'message':'User at course edit page'}), 200

# Route to retrieve page for updating a specified courseid's info
@course_views.route('/courseedit/<int:id>', methods=['GET'])
@jwt_required()
def get_edit_specific_course_view(id):
    course = get_course_json(id)
    allocations = get_allocates_by_course_json(id)
    staff = get_course_staff(id)
    table_info = []
    for allocate in allocations:
        match = next((user for user in staff if user['id'] == allocate['staffid']), None)
        if match:
            table_info.append({
                'staffid': allocate['staffid'],
                'role': allocate['role'],
                'fname': match['fname'],
                'lname': match['lname']
            })
    return jsonify({'course': course, 'allocations': table_info}), 200

# Route to update a course's info with inputted form data
@course_views.route('/courseedit', methods=['PUT'])
@jwt_required()
def edit_course():
    data = request.form
    id = data['id']
    coursecode = data['coursecode']
    coursename = data['coursename']
    semester = data['semester']
    year = data['year']
    check = update_course(id, coursecode, coursename, semester, year)
    if check:
        return jsonify({'message': 'Course edited successfully.', 'courseId': check.id}), 200
    else:
        return jsonify({'message': 'Course could not be edited.'}), 400


# Route to retrieve page for a list of all courses in db in json format
@course_views.route('/api/courses', methods=['GET'])
@jwt_required()
def get_all_courses_view():
    courses = get_all_courses_json()
    return jsonify(courses), 200
