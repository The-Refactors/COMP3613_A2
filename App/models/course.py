from App.database import db
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courseCode = db.Column(db.String(100), nullable=False)
    courseName = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    staffs = db.relationship('Staff', secondary='allocations', backref='courses', lazy=True)

    __table_args__ = (
        CheckConstraint("semester IN (1, 2, 3)", name='check_semester'),
    )

    @validates('semester')
    def validate_semester(self, key, semester):
        if semester not in [1, 2, 3]:
            raise ValueError("Semester must be 1, 2 or 3")
        return semester

    def __init__(self, courseCode, courseName, semester, year):
        self.courseCode = courseCode
        self.courseName = courseName
        self.semester = semester
        self.year = year

    def get_json(self):
        return{
            'id': self.id,
            'coursecode': self.courseCode,
            'coursename': self.courseName,
            'semester': self.semester,
            'year': self.year
        }
