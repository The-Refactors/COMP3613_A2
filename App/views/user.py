from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    update_user_name,
    get_single_user_json,
    get_allocates_by_staff_json,
    get_staff_courses,
    update_user
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/usercreate', methods=['GET'])
@jwt_required()
def get_create_user_view():
    return jsonify({'message':'User at user creation page'}), 200

# Route to create a new user
@user_views.route('/usercreate', methods=['POST'])
@jwt_required()
def create_new_user():
    data = request.form
    username = data['username']
    password = data['password']
    position = data['position']
    fname = data['fname']
    lname = data['lname']
    check = create_user(username, password, position)
    if check:
        name = (fname, lname)
        update_user_name(check.id, name)
        return jsonify({'message': 'User created successfully.', 'userId': check.id}), 201
    else:
        return jsonify({'message': 'User could not be created.'}), 400

@user_views.route('/useredit', methods=['GET'])
@jwt_required()
def get_edit_user_view():
    return jsonify({'message':'User at user edit page'}), 200

@user_views.route('/useredit/<int:id>', methods=['GET'])
@jwt_required()
def get_edit_specific_user_view(id):
    user = get_single_user_json(id)
    allocations = get_allocates_by_staff_json(id)
    courses = get_staff_courses(id)
    table_info = []
    for allocate in allocations:
        match = next(course for course in courses if course['id'] == allocate['courseId'])
        table_info.append({
            'courseId': allocate['courseId'],
            'role': allocate['role'],
            'coursecode': match['coursecode'],
            'coursename': match['coursename']
        })
    return jsonify({'user': user, 'allocations': table_info}), 200

@user_views.route('/useredit', methods=['PUT'])
@jwt_required()
def edit_user():
    data = request.form
    id = data['id']
    username = data['username']
    fname = data['fname']
    lname = data['lname']
    check = update_user(id, username)
    name = (fname, lname)
    if check:
        update_user_name(id, name)
        return jsonify({'message': 'User edited successfully.', 'userId': check.id}), 200
    else:
        return jsonify({'message': 'User could not be edited.'}), 400


@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)


@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))


@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    user = create_user(data['username'], data['password'])
    return jsonify({'message': f"user {user.username} created with id {user.id}"})

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')