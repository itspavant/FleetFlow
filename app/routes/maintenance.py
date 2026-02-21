from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.maintenance import MaintenanceLog
from app.models.vehicle import Vehicle
from app.models.enums import VehicleStatus, MaintenanceStatus
from app.services.maintenance_service import MaintenanceService
from app.services.exceptions import InvalidStateTransitionError
from app.extensions import db

maintenance_bp = Blueprint("maintenance", __name__, url_prefix="/maintenance")


@maintenance_bp.route("/")
@login_required
def list_maintenance():
    logs = MaintenanceLog.query.all()
    return render_template("maintenance/list.html", logs=logs)


@maintenance_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_maintenance():
    vehicles = Vehicle.query.filter(
        Vehicle.status == VehicleStatus.AVAILABLE
    ).all()

    if request.method == "POST":
        vehicle_id = int(request.form["vehicle_id"])
        description = request.form["description"]
        cost = float(request.form["cost"])
        remarks = request.form.get("remarks")

        try:
            MaintenanceService.create_maintenance(
                vehicle_id, description, cost, remarks
            )
            flash("Maintenance created. Vehicle moved to IN_SHOP.")
        except InvalidStateTransitionError as e:
            flash(str(e))

        return redirect(url_for("maintenance.list_maintenance"))

    return render_template(
        "maintenance/create.html",
        vehicles=vehicles
    )


@maintenance_bp.route("/complete/<int:maintenance_id>")
@login_required
def complete_maintenance(maintenance_id):
    try:
        MaintenanceService.complete_maintenance(maintenance_id)
        flash("Maintenance completed. Vehicle available again.")
    except Exception as e:
        flash(str(e))

    return redirect(url_for("maintenance.list_maintenance"))


@maintenance_bp.route("/edit/<int:maintenance_id>", methods=["GET", "POST"])
@login_required
def edit_maintenance(maintenance_id):
    log = MaintenanceLog.query.get_or_404(maintenance_id)

    if log.status != MaintenanceStatus.OPEN:
        flash("Only open maintenance can be edited.")
        return redirect(url_for("maintenance.list_maintenance"))

    if request.method == "POST":
        log.description = request.form["description"]
        log.cost = float(request.form["cost"])
        log.remarks = request.form.get("remarks")

        db.session.commit()
        flash("Maintenance updated.")
        return redirect(url_for("maintenance.list_maintenance"))

    return render_template("maintenance/edit.html", log=log)
