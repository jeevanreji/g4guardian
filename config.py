import os

class Config:
    # General App Config
    

    # Database Config
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'mysql+pymysql://admin:Realmadrid123@database_host:3306/database-1?ssl_ca=/path/to/ca-certificate.crt')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    # Celery Config
    #CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    #CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    #TEMPLATE_FOLDER = os.getenv('TEMPLATE_FOLDER', './Users/jeevanreji/Documents/segMaster/templates/')  # Default to './templates' in the current directory
    MAIL_SERVER = 'email-smtp.us-east-1.amazonaws.com'  # Replace with your SMTP server
    MAIL_PORT = 587  # SMTP port (for TLS)
    MAIL_USE_TLS = True  # If your server supports TLS
    MAIL_USERNAME = 'AKIASVLKCHPUWPG45EFB'  # Set your mail username here
    MAIL_PASSWORD = 'BDT4dca92kgy4Pp9JuoziiJU+kGkDlz4GZUSFJCSrbDY'  # Set your mail password here
    MAIL_DEFAULT_SENDER = 'jreji6@gatech.edu'  # Default sender's email address

    TEMPLATE_FOLDER = '/Users/jeevanreji/Documents/segMaster/templates/'
    STATIC_FOLDER = '/Users/jeevanreji/Documents/segMaster/static'
    # app = Flask(__name__, template_folder='/Users/jeevanreji/Documents/segMaster/templates/',static_folder='/Users/jeevanreji/Documents/segMaster/static')

    