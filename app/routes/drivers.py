from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.extensions import db
from app.models.enums import DriverStatus
from datetime import datetime
from app.utils.permissions import role_required
from app.models.enums import UserRole
from app.models.driver import Driver

drivers_bp = Blueprint("drivers", __name__, url_prefix="/drivers")


@drivers_bp.route("/")
@login_required
def list_drivers():
    drivers = Driver.query.all()
    return render_template("drivers/list.html", drivers=drivers)


@drivers_bp.route("/create", methods=["GET", "POST"])
@login_required
@role_required(UserRole.MANAGER)
def create_driver():
    if request.method == "POST":
        name = request.form["name"]
        license_number = request.form["license_number"]
        license_category = request.form["license_category"]
        license_expiry = datetime.strptime(
            request.form["license_expiry_date"], "%Y-%m-%d"
        ).date()

        if Driver.query.filter_by(license_number=license_number).first():
            flash("License number already exists.")
            return redirect(url_for("drivers.create_driver"))

        driver = Driver(
            name=name,
            license_number=license_number,
            license_category=license_category,
            license_expiry_date=license_expiry,
            status=DriverStatus.ON_DUTY
        )

        db.session.add(driver)
        db.session.commit()

        flash("Driver created successfully.")
        return redirect(url_for("drivers.list_drivers"))

    return render_template("drivers/create.html")