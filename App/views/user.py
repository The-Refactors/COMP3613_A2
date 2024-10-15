from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    update_user_name
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
    data = request.json
    check = create_user(data.get('username'), data.get('password'), data.get('position'))
    if check:
        name = (data.get('fname'), data.get('lname'))
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
    return jsonify(user, allocations, courses), 200
    # return jsonify({'message':'User at course edit page for particular course', 'courseId': course.id}), 200


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