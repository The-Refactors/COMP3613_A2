from App.models.allocation import *
from App.database import db
import csv

def create_allocation(courseid, staffid, role):
    allocate_check = Allocation.query.filter_by(courseid=courseid, staffid=staffid, role=role).first()
    if not allocate_check:
        newallocation = Allocation(courseid=courseid, staffid=staffid, role=role)
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

# def get_allocates_by_course(courseid):
#     allocates = Allocation.query.filter_by(courseid=courseid).all()
#     return allocates

def get_allocates_by_course_json(courseid):
    allocates = Allocation.query.filter_by(courseid=courseid).all()
    entries = []
    if not allocates:
        return entries
    for allocate in allocates:
        entry = allocate.get_json()
        entries.append(entry)
    return entries

def get_allocates_by_staff(staffid):
    allocates = Allocation.query.filter_by(staffid=staffid).all()
    if not allocates:
        return []
    return allocates

def get_allocates_by_staff_json(staffid):
    allocates = Allocation.query.filter_by(staffid=staffid).all()
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
            courseid = row[0]
            staffid = row[1]
            role = row[2]

            allocation = Allocation(
                courseid=courseid,
                staffid=staffid,
                role=role
            )
            db.session.add(allocation)
        db.session.commit()
