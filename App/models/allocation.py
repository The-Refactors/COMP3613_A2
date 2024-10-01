from App.database import db

class Allocation(db.Model):
    __tablename__='allocations'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)

    def __init__(self, course_id, staff_id):
        self.course_id = course_id
        self.staff_id = staff_id

    def get_json(self):
        return{
            'id': self.id,
            'courseId': self.course_id,
            'staffId': self.staff_id
        }
