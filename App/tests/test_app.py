import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash


from App.main import create_app
from App.database import db, create_db
from App.models import Admin, Staff, Course, Allocation
from App.controllers import (
    # Course Testing
    # get_course_by_name,
    # get_course_by_code,
    get_course,
    create_course,
    get_all_courses_json,
    update_course,
    # Allocation Testing
    # get_all_allocates_json,
    create_allocation,
    get_allocates_by_staff,
    delete_allocate,
    get_allocate,
    # User Testing
    create_user,
    update_user,
    get_user
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''

class CourseUnitTests(unittest.TestCase):

    # Test to create a new course with specific attributes
    def test_new_course(self):
        course = Course("CS101", "Intro to CS", 1, 2024)
        assert course.courseCode == "CS101"
        assert course.courseName == "Intro to CS"
        assert course.semester == 1
        assert course.year == 2024

    # Test to ensure json format shows all attributes correctly for course
    def test_get_json(self):
        course = Course("CS101", "Intro to CS", 1, 2024)
        course_json = course.get_json()
        self.assertDictEqual(course_json, {
        "id": None,
        "coursecode": "CS101",
        "coursename": "Intro to CS",
        "semester": 1,
        "year": 2024
    })

class AllocationUnitTests(unittest.TestCase):

    # Test to create a new allocation
    def test_new_allocation(self):
        allocation = Allocation(1, 2, 'lecturer')
        assert allocation.course_id == 1
        assert allocation.staff_id == 2
        assert allocation.role == "lecturer"

    # Test to ensure json format shows all attributes correctly for allocation
    def test_get_json(self):
        allocation = Allocation(1, 2, 'lecturer')
        allocation_json = allocation.get_json()
        self.assertDictEqual(allocation_json, {
            "id": None,
            "courseId": 1,
            "staffId": 2,
            "role": "lecturer"
        })

class UserUnitTests(unittest.TestCase):

    # Test to create a new admin user
    def test_new_user_admin(self):
        user = Admin('tom', 'tompass', 'admin')
        assert user.username == 'tom'
        assert user.type == 'admin'

    # Test to create a new staff user
    def test_new_user_staff(self):
        user = Staff('tom', 'tompass', 'staff')
        assert user.username == 'tom'
        assert user.type == 'staff'

    # Test to ensure json format shows all attributes correctly for user
    def test_get_json(self):
        user = Admin('cam', 'campass', 'admin')
        user_json = user.get_json()
        self.assertDictEqual(user_json, {
            "id": None,
            "username": "cam",
            "fname": None,
            "lname": None,
            "position": 'admin'
        })

    # Test to ensure passwords are hashed
    def test_hashed_password(self):
        user = Staff('meg', 'megpass', 'staff')
        user.set_password('newpass')
        assert user.password != 'newpass'

    # Test to ensure passwords are checked correctly despite hashing
    def test_check_password(self):
        user = Staff('tim', 'timpass', 'staff')
        check = user.check_password('timpass')
        assert check == True

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and reused for all methods in the class
@pytest.fixture(autouse=True, scope="class")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class CourseIntegrationTests(unittest.TestCase):

    # Test to create a new course and check info is stored correctly
    def test_create_course(self):
        create_course("CS101", "Data Structures", 1, 2024)
        course = get_course(1)
        assert course.courseCode == "CS101"
        assert course.courseName == "Data Structures"

    # def test_get_course_by_code(self):
    #     course = create_course("CS103", "Algorithms", 2, 2025)
    #     fetched_course = get_course_by_code("CS103")
    #     assert fetched_course.courseName == "Algorithms"

    # Test to check retrieval of courses is correct
    def test_get_all_courses_json(self):
        courses_json = get_all_courses_json()
        self.assertIsInstance(courses_json, list)
        assert len(courses_json) == 1

    # Test to update a course's info and check info is stored correctly
    def test_update_course(self):
        course = create_course("CS102", "Operating Systems", 1, 2024)
        updated_course = update_course(course.id, "CS102","Advanced OS", 1, 2024)
        assert updated_course.courseName == "Advanced OS"


class AllocationIntegrationTests(unittest.TestCase):

    # Test to create an allocation and check info is stored correctly
    def test_create_allocation(self):
        course = create_course("CS101", "Database Systems", 1, 2024)
        staff = create_user('tom', 'tompass', 'staff')
        create_allocation(course.id, staff.id, 'lecturer').get_json()
        result = get_allocate(1)
        assert result.id == 1
        assert result.course_id == 1
        assert result.staff_id == 1
        assert result.role == "lecturer"

    # Test to check retrieval of allocations is correct
    def test_get_allocates_by_staff(self):
        course = create_course("CS102", "Networking", 1, 2024)
        staff = create_user('jane', 'janepass', 'staff')
        create_allocation(course.id, staff.id, 'lecturer')
        allocations = get_allocates_by_staff(staff.id)
        assert len(allocations) == 1

    # Test to delete an allocation
    def test_delete_allocate(self):
        # Create course and staff to be used in this test
        course = create_course("CS103", "Software Engineering", 1, 2024)
        staff = create_user('joe', 'joepass', 'staff')

        # Fetch allocations before creation
        allocations_before_create = get_allocates_by_staff(staff.id)
        print(f"Allocations before creation: {allocations_before_create}")  # Debug line

        # Create allocation
        allocation = create_allocation(course.id, staff.id, 'lecturer')

        # Check if a new allocation was created
        allocations_after_create = get_allocates_by_staff(staff.id)
        self.assertGreater(len(allocations_after_create), len(allocations_before_create), "No allocations were created")

        # Delete the allocation using the fetched ID
        result = delete_allocate(allocation.id)
        self.assertTrue(result, "Allocation deletion failed")

        # Fetch allocations again after deletion
        allocations_after_delete = get_allocates_by_staff(staff.id)
        print(f"Allocations after deletion: {allocations_after_delete}")  # Debug line

        # Check if a new allocation still exists
        self.assertLess(allocations_after_delete, allocations_after_create, "Allocation still exists after deletion")


class UserIntegrationTests(unittest.TestCase):

    # Test to create an admin user and check info is stored correctly
    def test_create_user_admin(self):
        create_user('harry', 'harrypass', 'admin')
        user = get_user(1)
        assert user.username == 'harry'
        assert user.type == 'admin'

    # Test to create a staff user and check info is stored correctly
    def test_create_user_staff(self):
        create_user('tom', 'tompass', 'staff')
        user = get_user(2)
        assert user.username == 'tom'
        assert user.type == 'staff'

    # Test to update a user's info and check info is stored correctly
    def test_update_user(self):
        updated_user = update_user(1, 'thomas')
        assert updated_user.username == 'thomas'
