from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies

from App.controllers import (
    get_allocates_by_staff_json,
    get_staff_courses
)

home_views = Blueprint('home_views', __name__, template_folder='../templates')

@home_views.route('/home', methods=['GET'])
@jwt_required()
def home_page():
    return jsonify({'message':'User at home page'})


@home_views.route('/staffhome/<int:id>', methods=['GET'])
@jwt_required()
def staff_home_page(id):
    allocations = get_allocates_by_staff_json(id)
    courses = get_staff_courses(id)
    table_info = []
    for allocate in allocations:
        match = next(course for course in courses if course['id'] == allocate['courseid'])
        table_info.append({
            'coursecode': match['coursecode'],
            'coursename': match['coursename'],
            'role': allocate['role']
        })
    return jsonify({'message': f'User {id} at staff home page', 'courses': table_info})