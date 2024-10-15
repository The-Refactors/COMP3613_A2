import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.models import Course, Allocation
from App.controllers import (
    # Course Testing
    create_course,
    get_course_by_name,
    get_course_by_code,
    get_course,
    get_all_courses_json,
    update_course,
    # Allocation Testing
    create_allocation,
    get_all_allocates_json,
    get_allocates_by_staff,
    delete_allocate,
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''

class CourseUnitTests(unittest.TestCase):

    def test_new_course(self):
        course = Course("CS101", "Intro to CS", 1, 2024)
        assert course.courseCode == "CS101"
        assert course.courseName == "Intro to CS"
        assert course.semester == 1
        assert course.year == 2024
    
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
    
    def test_update_course(self):
        course = Course("CS101", "Intro to CS", 1, 2024)
        course.courseName = "Advanced CS"
        course.semester = 2
        course.year = 2025
        self.assertEqual(course.courseName, "Advanced CS")
        self.assertEqual(course.semester, 2)
        self.assertEqual(course.year, 2025)


class AllocationUnitTests(unittest.TestCase):

    def test_new_allocation(self):
        allocation = Allocation(1, 2, 'lecturer')
        assert allocation.course_id == 1
        assert allocation.staff_id == 2
        assert allocation.role == "lecturer"

    def test_get_json(self):
        allocation = Allocation(1, 2, 'lecturer')
        allocation_json = allocation.get_json()
        self.assertDictEqual(allocation_json, {
            "id": None,
            "courseId": 1,
            "staffId": 2,
            "role": "lecturer"
        })

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and reused for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class CourseIntegrationTests(unittest.TestCase):

    def test_create_course(self):
        course = create_course("CS102", "Data Structures", 1, 2024)
        assert course.courseCode == "CS102"
        assert course.courseName == "Data Structures"

    def test_get_course_by_code(self):
        course = create_course("CS103", "Algorithms", 2, 2025)
        fetched_course = get_course_by_code("CS103")
        assert fetched_course.courseName == "Algorithms"

    def test_get_all_courses_json(self):
        courses_json = get_all_courses_json()
        self.assertIsInstance(courses_json, list)
        assert len(courses_json) >= 1

    def test_update_course(self):
        course = create_course("CS104", "Operating Systems", 1, 2024)
        update_course(course.id, "CS104","Advanced OS", 1, 2024)
        updated_course = get_course(course.id)
        assert updated_course.courseName == "Advanced OS"


class AllocationIntegrationTests(unittest.TestCase):

    def test_create_allocation(self):
        course = create_course("CS105", "Database Systems", 1, 2024)
        result = create_allocation(course.id, 2, 'lecturer').get_json()
        self.assertDictEqual(result, {
            "id": 1,
            "courseId": 4,
            "staffId": 2,
            "role": "lecturer"
        })

    def test_get_allocates_by_staff(self):
        course = create_course("CS106", "Networking", 1, 2024)
        create_allocation(course.id, 3, 'lecturer')
        allocations = get_allocates_by_staff(3)
        assert len(allocations) > 0

    def test_delete_allocate(self):
        # Fetch allocations before creation
        allocations_before_create = get_allocates_by_staff(2)
        print(f"Allocations before creation: {allocations_before_create}")  # Debug line

        # Create allocation
        course = create_course("CS107", "Software Engineering", 1, 2024)
        create_allocation(course.id, 2, 'lecturer')

        # Fetch allocations for the staff to get the new allocation ID
        allocations = get_allocates_by_staff(2)
        self.assertGreater(len(allocations), len(allocations_before_create), "No allocations were created")

        allocation_id = allocations[-1].id  # Get the ID of the allocation

        # Delete the allocation using the fetched ID
        result = delete_allocate(allocation_id)
        self.assertTrue(result, "Allocation deletion failed")

        # Fetch allocations again after deletion
        allocations_after_delete = get_allocates_by_staff(2)
        print(f"Allocations after deletion: {allocations_after_delete}")  # Debug line

        # Check if a new allocation exists
        self.assertEqual(allocations_before_create, allocations_after_delete, "Allocation still exists after deletion")