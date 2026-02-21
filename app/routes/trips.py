from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.permissions import role_required
from app.models.enums import UserRole
from flask_login import login_required
from app.extensions import db
from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.enums import TripStatus, VehicleStatus, DriverStatus
from app.services.trip_service import TripService
from app.services.exceptions import TripAssignmentError


trips_bp = Blueprint("trips", __name__, url_prefix="/trips")

from flask import request
from sqlalchemy import or_

@trips_bp.route("/")
@login_required
def list_trips():

    search = request.args.get("search")
    status = request.args.get("status")
    sort = request.args.get("sort")

    query = Trip.query.join(Trip.vehicle).join(Trip.driver)

    if search:
        query = query.filter(
            or_(
                Vehicle.model.ilike(f"%{search}%"),
                Driver.name.ilike(f"%{search}%")
            )
        )

    if status:
        query = query.filter(Trip.status == TripStatus[status])

    if sort == "asc":
        query = query.order_by(Trip.id.asc())
    else:
        query = query.order_by(Trip.id.desc())

    trips = query.all()

    return render_template("trips/list.html", trips=trips)


@trips_bp.route("/create", methods=["GET", "POST"])
@login_required
@role_required(UserRole.MANAGER, UserRole.DISPATCHER)
def create_trip():
    vehicles = Vehicle.query.filter(
        Vehicle.status == VehicleStatus.AVAILABLE
    ).all()

    drivers = Driver.query.filter(
        Driver.status == DriverStatus.ON_DUTY
    ).all()

    if request.method == "POST":
        vehicle_id = int(request.form["vehicle_id"])
        driver_id = int(request.form["driver_id"])
        cargo_weight = float(request.form["cargo_weight"])
        origin = request.form["origin"]
        destination = request.form["destination"]
        revenue = float(request.form["revenue"])

        trip = Trip(
            vehicle_id=vehicle_id,
            driver_id=driver_id,
            cargo_weight=cargo_weight,
            origin=origin,
            destination=destination,
            revenue=revenue,
            status=TripStatus.DRAFT
        )

        db.session.add(trip)
        db.session.commit()

        flash("Trip created as Draft.")
        return redirect(url_for("trips.list_trips"))

    return render_template(
        "trips/create.html",
        vehicles=vehicles,
        drivers=drivers
    )


@trips_bp.route("/dispatch/<int:trip_id>")
@login_required
@role_required(UserRole.MANAGER, UserRole.DISPATCHER)
def dispatch_trip(trip_id):
    try:
        TripService.dispatch_trip(trip_id)
        flash("Trip dispatched successfully.")
    except TripAssignmentError as e:
        flash(str(e))
    return redirect(url_for("trips.list_trips"))


@trips_bp.route("/cancel/<int:trip_id>")
@login_required
@role_required(UserRole.MANAGER, UserRole.DISPATCHER)
def cancel_trip(trip_id):

    trip = Trip.query.get_or_404(trip_id)

    if trip.status == TripStatus.DRAFT:

        trip.status = TripStatus.CANCELLED

        # Reset driver & vehicle
        if trip.driver:
            trip.driver.status = DriverStatus.ON_DUTY

        if trip.vehicle:
            trip.vehicle.status = VehicleStatus.AVAILABLE

        db.session.commit()

        flash("Trip cancelled successfully.", "warning")

    return redirect(url_for("trips.list_trips"))


@trips_bp.route("/complete/<int:trip_id>", methods=["POST"])
@login_required
@role_required(UserRole.MANAGER, UserRole.DISPATCHER)
def complete_trip(trip_id):
    end_odometer = float(request.form["end_odometer"])
    try:
        TripService.complete_trip(trip_id, end_odometer)
        flash("Trip completed successfully.")
    except Exception as e:
        flash(str(e))
    return redirect(url_for("trips.list_trips"))


@trips_bp.route("/edit/<int:trip_id>", methods=["GET", "POST"])
@login_required
@role_required(UserRole.MANAGER, UserRole.DISPATCHER)
def edit_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)

    if trip.status != TripStatus.DRAFT:
        flash("Only draft trips can be edited.")
        return redirect(url_for("trips.list_trips"))

    vehicles = Vehicle.query.filter(
        Vehicle.status == VehicleStatus.AVAILABLE
    ).all()

    drivers = Driver.query.filter(
        Driver.status == DriverStatus.ON_DUTY
    ).all()

    if request.method == "POST":
        trip.vehicle_id = int(request.form["vehicle_id"])
        trip.driver_id = int(request.form["driver_id"])
        trip.cargo_weight = float(request.form["cargo_weight"])
        trip.origin = request.form["origin"]
        trip.destination = request.form["destination"]
        trip.revenue = float(request.form["revenue"])

        db.session.commit()

        flash("Trip updated.")
        return redirect(url_for("trips.list_trips"))

    return render_template(
        "trips/edit.html",
        trip=trip,
        vehicles=vehicles,
        drivers=drivers
    )
