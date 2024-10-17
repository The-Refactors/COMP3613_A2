import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App import parse_users, parse_allocations
from App.database import db, get_migrate
from App.models import User, Course, Allocation

from App.controllers import (create_user, get_all_users_json, get_all_users, initialize, create_course,
                             get_all_courses_json, get_all_staff, get_single_user_json, get_user, get_course,
                             create_allocation, get_all_allocates_json, get_user_by_username, delete_allocate,
                             update_course, update_user, update_user_name, parse_courses, parse_users, parse_allocations)
from App.database import get_migrate
from App.main import create_app

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    parse_users()
    parse_courses()
    parse_allocations()
    print('database initialized')


'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the command
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands')


# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("type", default="admin")
@click.option("--fname", default="firstname")
@click.option("--lname", default="lastname")
def create_user_command(username, password, type, fname, lname):
    if get_user_by_username(username=username):
        print(f"{username} already exists")
        return
    create_user(username, password, type)
    print(f'{username} created with type {type}')
    user = get_user_by_username(username=username)
    name = [fname, lname]
    update_user_name(user.id, name)
    print(f'{username} name set to {fname} {lname}')


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
    course_list = [[course.coursecode, course.coursename, course.year, course.semester] for course in
                   staff_member.courses]
    print(course_list)


@user_cli.command("update", help="Updates name(s) of given user")
@click.argument("id")
@click.option("--username")
@click.option("--fname")
@click.option("--lname")
def update_user_command(id, username, fname, lname):
    if username:
        if update_user(id, username):
            print(f'User {id} username changed to {username}')
        else:
            print("Username unchanged")
    if fname or lname:
        name = [fname, lname]
        if update_user_name(id, name):
            print(f'User {id} name changed')
        else:
            print(f'User {id} name unchanged')


app.cli.add_command(user_cli)
# add the group to the cli

# create a course cli group
course_cli = AppGroup('course', help='Course object commands')


@course_cli.command("create", help="Creates a course")
@click.argument("coursecode", default="COMP3613")
@click.argument("coursename", default="Software Engineering II")
@click.argument("semester", default="1", type=int)
@click.argument("year", default="2024", type=int)
def create_course_command(coursecode, coursename, semester, year):
    create_course(coursecode, coursename, semester, year)
    print(f'{coursecode} - {coursename} created for {year} semester {semester}')


@course_cli.command("list", help="Lists courses in the database")
def list_course_command():
    print(get_all_courses_json())


@course_cli.command("view", help="Lists all staff allocated to course")
def view_course_allocates_command():
    courses = get_all_courses_json()
    print(courses)
    course_id = click.prompt("Please enter the ID of the course", type=int)
    selected_course = get_course(course_id)
    if not selected_course:
        print("Invalid course ID. Exiting...")
        return
    staff_list = [[staff.username, staff.role] for staff in selected_course.staffs]
    print(staff_list)


@course_cli.command("update", help="Updates the content of a course entry")
@click.option("--id")
@click.option("--code")
@click.option("--name")
@click.option("--semester", type=int)
@click.option("--year", type=int)
def update_course_command(id, code, name, semester, year):
    if not id:
        course_list = get_all_courses_json()
        print(course_list)
        id = click.prompt("Please enter the ID of the course", type=int)
    selected_course = get_course(id)
    if not selected_course:
        print("Invalid course ID. Exiting...")
        return
    if not code:
        code = click.prompt("Please enter the new code", type=str, default=selected_course.coursecode)
    if not name:
        name = click.prompt("Please enter the new name", type=str, default=selected_course.coursename)
    if not semester:
        semester = click.prompt("Please enter the new semester", type=int, default=selected_course.semester)
    if not year:
        year = click.prompt("Please enter the new year", type=int, default=selected_course.year)
    update_course(id, code, name, semester, year)
    print(selected_course.get_json())


app.cli.add_command(course_cli)
# add the group to the cli

# create an allocate cli group
allocate_cli = AppGroup('allocate', help='Allocation object commands')


@allocate_cli.command("create", help="Allocates a user to a course with a role")
@click.option("--courseid", type=int)
@click.option("--staffid", type=int)
@click.option("--role")
def create_allocate_user_command(courseid, staffid, role):
    if not courseid:
        course_list = get_all_courses_json()
        print(course_list)
        courseid = click.prompt("Please enter the ID of the course", type=int)
    selected_course = get_course(courseid)
    if not selected_course:
        print("Invalid course ID. Exiting...")
        return

    staff_members = get_all_staff()
    if not staffid:
        for staff in staff_members:
            json = get_single_user_json(staff.id)
            print(json)
        staffid = click.prompt("Please enter the ID of the staff member", type=int)
    selected_staff = get_user(staffid)
    if not selected_staff in staff_members:
        print("Invalid staff ID. Exiting...")
        return

    if not role in ["lecturer", "tutor", "teaching assistant"]:
        role = click.prompt("Select the staff member's role for the course:\n1.'lecturer'\n2.'tutor'\n3.'teaching assistant'",
                            type=int)
        if role == 1:
            role = "lecturer"
        elif role == 2:
            role = "tutor"
        elif role == 3:
            role = "teaching assistant"
        else:
            print("Invalid role. Exiting...")
            return

    newallocate = create_allocation(courseid, staffid, role)
    if newallocate:
        print(f'{selected_staff.username} allocated to {selected_course.coursecode} as {newallocate.role}')
    else:
        print(f'{selected_staff.username} was not allocated to {selected_course.coursecode} as {newallocate.role}')


@allocate_cli.command("list", help="Lists allocations in the database")
def list_allocate_command():
    allocations = get_all_allocates_json()
    print(allocations)


@allocate_cli.command("remove", help="Removes allocation entry from database")
@click.option("--id", type=int)
def rem_allocate_command(id):
    allocations = get_all_allocates_json()
    if not allocations:
        print("No allocations")
        return
    if not id:
        print(allocations)
        id = click.prompt("Please enter the ID of the allocation", type=int)
    if not delete_allocate(id):
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