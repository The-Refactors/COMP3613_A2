from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user, current_user

from.index import index_views
from App.controllers import (
    verify_type_fail,
    create_allocation,
    get_all_allocates_json,
    delete_allocate,
    get_all_staff_json,
    get_all_courses_json
)

# Create a Blueprint for the allocation routes
allocation_views = Blueprint('allocation_views', __name__, template_folder='../templates')

# Route to retrieve page for creating allocations
@allocation_views.route('/allocationcreate', methods=['GET'])
@jwt_required()
def get_create_allocations_view():
    fail_verify = verify_type_fail(current_user, 'admin')
    if fail_verify:
        return fail_verify
    return jsonify({'message': f'User {current_user.id} at allocation creation page'}), 200

# Route to page to create an allocation with inputted form data
@allocation_views.route('/allocationcreate', methods=['POST'])
@jwt_required()
def create_new_allocation():
    fail_verify = verify_type_fail(current_user, 'admin')
    if fail_verify:
        return fail_verify
    data = request.form
    courseid = data['courseid']
    staffid = data['staffid']
    role = data['role']
    check = create_allocation(courseid, staffid, role)
    if check:
        return jsonify({'message': f'Allocation created with id {check.id}'}), 201
    else:
        return jsonify({'message': 'Allocation could not be created'}), 400

# Route to retrieve page for a list of all allocations in db in json format
@allocation_views.route('/api/allocations', methods=['GET'])
@jwt_required()
def get_all_allocations_view():
    fail_verify = verify_type_fail(current_user, 'admin')
    if fail_verify:
        return fail_verify
    allocations = get_all_allocates_json()
    return jsonify(allocations), 200

# Route to retrieve page for listing all allocation info
@allocation_views.route('/allocationedit', methods=['GET'])
@jwt_required()
def get_edit_allocation_view():
    fail_verify = verify_type_fail(current_user, 'admin')
    if fail_verify:
        return fail_verify
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
    fail_verify = verify_type_fail(current_user, 'admin')
    if fail_verify:
        return fail_verify
    success = delete_allocate(id)
    if success:
        return jsonify({'message': f'Allocation {id} deleted successfully'}), 200
    return jsonify({'message': f'Allocation {id} not found'}), 404