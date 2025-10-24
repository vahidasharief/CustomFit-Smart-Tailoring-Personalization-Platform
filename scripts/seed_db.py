import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from flask import Flask
from models import db, Tailor, User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

SAMPLE_TAILORS = [
    {
        'name': 'Rajesh Kumar',
        'email': 'rajesh.kumar@customfit.com',
        'phone': '+91-555-0123',
        'experience_years': 15,
        'specialty': 'Traditional Sherwanis & Wedding Wear'
    },
    {
        'name': 'Priya Sharma',
        'email': 'priya.sharma@customfit.com',
        'phone': '+91-555-0124',
        'experience_years': 12,
        'specialty': 'Designer Sarees & Lehengas'
    },
    {
        'name': 'Abdul Karim',
        'email': 'abdul.karim@customfit.com',
        'phone': '+91-555-0125',
        'experience_years': 18,
        'specialty': 'Modern Indo-Western Fusion'
    },
    {
        'name': 'Meera Patel',
        'email': 'meera.patel@customfit.com',
        'phone': '+91-555-0126',
        'experience_years': 20,
        'specialty': 'Bridal Couture & Embroidery'
    },
    {
        'name': 'Suresh Mehta',
        'email': 'suresh.mehta@customfit.com',
        'phone': '+91-555-0127',
        'experience_years': 16,
        'specialty': 'Contemporary Ethnic Wear'
    }
]

def seed_demo_user():
    with app.app_context():
        # Check if users table is empty
        if User.query.first() is None:
            print("Creating demo user...")
            user = User(
                name='Demo User',
                email='demo@customfit.test'
            )
            user.set_password('demo123')
            db.session.add(user)
            db.session.commit()
            print("Successfully created demo user!")
        else:
            print("Users table already contains data. Skipping...")

def seed_tailors():
    with app.app_context():
        # Clear existing tailors
        print("Clearing existing tailors...")
        Tailor.query.delete()
        db.session.commit()
        
        print("Seeding tailors table with new data...")
        for tailor_data in SAMPLE_TAILORS:
            tailor = Tailor(**tailor_data)
            db.session.add(tailor)
        db.session.commit()
        print("Successfully seeded tailors table with new data!")

if __name__ == '__main__':
    try:
        seed_demo_user()
        seed_tailors()
        print("Database seeding completed successfully!")
        exit(0)
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
        exit(1)