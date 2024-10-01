import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Course, Allocation
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, )


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
    create_user(username, password, role)
    print(f'{username} created with role {role}')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli


course_cli = AppGroup('course', help='User object commands')

@user_cli.command("create", help="Creates a course")
@click.argument("courseCode", default="COMP3613")
@click.argument("courseName", default="Software Engineering II")
@click.argument("semester", default="1")
@click.argument("year", default="2024")
def create_course_command(courseCode, courseName, semester, year):
    create_course(courseCode, courseName, semester, year)
    print(f'{courseCode} - {courseName} created for {year} semester {semester}')

app.cli.add_command(course_cli) # add the group to the cli

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