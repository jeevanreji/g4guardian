# app/routes/energy_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session,jsonify
from app.models import db, EnergyLog, User,DeviceEnergy,ForecastedValue
from datetime import datetime, timedelta
from flask_mail import Message
from sqlalchemy.orm.exc import NoResultFound

energy_routes = Blueprint('energy_routes', __name__)

# app/routes/energy_routes.py
from flask import Blueprint, render_template, request, jsonify, session, flash
from app.models import db, EnergyLog, User
from app.utils.mail import send_alert_email
energy_routes = Blueprint('energy_routes', __name__)

@energy_routes.route('/users/<int:user_id>/dashboard', methods=['GET'])
def user_dashboard(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Fetch energy data from User model
    energy_consumed = user.energy_consumed  # This assumes this is being tracked in the User model
    energy_released = user.energy_released  # Similarly for energy_released

    # Fetch energy data from the EnergyLog for released energy
    logs = EnergyLog.query.filter_by(user_id=user.id).all()
    total_released = sum(log.energy_change for log in logs if log.type == 'released')

    # Fetch devices' energy consumption (assuming a many-to-one relationship with User)
    devices = DeviceEnergy.query.filter_by(user_id=user.id).all()  # Assuming Device is a model tracking devices
    device_consumptions = [{
        'device_name': device.name, 
        'energy_consumed': device.energy_consumed  # Assuming device has 'energy_consumed' field
    } for device in devices]
    print("device consumptions are: ",device_consumptions)
    return render_template(
        'user_home.html',
        user=user, 
        energy_consumed=energy_consumed, 
        energy_released=total_released,
        device_consumptions=device_consumptions  # Pass the device consumption data
    )


@energy_routes.route('/users/<int:user_id>/set_energy_demand', methods=['GET', 'POST'])
def set_energy_demand(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'POST':
        try:
            # Fetching the new energy demand from the form
            energy_demand = float(request.form.get('energy_demand'))
            device_type = request.form.get('device_type')
            if energy_demand < 0:
                raise ValueError("Energy demand must be non-negative.")

            # Update total energy demand and energy consumed by the user
            user.energy_demand += energy_demand
            user.energy_consumed += energy_demand

            # Check if the device already exists
            device = DeviceEnergy.query.filter_by(user_id=user_id, device_type=device_type).first()

            # If the device exists, increment energy values and request count
            if device:
                device.energy_demand += energy_demand
                device.energy_consumed += energy_demand
                device.number_of_requests += 1
                device.last_request_timestamp = datetime.utcnow()
            else:
                # If it's a new device for the user, create an entry in the DeviceEnergy table
                new_device = DeviceEnergy(
                    device_type=device_type,
                    energy_demand=energy_demand,
                    energy_consumed=energy_demand,
                    number_of_requests=1,
                    last_request_timestamp=datetime.utcnow(),
                    user_id=user_id
                )
                db.session.add(new_device)

            # Check against forecasted value
            forecasted_value = ForecastedValue.query.first()  # Assuming only one row
            if forecasted_value and user.energy_consumed > forecasted_value.value:
                send_alert_email(user.email_address, 
                                 f"Energy demand alert: Device '{device_type}' provisioning large energy demand", 
                                 f"Dear {user.username},\n\nYour device '{device_type}' is provisioning a lot of energy. Please consider removing it.")
                flash('Energy request exceeds forecasted value. Email alert sent!', 'danger')
                return redirect(url_for('energy_routes.set_energy_demand', user_id=user_id))

            # Frequency Check: If no. of requests > 10 and time between transactions < 15 mins
            time_difference = datetime.utcnow() - device.last_request_timestamp if device else timedelta(minutes=0)
            if device and device.number_of_requests > 4 and time_difference < timedelta(minutes=15):
                flash(f"Too many requests for device '{device_type}' in a short time. Transaction rejected!", 'danger')
                send_alert_email(user.email_address, 
                                 "Energy demand rejected: Too frequent requests",
                                 f"Dear {user.username},\n\nYou have sent too many requests for your device '{device_type}' in a short period. Please wait before sending another request.")
                return redirect(url_for('energy_routes.set_energy_demand', user_id=user_id))

            db.session.commit()
            
            flash("Energy demand updated successfully!", "success")
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


@energy_routes.route('/users/<int:user_id>/scale_down_energy_demand', methods=['GET', 'POST'])
def scale_down_energy_demand(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if request.method == 'POST':
        try:
            # Fetching device information from the form
            device_type = request.form.get('device_type')
            scale_factor = float(request.form.get('scale_factor'))  # scale_factor should be between 0 and 1

            if scale_factor < 0 or scale_factor > 1:
                raise ValueError("Scale factor must be between 0 and 1.")

            # Fetch the device for this user
            device = DeviceEnergy.query.filter_by(user_id=user_id, device_type=device_type).first()

            if not device:
                raise ValueError(f"Device '{device_type}' not found for this user.")

            # Calculate the new energy demand after scaling down
            new_energy_demand = device.energy_demand * scale_factor

            # Ensure the energy demand does not go below zero
            if new_energy_demand < 0:
                new_energy_demand = 0

            # Update the device's energy demand
            device.energy_demand = new_energy_demand

            # Optionally, if you want to scale down the energy consumed as well
            device.energy_consumed = new_energy_demand  # This assumes it's proportional

            db.session.commit()

            flash(f"Energy demand for '{device_type}' successfully scaled down to {new_energy_demand:.2f} kWh", "success")

        except (ValueError, TypeError) as e:
            flash(f"Error: {str(e)}", "error")

    return render_template('scaled_down_energy_demand.html', user=user)