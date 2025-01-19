# app/routes/master_routes.py
from flask import Blueprint, jsonify
from app.models import db, EnergyLog, User

master_routes = Blueprint('master_routes', __name__)

# View total energy consumption and release by all users (Master Role Only)
@master_routes.route('/master/energy_summary', methods=['GET'])
def energy_summary():
    # Aggregate data from EnergyLog (total energy requested, released, and consumed)
    total_requested_energy = db.session.query(db.func.sum(EnergyLog.energy_change)).filter(EnergyLog.type == 'requested').scalar() or 0
    total_released_energy = db.session.query(db.func.sum(EnergyLog.energy_change)).filter(EnergyLog.type == 'released').scalar() or 0
    total_consumed_energy = db.session.query(db.func.sum(EnergyLog.energy_change)).filter(EnergyLog.type == 'consumed').scalar() or 0

    return jsonify({
        "total_requested_energy": total_requested_energy,
        "total_released_energy": total_released_energy,
        "total_consumed_energy": total_consumed_energy
    }), 200
