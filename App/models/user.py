from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    position = db.Column(db.String(50), nullable=False, default='admin')
    type = db.Column(db.String(50))

    __table_args__ = (
        CheckConstraint("position IN ('admin', 'staff')", name='check_position'),
    )

    @validates('position')
    def validate_position(self, key, position):
        if position not in ['admin', 'staff']:
            raise ValueError("Position must be 'admin' or 'staff'")
        return position

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'fname': self.fname,
            'lname': self.lname,
            'position': self.position
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

class Admin(User):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

class Staff(User):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }

    def __init__(self, username, password, position):
        super().__init__(username, password)
        self.position = position