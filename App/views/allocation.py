from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views
from App.controllers import (
    create_allocation,
    get_all_allocates_json,
    get_allocates_by_staff,
    get_allocate,
    delete_allocate
)

# Create a Blueprint for the allocation routes
allocation_views = Blueprint('allocation_views', __name__, url_prefix='/allocations')

# Route to create a new allocation
@allocation_views.route('/', methods=['POST'])
def create_allocation_view():
    data = request.json
    course_id = data.get('course_id')
    staff_id = data.get('staff_id')
    
    if not course_id or not staff_id:
        return jsonify({'message': 'Course ID and Staff ID are required.'}), 400
    
    success = create_allocation(course_id, staff_id)
    if success:
        return jsonify({'message': 'Allocation created successfully.'}), 201
    else:
        return jsonify({'message': 'Allocation already exists.'}), 409

# Route to get all allocations
@allocation_views.route('/', methods=['GET'])
def get_all_allocations_view():
    allocations = get_all_allocates_json()
    return jsonify(allocations), 200

# Route to get allocations by staff ID
@allocation_views.route('/staff/<int:staff_id>', methods=['GET'])
def get_allocations_by_staff_view(staff_id):
    allocations = get_allocates_by_staff(staff_id)
    if not allocations:
        return jsonify({'message': 'No allocations found for this staff member.'}), 404
    allocations_json = [allocation.get_json() for allocation in allocations]
    return jsonify(allocations_json), 200

# Route to get a single allocation by ID
@allocation_views.route('/<int:id>', methods=['GET'])
def get_allocation_view(id):
    allocation = get_allocate(id)
    if not allocation:
        return jsonify({'message': 'Allocation not found.'}), 404
    return jsonify(allocation.get_json()), 200

# Route to delete an allocation by ID
@allocation_views.route('/<int:id>', methods=['DELETE'])
def delete_allocation_view(id):
    success = delete_allocate(id)
    if success:
        return jsonify({'message': 'Allocation deleted successfully.'}), 200
    else:
        return jsonify({'message': 'Allocation not found.'}), 404
