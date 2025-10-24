# CustomFit - Tailoring Appointment System

A modern web application for managing custom tailoring appointments, built with Flask and MySQL.

## Features

- Browse design catalog
- Book appointments with expert tailors
- Input custom measurements
- Admin view for bookings
- Modern, responsive UI with Tailwind CSS

## Setup Instructions

### Prerequisites

- Python 3.11+
- MySQL 8.0+
- Virtual environment (recommended)

### Database Setup

1. Create MySQL database and user:

```sql
CREATE DATABASE customfit;
CREATE USER 'customfit_user'@'localhost' IDENTIFIED BY 'your_password_here';
GRANT ALL PRIVILEGES ON customfit.* TO 'customfit_user'@'localhost';
FLUSH PRIVILEGES;
```

2. Import schema and sample data:

```bash
mysql -u customfit_user -p customfit < migrations/schema.sql
mysql -u customfit_user -p customfit < sample_data/insert_sample_tailors.sql
```

### Application Setup

1. Clone the repository:

```bash
git clone [repository-url]
cd customfit
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create .env file:

```bash
cp .env.example .env
```

Update the values in .env with your database credentials.

5. Run the application:

```bash
python app.py
```

The application will be available at http://localhost:5000

## API Endpoints

- GET /api/designs - List all designs
- GET /api/tailors - List all tailors
- GET /api/bookings - List all bookings

## Testing the API

Sample curl commands:

```bash
# Get designs
curl http://localhost:5000/api/designs

# Get tailors
curl http://localhost:5000/api/tailors

# Get bookings
curl http://localhost:5000/api/bookings
```

## Project Structure

```
customfit/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── models.py           # SQLAlchemy models
├── static/
│   ├── css/           # Custom styles
│   ├── js/            # Client-side scripts
│   └── images/        # Design images
├── templates/          # Jinja2 templates
├── migrations/         # Database migrations
└── sample_data/       # Sample data files
```
