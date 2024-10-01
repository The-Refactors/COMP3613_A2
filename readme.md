#Flask Commands
#User Group Commands
##Create user
Creates a new user with the specified username, password and role(admin by default)

```bash
$ flask user create <username> <password> <role>
```

```python
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
```

##List users
Lists all user in the database(optionally as json format)

```bash
$ flask user list <format>
```

```python
@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())
```

##View allocated courses for a chosen user
Presents a list of non admin users in the database. A user id is input and a list of courses to which the user has been allocated is shown

```bash
$ flask user view
```

```python
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
```

##Update user’s name
Updates the username of the user given by the entered id to the new name given

```bash
$ flask user update-name <id> <newname>
```

```python
@user_cli.command("update-name", help="Updates username of given user")
@click.argument("id")
@click.argument("newname")
def update_user_name_command(id, newname):
    if update_user_name(id, newname):
        print(f'User {id} name changed to {newname}')
    else:
        print("Name unchanged")
```

##Update user’s role
Updates the role of the user given by the entered id to the new role given

```bash
$ flask user update-role <id> <newrole>
```

```python
@user_cli.command("update-role", help="Updates role of given user")
@click.argument("id")
@click.argument("newrole")
def update_user_role_command(id, newrole):
    if update_user_role(id, newrole):
        print(f'User {id} role changed to {newrole}')
    else:
        print("Role unchanged")
```

#Course Group Commands
##Create course
Creates a new course with the attributes specified

```bash
$ flask course create <courseCode> <courseName> <semester> <year>
```

```python
@course_cli.command("create", help="Creates a course")
@click.argument("courseCode", default="COMP3613")
@click.argument("courseName", default="Software Engineering II")
@click.argument("semester", default="1")
@click.argument("year", default="2024")
def create_course_command(coursecode, coursename, semester, year):
    create_course(coursecode, coursename, semester, year)
    print(f'{coursecode} - {coursename} created for {year} semester {semester}')
```

##List courses
Lists all courses in the database in json format

```bash
$ flask course list
```

```python
@course_cli.command("list", help="Lists courses in the database")
def list_course_command():
    print(get_all_courses_json())
```

##View allocated users to a course
Presents a list of courses in the database. A course id is input and a list of users to which the course has been allocated is shown

```bash
$ flask course view
```

```python
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
```

##Update course information
Presents a list of courses in the database. A course id is input and a selection of attributes is shown. The selection is input, then the new content of the attribute is entered

```bash
$ flask course update
```

```python
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
```

#Allocate Group Commands
##Allocate user to a course
Presents a list of non admin users in the database. A user id is input then a list of courses is shown. A course id is input which creates the allocation

```bash
$ flask allocate user
```

```python
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
```

##Allocate course to a user
Presents a list of courses in the database. A course id is input then a list of non admin users is shown. A user id is input which creates the allocation

```bash
$ flask allocate course
```

```python
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
```

##List allocations
List all allocations in the database in json format

```bash
$ flask allocate list
```

```python
@allocate_cli.command("list", help="Lists allocations in the database")
def list_allocate_command():
    allocations = get_all_allocates_json()
    print(allocations)
```

##Remove an allocation
Presents a list of all allocations in the database. An allocation id is input and the corresponding entry is deleted

```bash
$ flask allocate remove
```

```python
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
```
