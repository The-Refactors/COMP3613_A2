from App.models.allocation import *
from App.database import db

def create_allocation(course_id, staff_id):
    allocate_check = Allocation.query.filter_by(course_id=course_id, staff_id=staff_id).first()
    if not allocate_check:
        newallocation = Allocation(course_id=course_id, staff_id=staff_id)
        db.session.add(newallocation)
        db.session.commit()
        return True
    return False

def get_all_allocates_json():
    allocates = Allocation.query.all()
    if not allocates:
        return []
    allocates = [allocate.get_json() for allocate in allocates]
    return allocates

def get_allocates_by_staff(id):
    return Allocation.query.filter_by(staff_id=id).all()

def get_allocate(id):
    return Allocation.query.get(id)

def delete_allocate(id):
    allocate = get_allocate(id)
    if allocate:
        db.session.delete(allocate)
        db.session.commit()
        return True
    return False