from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.extensions import db
from app.models.vehicle import Vehicle
from app.models.enums import VehicleStatus, VehicleType

vehicles_bp = Blueprint("vehicles", __name__, url_prefix="/vehicles")


@vehicles_bp.route("/")
@login_required
def list_vehicles():
    vehicles = Vehicle.query.all()
    return render_template("vehicles/list.html", vehicles=vehicles)


@vehicles_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_vehicle():
    if request.method == "POST":
        vehicle_type = request.form["vehicle_type"]
        model = request.form["model"]
        year = int(request.form["year"])
        license_plate = request.form["license_plate"]
        max_capacity = float(request.form["max_capacity"])
        acquisition_cost = float(request.form["acquisition_cost"])

        # Prevent duplicate license plate
        if Vehicle.query.filter_by(license_plate=license_plate).first():
            flash("License plate already exists.")
            return redirect(url_for("vehicles.create_vehicle"))

        vehicle = Vehicle(
            vehicle_type=VehicleType(vehicle_type),
            model=model,
            year=year,
            license_plate=license_plate,
            max_capacity=max_capacity,
            acquisition_cost=acquisition_cost,
            status=VehicleStatus.AVAILABLE
        )

        db.session.add(vehicle)
        db.session.commit()

        flash("Vehicle created successfully.")
        return redirect(url_for("vehicles.list_vehicles"))

    return render_template("vehicles/create.html")


@vehicles_bp.route("/edit/<int:vehicle_id>", methods=["GET", "POST"])
@login_required
def edit_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    if request.method == "POST":
        vehicle.vehicle_type = VehicleType(request.form["vehicle_type"])
        vehicle.model = request.form["model"]
        vehicle.year = int(request.form["year"])
        vehicle.max_capacity = float(request.form["max_capacity"])
        vehicle.acquisition_cost = float(request.form["acquisition_cost"])

        db.session.commit()
        flash("Vehicle updated successfully.")
        return redirect(url_for("vehicles.list_vehicles"))

    return render_template("vehicles/edit.html", vehicle=vehicle)


@vehicles_bp.route("/retire/<int:vehicle_id>")
@login_required
def retire_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    if vehicle.status == VehicleStatus.ON_TRIP:
        flash("Cannot retire vehicle while on trip.")
        return redirect(url_for("vehicles.list_vehicles"))

    vehicle.status = VehicleStatus.RETIRED
    db.session.commit()

    flash("Vehicle retired.")
    return redirect(url_for("vehicles.list_vehicles"))
