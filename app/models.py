from app import db
from datetime import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(80), nullable=False)
    energy_demand = db.Column(db.Float, default=0.0)  # kWh demand per hour
    energy_consumed = db.Column(db.Float, default=0.0)  # Total kWh consumed
    energy_released = db.Column(db.Float, default=0.0)  # Total kWh uploaded to the grid
    role = db.Column(db.String(20),default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(255), nullable=False)  # New password field
    def __repr__(self):
        return f"<User {self.username}>"
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class EnergyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    energy_change = db.Column(db.Float, nullable=False)  # Positive for consumption, negative for release
    type = db.Column(db.String(80), nullable=False)  # 'consumed' or 'released'

    user = db.relationship('User', backref='energy_logs')

    def __repr__(self):
        return f"<EnergyLog {self.id} ({self.type}): {self.energy_change} kWh>"
