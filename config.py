import os

class Config:
    """Base configuration"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quiz_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key-change-this-in-production'
    SESSION_TYPE = 'filesystem'
