import os
from dotenv import load_dotenv

# Get base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Load .env file
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config:
    # Application directory
    BASE_DIR = BASE_DIR
    
    # Security
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-key-please-change-in-production')
    
    # Database configuration with PyMySQL driver
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'customfit_user')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'customfit')
    MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
    
    # SQLAlchemy configuration with PyMySQL
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # Security headers
    SEND_FILE_MAX_AGE_DEFAULT = 31536000
    SESSION_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True