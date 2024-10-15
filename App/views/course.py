from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from .index import index_views

from App.controllers import (
    create_course,
    get_course_by_name,
    get_course_by_code,
    get_course,
    get_all_courses_json,
    update_course,
    get_course_json,
    get_allocates_by_course_json,
    get_course_staff
)

# Create a Blueprint for the course routes
course_views = Blueprint('course_views', __name__, template_folder='../templates')


@course_views.route('/coursecreate', methods=['GET'])
@jwt_required()
def get_create_course_view():
    return jsonify({'message':'User at course creation page'}), 200


# Route to create a new course
@course_views.route('/coursecreate', methods=['POST'])
@jwt_required()
def create_new_course():
    data = request.json
    check = create_course(data.get('courseCode'), data.get('courseName'), data.get('semester'), data.get('year'))
    if check:
        return jsonify({'message': 'Course created successfully.', 'courseId': check.id}), 201
    else:
        return jsonify({'message': 'Course could not be created.'}), 400


@course_views.route('/courseedit', methods=['GET'])
@jwt_required()
def get_edit_course_view():
    return jsonify({'message':'User at course edit page'}), 200


@course_views.route('/courseedit/<int:id>', methods=['GET'])
@jwt_required()
def get_edit_specific_course_view(id):
    course = get_course_json(id)
    allocations = get_allocates_by_course_json(id)
    staff = get_course_staff(id)
    table_info = []
    for allocate in allocations:
        match = next(user for user in staff if user['id'] == allocate['staffId'])
        table_info.append({
            'staffId': allocate['staffId'],
            'role': allocate['role'],
            'fname': match['fname'],
            'lname': match['lname']
        })
    return jsonify({'course': course, 'allocations': table_info}), 200

@course_views.route('/courseedit', methods=['PUT'])
@jwt_required()
def edit_course():
    data = request.json
    check = update_course(data.get('id'), data.get('courseCode'), data.get('courseName'), data.get('semester'), data.get('year'))
    if check:
        return jsonify({'message': 'Course edited successfully.', 'courseId': check.id}), 201
    else:
        return jsonify({'message': 'Course could not be edited.'}), 400


# Route to get all courses
@course_views.route('/api/courses', methods=['GET'])
@jwt_required()
def get_all_courses_view():
    courses = get_all_courses_json()
    return jsonify(courses), 200


# Route to get a course by course code
@course_views.route('/code/<string:course_code>', methods=['GET'])
def get_course_by_code_view(course_code):
    course = get_course_by_code(course_code)
    if not course:
        return jsonify({'message': 'Course not found.'}), 404
    return jsonify(course.get_json()), 200


# Route to get a course by name
@course_views.route('/name/<string:course_name>', methods=['GET'])
def get_course_by_name_view(course_name):
    course = get_course_by_name(course_name)
    if not course:
        return jsonify({'message': 'Course not found.'}), 404
    return jsonify(course.get_json()), 200


# Route to update a course
@course_views.route('/<int:course_id>', methods=['PATCH'])
def update_course_view(course_id):
    data = request.json
    attribute = data.get('attribute')
    content = data.get('content')

    if not attribute or not content:
        return jsonify({'message': 'Attribute and content are required for update.'}), 400

    updated_course = update_course(course_id, attribute, content)
    if updated_course:
        return jsonify({'message': 'Course updated successfully.'}), 200
    else:
        return jsonify({'message': 'Course not found or update failed.'}), 404


# Route to get a single course by ID
@course_views.route('/<int:course_id>', methods=['GET'])
def get_course_view(course_id):
    course = get_course(course_id)
    if not course:
        return jsonify({'message': 'Course not found.'}), 404
    return jsonify(course.get_json()), 200


# Route to delete a course by ID
@course_views.route('/<int:course_id>', methods=['DELETE'])
def delete_course_view(course_id):
    course = get_course(course_id)
    if course:
        course.delete()
        return jsonify({'message': 'Course deleted successfully.'}), 200
    else:
        return jsonify({'message': 'Course not found.'}), 404
