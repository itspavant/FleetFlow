from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.permissions import role_required
from app.models.enums import UserRole
from flask_login import login_required
from app.extensions import db
from app.models.fuel import FuelLog
from app.models.trip import Trip
from datetime import datetime


fuel_bp = Blueprint("fuel", __name__, url_prefix="/fuel")


@fuel_bp.route("/add/<int:trip_id>", methods=["GET", "POST"])
@login_required
@role_required(UserRole.MANAGER, UserRole.DISPATCHER)
def add_fuel(trip_id):
    trip = Trip.query.get_or_404(trip_id)

    if request.method == "POST":
        liters = float(request.form["liters"])
        cost = float(request.form["cost"])
        date = datetime.strptime(
            request.form["date"], "%Y-%m-%d"
        ).date()

        fuel = FuelLog(
            trip_id=trip_id,
            liters=liters,
            cost=cost,
            date=date
        )

        db.session.add(fuel)
        db.session.commit()

        flash("Fuel log added.")
        return redirect(url_for("trips.list_trips"))

    return render_template("fuel/add.html", trip=trip)


@fuel_bp.route("/view/<int:trip_id>")
@login_required
def view_fuel(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    logs = trip.fuel_logs
    return render_template("fuel/list.html", trip=trip, logs=logs)


@fuel_bp.route("/edit/<int:fuel_id>", methods=["GET", "POST"])
@login_required
@role_required(UserRole.MANAGER, UserRole.DISPATCHER)
def edit_fuel(fuel_id):
    fuel = FuelLog.query.get_or_404(fuel_id)

    if request.method == "POST":
        fuel.liters = float(request.form["liters"])
        fuel.cost = float(request.form["cost"])
        fuel.date = request.form["date"]

        db.session.commit()
        flash("Fuel updated.")
        return redirect(url_for("fuel.view_fuel", trip_id=fuel.trip_id))

    return render_template("fuel/edit.html", fuel=fuel)


@fuel_bp.route("/delete/<int:fuel_id>")
@login_required
@role_required(UserRole.MANAGER)
def delete_fuel(fuel_id):
    fuel = FuelLog.query.get_or_404(fuel_id)
    trip_id = fuel.trip_id

    db.session.delete(fuel)
    db.session.commit()

    flash("Fuel deleted.")
    return redirect(url_for("fuel.view_fuel", trip_id=trip_id))
