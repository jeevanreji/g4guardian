# app/routes/energy_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session,jsonify
from app.models import db, EnergyLog, User


energy_routes = Blueprint('energy_routes', __name__)

# app/routes/energy_routes.py
from flask import Blueprint, render_template, request, jsonify, session, flash
from app.models import db, EnergyLog, User

energy_routes = Blueprint('energy_routes', __name__)

@energy_routes.route('/users/<int:user_id>/dashboard', methods=['GET'])
def user_dashboard(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Fetch energy data
    energy_consumed = user.energy_consumed  # This assumes this is being tracked in the User model
    energy_released = user.energy_released  # Similarly for energy_released
    
    # You can optionally aggregate logs from EnergyLog
    logs = EnergyLog.query.filter_by(user_id=user.id).all()
    total_released = sum(log.energy_change for log in logs if log.type == 'released')

    return render_template('user_home.html', user=user, energy_consumed=energy_consumed, energy_released=total_released)


@energy_routes.route('/users/<int:user_id>/set_energy_demand', methods=['GET', 'POST'])
def set_energy_demand(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'POST':
        try:
            # Fetching the new energy demand from the form
            energy_demand = float(request.form.get('energy_demand'))
            if energy_demand < 0:
                raise ValueError("Energy demand must be non-negative.")

            # Update the energy_demand by adding the new value to the previous value
            user.energy_demand += energy_demand

            # Update the energy_consumed (this will add the new value to the cumulative energy consumed)
            user.energy_consumed += energy_demand

            db.session.commit()
            
            flash("Energy demand updated successfully! It will keep updating every minute.", "success")
        except (ValueError, TypeError) as e:
            flash(f"Error: {str(e)}", "error")

    return render_template('set_energy_demand.html', user=user)


# Upload energy to the grid
@energy_routes.route('/users/<int:user_id>/upload_energy', methods=['GET', 'POST'])
def upload_energy(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'POST':
        try:
            # Fetching the uploaded energy from the form
            energy = float(request.form.get('energy'))
            if energy < 0:
                raise ValueError("Uploaded energy must be non-negative.")

            # Update the energy_released by adding the new value to the previous value
            user.energy_released += energy

            # Log the energy change (energy released is a negative change)
            log = EnergyLog(user_id=user.id, energy_change=-energy, type='released')
            db.session.add(log)

            # Commit to the database
            db.session.commit()

            flash(f"{energy} kWh uploaded to the grid successfully!", "success")
        except (ValueError, TypeError) as e:
            flash(f"Error: {str(e)}", "error")

    return render_template('upload_energy.html', user=user)
