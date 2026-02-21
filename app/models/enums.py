import enum


class UserRole(enum.Enum):
    MANAGER = "Manager"
    DISPATCHER = "Dispatcher"
    SAFETY_OFFICER = "SafetyOfficer"
    ANALYST = "Analyst"


class VehicleStatus(enum.Enum):
    AVAILABLE = "Available"
    ON_TRIP = "OnTrip"
    IN_SHOP = "InShop"
    RETIRED = "Retired"


class DriverStatus(enum.Enum):
    ON_DUTY = "OnDuty"
    ON_TRIP = "OnTrip"
    OFF_DUTY = "OffDuty"
    SUSPENDED = "Suspended"


class TripStatus(enum.Enum):
    DRAFT = "Draft"
    DISPATCHED = "Dispatched"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class MaintenanceStatus(enum.Enum):
    OPEN = "Open"
    COMPLETED = "Completed"