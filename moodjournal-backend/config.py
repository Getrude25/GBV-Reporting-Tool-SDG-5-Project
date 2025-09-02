import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-12345'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-67890'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Using SQLite for simplicity
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'moodjournal.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API keys (you can set these as environment variables later)
    CLICKPESA_API_KEY = os.environ.get('CLICKPESA_API_KEY') or 'test-key'
    CLICKPESA_SECRET_KEY = os.environ.get('CLICKPESA_SECRET_KEY') or 'test-secret'
    HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY') or 'test-hf-key'
