from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views
from App.controllers import (
    create_allocation,
    get_all_allocates_json,
    delete_allocate,
    get_all_staff_json,
    get_all_courses_json
)

# Create a Blueprint for the allocation routes
allocation_views = Blueprint('allocation_views', __name__, template_folder='../templates')


@allocation_views.route('/allocationcreate', methods=['GET'])
@jwt_required()
def get_create_allocations_view():
    return jsonify({'message':'User at allocation creation page'}), 200


@allocation_views.route('/allocationcreate', methods=['POST'])
@jwt_required()
def create_new_allocation():
    data = request.form
    courseid = data['courseid']
    staffid = data['staffid']
    role = data['role']
    check = create_allocation(courseid, staffid, role)
    if check:
        return jsonify({'message': 'Allocation created successfully.', 'ID': check.id}), 201
    else:
        return jsonify({'message': 'Allocation could not be created.'}), 400


@allocation_views.route('/api/allocations', methods=['GET'])
@jwt_required()
def get_all_allocations_view():
    allocations = get_all_allocates_json()
    return jsonify(allocations), 200


@allocation_views.route('/allocationedit', methods=['GET'])
@jwt_required()
def get_edit_allocation_view():
    allocations = get_all_allocates_json()
    courses = get_all_courses_json()
    staff = get_all_staff_json()
    table_info = []
    for allocate in allocations:
        match_course = next((course for course in courses if course['id'] == allocate['courseid']), None)
        match_staff = next((user for user in staff if user['id'] == allocate['staffid']), None)
        if match_course and match_staff:
            table_info.append({
                'allocationid': allocate['id'],
                'courseid': allocate['courseid'],
                'staffid': allocate['staffid'],
                'role': allocate['role'],
                'coursecode': match_course['coursecode'],
                'coursename': match_course['coursename'],
                'semester': match_course['semester'],
                'year': match_course['year'],
                'fname': match_staff['fname'],
                'lname': match_staff['lname']
            })
    return jsonify(table_info), 200

# Route to delete an allocation by ID
@allocation_views.route('/allocationdelete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_allocation_view(id):
    success = delete_allocate(id)
    if success:
        return jsonify({'message':'Allocation deleted successfully'}), 200
    return jsonify({'message': 'Allocation not found'}), 404