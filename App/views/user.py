from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user, current_user

from.index import index_views

from App.controllers import (
    verify_type_fail,
    create_user,
    get_all_users,
    get_all_users_json,
    update_user_name,
    get_single_user_json,
    get_allocates_by_staff_json,
    get_staff_courses,
    update_user,
    update_user_password
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

# Route to retrieve page for creating a new user
@user_views.route('/usercreate', methods=['GET'])
@jwt_required()
def get_create_user_view():
    verify = verify_type_fail(current_user, 'admin')
    if verify:
        return verify
    return jsonify({'message':'User at user creation page'}), 200

# Route to create a new user with inputted form data
@user_views.route('/usercreate', methods=['POST'])
@jwt_required()
def create_new_user():
    verify = verify_type_fail(current_user, 'admin')
    if verify:
        return verify
    data = request.form
    username = data['username']
    password = data['password']
    type = data['type']
    fname = data['fname']
    lname = data['lname']
    check = create_user(username, password, type)
    if check:
        name = (fname, lname)
        update_user_name(check.id, name)
        return jsonify({'message': f'User created with id {check.id}'}), 201
    else:
        return jsonify({'message': 'User could not be created.'}), 400

# Route to retrieve page for updating a user's info
@user_views.route('/useredit', methods=['GET'])
@jwt_required()
def get_edit_user_view():
    verify = verify_type_fail(current_user, 'admin')
    if verify:
        return verify
    return jsonify({'message':'User at user edit page'}), 200

# Route to retrieve page for updating a specified userid's info
@user_views.route('/useredit/<int:id>', methods=['GET'])
@jwt_required()
def get_edit_specific_user_view(id):
    verify = verify_type_fail(current_user, 'admin')
    if verify:
        return verify
    user = get_single_user_json(id)
    allocations = get_allocates_by_staff_json(id)
    courses = get_staff_courses(id)
    table_info = []
    for allocate in allocations:
        match = next(course for course in courses if course['id'] == allocate['courseid'])
        table_info.append({
            'courseid': allocate['courseid'],
            'role': allocate['role'],
            'coursecode': match['coursecode'],
            'coursename': match['coursename']
        })
    return jsonify({'user': user, 'allocations': table_info}), 200

# Route to update a user's info with inputted form data
@user_views.route('/useredit', methods=['PUT'])
@jwt_required()
def edit_user():
    verify = verify_type_fail(current_user, 'admin')
    if verify:
        return verify
    data = request.form
    id = data['id']
    password = request.form.get('password')
    pass_flag = False
    if password:
        pass_flag = update_user_password(id, password)
    username = data['username']
    fname = data['fname']
    lname = data['lname']
    check = update_user(id, username)
    name = (fname, lname)
    if check:
        update_user_name(id, name)
        if pass_flag:
            return jsonify({'message': f'User {check.id} info and password edited successfully.'}), 200
        return jsonify({'message': f'User {check.id} info edited successfully.'}), 200
    else:
        return jsonify({'message': f'User {check.id} could not be edited.'}), 400

# Route to update a user's password with inputted form data
@user_views.route('/userpassedit/<int:id>', methods=['PUT'])
@jwt_required()
def edit_user_password(id):
    if current_user.id != id:
        return jsonify({'message': f'User {current_user.id} does not have access to this page'}), 403
    password = request.form.get('password')
    check = False
    if password:
        check = update_user_password(id, password)
    if check:
        return jsonify({'message': f'User {current_user.id} password edited successfully.'}), 200
    else:
        return jsonify({'message': f'User {current_user.id} password could not be edited.'}), 400

# Route to update a user's password with inputted form data
@user_views.route('/userpassedit/<int:id>', methods=['GET'])
@jwt_required()
def get_update_password_view(id):
    if current_user.id != id:
        return jsonify({'message': f'User {current_user.id} does not have access to this page'}), 403
    return jsonify({'message': f'User {current_user.id} at password edit page.'}), 200


@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)


@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'], data['type'])
    return redirect(url_for('user_views.get_user_page'))


@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    user = create_user(data['username'], data['password'], data['type'])
    return jsonify({'message': f"user {user.username} created with id {user.id}"})

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')