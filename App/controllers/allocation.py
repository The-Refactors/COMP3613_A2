from App.models.allocation import *
from App.database import db
import csv

def create_allocation(course_id, staff_id, role):
    allocate_check = Allocation.query.filter_by(course_id=course_id, staff_id=staff_id, role=role).first()
    if not allocate_check:
        newallocation = Allocation(course_id=course_id, staff_id=staff_id, role=role)
        db.session.add(newallocation)
        db.session.commit()
        return newallocation
    return False

def get_all_allocates_json():
    allocates = Allocation.query.all()
    if not allocates:
        return []
    allocates = [allocate.get_json() for allocate in allocates]
    return allocates

# def get_allocates_by_course(course_id):
#     allocates = Allocation.query.filter_by(course_id=course_id).all()
#     return allocates

def get_allocates_by_course_json(course_id):
    allocates = Allocation.query.filter_by(course_id=course_id).all()
    entries = []
    if not allocates:
        return entries
    for allocate in allocates:
        entry = allocate.get_json()
        entries.append(entry)
    return entries

def get_allocates_by_staff(staff_id):
    allocates = Allocation.query.filter_by(staff_id=staff_id).all()
    if not allocates:
        return []
    return allocates

def get_allocates_by_staff_json(staff_id):
    allocates = Allocation.query.filter_by(staff_id=staff_id).all()
    entries = []
    if not allocates:
        return entries
    for allocate in allocates:
        entry = allocate.get_json()
        entries.append(entry)
    return entries

# def get_allocates_by_role(role):
#     allocates = Allocation.query.filter_by(role=role).all()
#     if not allocates:
#         return []
#     return allocates

def get_allocate(id):
    allocation = Allocation.query.get(id)
    if not allocation:
        return None
    return allocation

def delete_allocate(allocation_id):
    allocation = get_allocate(allocation_id)
    if allocation:
        db.session.delete(allocation)
        db.session.commit()  # Make sure changes are committed to the database
        return True
    return False


def parse_allocations():
    with open('allocations.csv', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)

        for row in csvreader:
            course_id = row[0]
            staff_id = row[1]
            role = row[2]

            allocation = Allocation(
                course_id=course_id,
                staff_id=staff_id,
                role=role
            )
            db.session.add(allocation)
        db.session.commit()
