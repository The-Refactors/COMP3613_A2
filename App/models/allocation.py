from App.database import db
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

class Allocation(db.Model):
    __tablename__='allocations'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    __table_args__ = (
        CheckConstraint("role IN ('lecturer', 'tutor', 'teaching assistant')", name='check_role'),
    )

    @validates('role')
    def validate_role(self, key, role):
        if role not in ['lecturer', 'tutor', 'teaching assistant']:
            raise ValueError("Role must be 'lecturer', 'tutor' or 'teaching assistant'")
        return role

    def __init__(self, course_id, staff_id, role):
        self.course_id = course_id
        self.staff_id = staff_id
        self.role = role

    def get_json(self):
        return{
            'id': self.id,
            'courseId': self.course_id,
            'staffId': self.staff_id,
            'role': self.role
        }
