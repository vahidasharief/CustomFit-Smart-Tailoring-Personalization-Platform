from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from decimal import Decimal

db = SQLAlchemy()
bcrypt = Bcrypt()

def _s(dt, fmt='%Y-%m-%d'):
    """Safely format datetime objects"""
    return dt.strftime(fmt) if dt else None

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': _s(self.created_at, '%Y-%m-%d %H:%M:%S')
        }

class Tailor(db.Model):
    __tablename__ = 'tailors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    experience_years = db.Column(db.Integer)
    specialty = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('Booking', backref='tailor', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'specialty': self.specialty,
            'experience_years': self.experience_years,
            'created_at': _s(self.created_at, '%Y-%m-%d %H:%M:%S')
        }

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    design_id = db.Column(db.Integer, nullable=False, index=True)
    tailor_id = db.Column(db.Integer, db.ForeignKey('tailors.id'), nullable=False)
    chest = db.Column(db.Numeric(5,2), nullable=True)
    waist = db.Column(db.Numeric(5,2), nullable=True)
    hips = db.Column(db.Numeric(5,2), nullable=True)
    length = db.Column(db.Numeric(5,2), nullable=True)
    appointment_date = db.Column(db.Date, nullable=False, index=True)
    appointment_time = db.Column(db.Time, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'design_id': self.design_id,
            'tailor': self.tailor.to_dict() if self.tailor else None,
            'measurements': {
                'chest': float(self.chest) if self.chest else None,
                'waist': float(self.waist) if self.waist else None,
                'hips': float(self.hips) if self.hips else None,
                'length': float(self.length) if self.length else None
            },
            'appointment_date': _s(self.appointment_date),
            'appointment_time': _s(self.appointment_time, '%H:%M'),
            'notes': self.notes or '',
            'created_at': _s(self.created_at, '%Y-%m-%d %H:%M:%S')
        }