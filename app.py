from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from datetime import datetime, date, time
from models import db, bcrypt, Tailor, Booking, User
from config import Config
import json
import os
import csv
import io
from email_validator import validate_email, EmailNotValidError

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'error'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()
    
    # Create a test user if no users exist
    if not User.query.first():
        test_user = User(
            name='Test User',
            email='test@example.com'
        )
        test_user.set_password('password123')
        db.session.add(test_user)
        db.session.commit()
        app.logger.info('Test user created')

csrf = CSRFProtect()
csrf.init_app(app)

# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            # Validate email
            email = validate_email(request.form['email']).email
            
            # Check if user exists
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
                return redirect(url_for('register'))
            
            # Validate password
            password = request.form['password']
            if len(password) < 6:
                flash('Password must be at least 6 characters', 'error')
                return redirect(url_for('register'))
            
            if password != request.form['confirm_password']:
                flash('Passwords do not match', 'error')
                return redirect(url_for('register'))
            
            # Create user
            user = User(
                name=request.form['name'],
                email=email
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
            
        except EmailNotValidError:
            flash('Invalid email address', 'error')
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Registration error: {str(e)}")
            flash('Error creating account', 'error')
    
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.info(f"Login route accessed with method: {request.method}")
    
    if current_user.is_authenticated:
        app.logger.info("User already authenticated, redirecting to index")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        app.logger.info("Processing login POST request")
        app.logger.info(f"Form data: {request.form}")
        
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            
            app.logger.info(f"Login attempt for email: {email}")
            
            if not email or not password:
                app.logger.warning("Missing email or password")
                flash('Please provide both email and password', 'error')
                return render_template('auth/login.html')
            
            user = User.query.filter_by(email=email).first()
            
            if user and user.check_password(password):
                login_user(user, remember=bool(request.form.get('remember')))
                flash('Successfully logged in!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page if next_page else url_for('index'))
            
            flash('Invalid email or password', 'error')
            
        except Exception as e:
            app.logger.error(f"Login error: {str(e)}")
            flash('Error during login. Please try again.', 'error')
    
    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

# Load designs from JSON file
def load_designs():
    designs_path = os.path.join(Config.BASE_DIR, 'sample_data', 'designs.json')
    with open(designs_path) as f:
        data = json.load(f)
        return data.get('designs', [])

def get_design_by_id(design_id):
    designs = load_designs()
    return next((d for d in designs if d['id'] == design_id), None)

def validate_booking_data(data):
    errors = []
    
    # Required fields
    required_fields = ['name', 'email', 'phone', 'design_id', 'tailor_id', 
                      'chest', 'waist', 'hips', 'length', 
                      'appointment_date', 'appointment_time']
    
    for field in required_fields:
        if not data.get(field):
            errors.append(f"{field} is required")
    
    # Email validation
    try:
        if data.get('email'):
            validate_email(data['email'])
    except EmailNotValidError:
        errors.append("Invalid email address")
    
    # Numeric validations
    try:
        measurements = ['chest', 'waist', 'hips', 'length']
        for m in measurements:
            if data.get(m):
                value = float(data[m])
                if value <= 0 or value > 100:
                    errors.append(f"Invalid {m} measurement")
    except ValueError:
        errors.append("Invalid measurement values")
    
    # Date and time validation
    try:
        if data.get('appointment_date'):
            date_obj = datetime.strptime(data['appointment_date'], '%Y-%m-%d').date()
            if date_obj < date.today():
                errors.append("Appointment date must be in the future")
    except ValueError:
        errors.append("Invalid date format")
    
    try:
        if data.get('appointment_time'):
            time_obj = datetime.strptime(data['appointment_time'], '%H:%M').time()
            if time_obj.hour < 9 or time_obj.hour >= 18:
                errors.append("Appointment time must be between 9 AM and 6 PM")
    except ValueError:
        errors.append("Invalid time format")
    
    return errors

@app.route('/')
def index():
    designs = load_designs()
    tailors = Tailor.query.all()
    return render_template('index.html', designs=designs[:3], tailors=tailors[:3])

@app.route('/designs')
def designs():
    designs = load_designs()
    return render_template('design.html', designs=designs)

@app.route('/design/<int:design_id>')
def design_detail(design_id):
    design = get_design_by_id(design_id)
    if not design:
        flash('Design not found', 'error')
        return redirect(url_for('designs'))
    return render_template('design.html', design=design)

@app.route('/tailors')
def tailors():
    tailors_list = Tailor.query.all()
    return render_template('tailor.html', tailors=tailors_list)

@app.route('/book', methods=['GET'])
@app.route('/book/<int:tailor_id>', methods=['GET'])
def book(tailor_id=None):
    designs = load_designs()
    if tailor_id:
        tailor = Tailor.query.get_or_404(tailor_id)
        tailors = [tailor]
    else:
        tailors = Tailor.query.all()
        tailor_id = request.args.get('tailor_id')
        if tailor_id:
            try:
                tailor_id = int(tailor_id)
                tailor = next((t for t in tailors if t.id == tailor_id), None)
                if tailor:
                    tailors = [tailor]
            except ValueError:
                pass
    
    return render_template('booking.html', designs=designs, tailors=tailors)

@app.route('/api/book', methods=['POST'])
def api_book():
    try:
        # Get JSON data or form data
        data = request.get_json() if request.is_json else request.form.to_dict()
        
        # Validate input
        errors = validate_booking_data(data)
        if errors:
            return jsonify({'errors': errors}), 400
        
        # Convert date and time strings to Python objects
        date_obj = datetime.strptime(data['appointment_date'], '%Y-%m-%d').date()
        time_obj = datetime.strptime(data['appointment_time'], '%H:%M').time()
        
        booking = Booking(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            design_id=int(data['design_id']),
            tailor_id=int(data['tailor_id']),
            chest=float(data['chest']),
            waist=float(data['waist']),
            hips=float(data['hips']),
            length=float(data['length']),
            appointment_date=date_obj,
            appointment_time=time_obj,
            notes=data.get('notes', '')
        )
        
        db.session.add(booking)
        db.session.commit()
        
        if request.is_json:
            return jsonify(booking.to_dict()), 201
        else:
            flash('Booking successful!', 'success')
            return redirect(url_for('index'))
            
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Booking error: {str(e)}")
        if request.is_json:
            return jsonify({'error': 'Internal server error'}), 500
        flash('Error creating booking. Please try again.', 'error')
        return redirect(url_for('book'))

@app.route('/admin/bookings')
@login_required
def admin_bookings():
    bookings = Booking.query.order_by(Booking.appointment_date, Booking.appointment_time).all()
    return render_template('admin_bookings.html', bookings=bookings)

@app.route('/admin/bookings.csv')
def admin_bookings_csv():
    bookings = Booking.query.order_by(Booking.appointment_date, Booking.appointment_time).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Design ID', 'Tailor', 
                    'Chest', 'Waist', 'Hips', 'Length',
                    'Appointment Date', 'Appointment Time', 'Notes', 'Created At'])
    
    # Write data
    for booking in bookings:
        writer.writerow([
            booking.id, booking.name, booking.email, booking.phone,
            booking.design_id, booking.tailor.name,
            booking.chest, booking.waist, booking.hips, booking.length,
            booking.appointment_date.strftime('%Y-%m-%d'),
            booking.appointment_time.strftime('%H:%M'),
            booking.notes,
            booking.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'bookings_{datetime.now().strftime("%Y%m%d")}.csv'
    )

# API Endpoints
@app.route('/api/designs')
def api_designs():
    return jsonify(load_designs())

@app.route('/api/tailors')
def api_tailors():
    tailors = Tailor.query.all()
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'email': t.email,
        'phone': t.phone,
        'specialty': t.specialty,
        'experience_years': t.experience_years
    } for t in tailors])

@app.route('/api/bookings')
def api_bookings():
    bookings = Booking.query.all()
    return jsonify([booking.to_dict() for booking in bookings])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)