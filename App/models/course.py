from App.database import db
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursecode = db.Column(db.String(100), nullable=False)
    coursename = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    staffs = db.relationship('Staff', secondary='allocations', backref='courses', lazy=True)

    __table_args__ = (
        CheckConstraint("semester IN (1, 2, 3)", name='check_semester'),
    )

    @validates('semester')
    def validate_semester(self, key, semester):
        try:
            semester = int(semester)
        except TypeError:
            raise TypeError("Semester must be an integer")
        if semester not in [1, 2, 3]:
            raise ValueError("Semester must be 1, 2 or 3")
        return semester

    def __init__(self, coursecode, coursename, semester, year):
        self.coursecode = coursecode
        self.coursename = coursename
        self.semester = semester
        self.year = year

    def get_json(self):
        return{
            'id': self.id,
            'coursecode': self.coursecode,
            'coursename': self.coursename,
            'semester': self.semester,
            'year': self.year
        }
