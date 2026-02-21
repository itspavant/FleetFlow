from app.extensions import db
from datetime import date

class TripExpense(db.Model):
    __tablename__ = "trip_expenses"

    id = db.Column(db.Integer, primary_key=True)

    trip_id = db.Column(
        db.Integer,
        db.ForeignKey("trips.id"),
        nullable=False
    )

    description = db.Column(db.String(255))
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=date.today)

    trip = db.relationship("Trip", backref="misc_expenses")