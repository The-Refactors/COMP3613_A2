import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Course, Allocation
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, create_course, get_all_courses_json, create_allocation, get_all_staff, get_single_user_json, get_user, get_course, create_allocation, get_all_allocates_json, get_user_by_username, get_allocates_by_staff, get_allocate, delete_allocate, update_course, update_user_name, update_user_role )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("role", default="admin")
def create_user_command(username, password, role):
    if get_user_by_username(username=username):
        print(f"{username} already exists")
        return
    create_user(username, password, role)
    print(f'{username} created with role {role}')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

@user_cli.command("view", help="Lists all courses allocated to a user")
def view_user_allocates_command():
    staff_members = get_all_staff()
    for staff in staff_members:
        json = get_single_user_json(staff.id)
        print(json)
    staff_id = click.prompt("Please enter the ID of the user", type=int)
    staff_member = get_user(staff_id)
    if not staff_member in staff_members:
        print("Invalid user ID. Exiting...")
        return
    course_list = [[course.courseCode, course.courseName, course.year, course.semester] for course in staff_member.courses]
    print(course_list)

@user_cli.command("update-name", help="Updates username of given user")
@click.argument("id")
@click.argument("newname")
def update_user_name_command(id, newname):
    if update_user_name(id, newname):
        print(f'User {id} name changed to {newname}')
    else:
        print("Name unchanged")

@user_cli.command("update-role", help="Updates role of given user")
@click.argument("id")
@click.argument("newrole")
def update_user_role_command(id, newrole):
    if update_user_role(id, newrole):
        print(f'User {id} role changed to {newrole}')
    else:
        print("Role unchanged")


app.cli.add_command(user_cli) 
# add the group to the cli

# create a course cli group
course_cli = AppGroup('course', help='User object commands')

@course_cli.command("create", help="Creates a course")
@click.argument("courseCode", default="COMP3613")
@click.argument("courseName", default="Software Engineering II")
@click.argument("semester", default="1")
@click.argument("year", default="2024")
def create_course_command(coursecode, coursename, semester, year):
    create_course(coursecode, coursename, semester, year)
    print(f'{coursecode} - {coursename} created for {year} semester {semester}')

@course_cli.command("list", help="Lists courses in the database")
def list_course_command():
    print(get_all_courses_json())

@course_cli.command("view", help="Lists all staff allocated to course")
def view_course_allocates_command():
    courses = get_all_courses_json()
    print (courses)
    course_id = click.prompt("Please enter the ID of the course", type=int)
    selected_course = get_course(course_id)
    if not selected_course:
        print("Invalid course ID. Exiting...")
        return
    staff_list = [[staff.username, staff.role] for staff in selected_course.staffs]
    print(staff_list)

@course_cli.command("update", help="Updates the content of a course entry")
def update_course_command():
    course_list = get_all_courses_json()
    print(course_list)
    course_id = click.prompt("Please enter the ID of the course", type=int)
    selected_course = get_course(course_id)
    if not selected_course:
        print("Invalid course ID. Exiting...")
        return
    attribute = click.prompt("1. Course Code\n2. Course Name\n3. Semester\n4. Year\nPlease select which attribute to update", type=int)
    if attribute in [1]:
        content = click.prompt("Please enter the new code", type=str)
    elif attribute in [2]:
        content = click.prompt("Please enter the new name", type=str)
    elif attribute in [3]:
        content = click.prompt("Please enter the new semester", type=int)
    elif attribute in [4]:
        content = click.prompt("Please enter the new year", type=int)
    else:
        print("Invalid selection")
        return
    update_course(course_id, attribute, content)
    print(selected_course.get_json())

app.cli.add_command(course_cli)
# add the group to the cli

# create an allocate cli group
allocate_cli = AppGroup('allocate', help='User object commands')

@allocate_cli.command("user", help="Allocates a user to a course")
def create_allocate_user_command():
    staff_members = get_all_staff()
    for staff in staff_members:
        json = get_single_user_json(staff.id)
        print(json)

    staff_id = click.prompt("Please enter the ID of the staff member", type=int)
    selected_staff = get_user(staff_id)
    if not selected_staff in staff_members:
        print("Invalid staff ID. Exiting...")
        return

    courses = get_all_courses_json()
    print (courses)
    course_id = click.prompt("Please enter the ID of the course", type=int)
    selected_course = get_course(course_id)
    if not selected_course:
        print("Invalid course ID. Exiting...")
        return
    
    if create_allocation(selected_course.id, selected_staff.id):
        print(f'{selected_staff.username} allocated to {selected_course.courseCode}')
    else:
        print(f'{selected_staff.username} was not allocated to {selected_course.courseCode}')

@allocate_cli.command("course", help="Allocates a course to a user")
def create_allocate_course_command():
    courses = get_all_courses_json()
    print (courses)
    course_id = click.prompt("Please enter the ID of the course", type=int)
    selected_course = get_course(course_id)
    if not selected_course:
        print("Invalid course ID. Exiting...")
        return

    staff_members = get_all_staff()
    for staff in staff_members:
        json = get_single_user_json(staff.id)
        print(json)

    staff_id = click.prompt("Please enter the ID of the staff member", type=int)
    selected_staff = get_user(staff_id)
    if not selected_staff in staff_members:
        print("Invalid staff ID. Exiting...")
        return

    if create_allocation(selected_course.id, selected_staff.id):
        print(f'{selected_staff.username} allocated to {selected_course.courseCode}')
    else:
        print(f'{selected_staff.username} was not allocated to {selected_course.courseCode}')
    
@allocate_cli.command("list", help="Lists allocations in the database")
def list_allocate_command():
    allocations = get_all_allocates_json()
    print(allocations)

@allocate_cli.command("remove", help="Removes allocation entry from database")
def rem_allocate_command():
    allocations = get_all_allocates_json()
    if not allocations:
        print("No allocations")
        return
    print(allocations)
    allocate_id = click.prompt("Please enter the ID of the allocation", type=int)
    if not delete_allocate(allocate_id):
        print("Invalid allocation ID. Exiting...")
    else:
        print("Allocation removed")


app.cli.add_command(allocate_cli)
# add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)