import os

class Config:
    # General App Config
    

    # Database Config
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'mysql+pymysql://admin:Realmadrid123@database_host:3306/database-1?ssl_ca=/path/to/ca-certificate.crt')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    # Celery Config
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    TEMPLATE_FOLDER = os.getenv('TEMPLATE_FOLDER', './Users/jeevanreji/Documents/segMaster/templates/')  # Default to './templates' in the current directory