class TripAssignmentError(Exception):
    pass


class VehicleUnavailableError(TripAssignmentError):
    pass


class DriverUnavailableError(TripAssignmentError):
    pass


class CapacityExceededError(TripAssignmentError):
    pass


class LicenseExpiredError(TripAssignmentError):
    pass


class InvalidStateTransitionError(Exception):
    pass