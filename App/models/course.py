from App.database import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courseName = db.Column(db.String(100), nullable=False)
    courseCode = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    staffs = db.relationship('Staff', secondary='allocations', backref='courses', lazy=True)

    def __init__(self, courseCode, courseName, semester, year):
        self.courseCode = courseCode
        self.courseName = courseName
        self.semester = semester
        self.year = year
