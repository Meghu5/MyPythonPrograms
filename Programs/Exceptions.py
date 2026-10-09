def load_config():
    try:
        with open("config.json", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as error:
        raise RuntimeError("Test configuration could not be loaded") from error # Raise a RuntimeError with a custom message, while preserving the original FileNotFoundError as the cause of the exception
    
class BookingValidationError(Exception):
    """Raised when the booking response violates the expected contract."""


class PaymentValidationError(Exception):
    """Raised when payment information is invalid."""


def validate_booking_response(response):
    if not isinstance(response, dict):
        raise BookingValidationError(
            "Booking response must be a dictionary"
        )

    status_code = response.get("status_code")

    if status_code != 200:
        raise BookingValidationError(
            f"Expected status_code=200, got {status_code}"
        )

    booking = response.get("booking")

    if not isinstance(booking, dict):
        raise BookingValidationError(
            "Missing or invalid 'booking' object"
        )

    required_fields = {
        "pnr",
        "status",
        "passenger",
        "flight",
        "payment"
    }

    missing_fields = required_fields - booking.keys()

    if missing_fields:
        raise BookingValidationError(
            f"Missing booking fields: {sorted(missing_fields)}"
        )

    if booking["status"] != "CONFIRMED":
        raise BookingValidationError(
            f"Unexpected booking status: {booking['status']}"
        )

    payment = booking["payment"]

    if payment.get("status") != "CAPTURED":
        raise PaymentValidationError(
            f"Payment status is not CAPTURED: {payment.get('status')}"
        )

    if payment.get("currency") != "AED":
        raise PaymentValidationError(
            f"Unexpected payment currency: {payment.get('currency')}"
        )

    amount = payment.get("amount")

    if not isinstance(amount, (int, float)):
        raise PaymentValidationError(
            f"Payment amount must be numeric, got {type(amount).__name__}"
        )

    return True


booking_response = {
    "status_code": 200,
    "booking": {
        "pnr": "EY7K9P",
        "status": "CONFIRMED",
        "passenger": {
            "first_name": "Meghana",
            "last_name": "K"
        },
        "flight": {
            "origin": "AUH",
            "destination": "LHR",
            "flight_number": "EY101"
        },
        "payment": {
            "status": "CAPTURED",
            "currency": "AED",
            "amount": 2450.75
        }
    }
}

try:
    validate_booking_response(booking_response)
except BookingValidationError as error:
    print("BOOKING VALIDATION FAILED:", error)
except PaymentValidationError as error:
    print("PAYMENT VALIDATION FAILED:", error)
except Exception as error:
    print("UNEXPECTED FRAMEWORK ERROR:", error)
    raise
else:
    print("Booking response validation PASSED")
finally:
    print("Validation workflow completed")
    
    #I define domain-specific exception classes for distinct failure categories, such as:

#ConfigurationError
#AuthenticationError
#ContractValidationError
#TransientServiceError
#BookingValidationError - They should be meaningful, lightweight, and used consistently by framework layers.
    
# good_client.py

import os


class ApiClient:
    def __init__(self, token: str | None = None): # The constructor of the ApiClient class takes an optional token parameter, which can be a string or None. If no token is provided, it attempts to retrieve the token from the environment variable "API_TOKEN". If neither is available
        self.token = token or os.getenv("API_TOKEN") # the token is stored in the instance variable self.token. If the token is not provided and the environment variable is not set, it raises a ValueError indicating that the API_TOKEN must be configured before creating an ApiClient instance.

        if not self.token:
            raise ValueError(
                "API_TOKEN must be configured before creating ApiClient"
            )
            
class Booking:
    def __init__(self, status): # double underscore methods like __init__ are used to define the constructor of the class. The constructor initializes the instance variable self._status with the provided status value.
        self._status = status

    @property # The @property decorator is used to define a getter method for the status property. It allows you to access the status of a Booking instance using booking_instance.status instead of calling a method like booking_instance.get_status(). This provides a more intuitive and Pythonic way to access the status attribute.
    def status(self): 
        return self._status # double underscore variables like self._status are used to indicate that the variable is intended to be private and should not be accessed directly from outside the class. Instead, the status property provides controlled access to the _status attribute.

    @status.setter # The @status.setter decorator is used to define a setter method for the status property. It allows you to set the status of a Booking instance using booking_instance.status = new_value instead of calling a method like booking_instance.set_status(new_value). This provides a more intuitive and Pythonic way to modify the status attribute.
    def status(self, value):
        allowed_statuses = {
            "PENDING",
            "CONFIRMED",
            "CANCELLED"
        }

        if value not in allowed_statuses:
            raise ValueError(f"Invalid status: {value}")

        self._status = value
        # overriding
class BaseReporter:
    def format_status(self, status): #override the format_status method to customize how the status is formatted. In this case, it converts the status string to uppercase using the upper() method before returning it. This ensures that the status is consistently formatted in uppercase when reported by the BaseReporter class.
        return status.upper() # upper() method is used to convert the status string to uppercase before returning it. This ensures that the status is consistently formatted in uppercase when reported by the BaseReporter class.


class HtmlReporter(BaseReporter):
    def format_status(self, status):#override the format_status method to customize how the status is formatted. In this case, it calls the format_status method of the parent class (BaseReporter) using super() to get the uppercase status, and then wraps that status in an HTML <span> tag before returning it. This allows the HtmlReporter class to extend the functionality of the BaseReporter class while still leveraging its existing behavior.
        return f"<span>{super().format_status(status)}</span>" #super() function is used to call the format_status method of the parent class (BaseReporter) to get the uppercase status, and then it wraps that status in an HTML <span> tag before returning it. This allows the HtmlReporter class to extend the functionality of the BaseReporter class while still leveraging its existing behavior.
    
  #composite pattern is a structural design pattern that allows you to compose objects into tree-like structures to represent part-whole hierarchies. It lets clients treat individual objects and compositions of objects uniformly. In the context of the provided code, the composite pattern is demonstrated through the use of the BaseReporter and HtmlReporter classes.  
class AuthProvider:
    def get_headers(self):
        return {
            "Authorization": "Bearer token"
        }


class BookingClient:
    def __init__(self, auth_provider):
        self.auth_provider = auth_provider

    def headers(self):
        return self.auth_provider.get_headers() # composition is used here to delegate the responsibility of providing headers to the AuthProvider instance. The BookingClient class does not need to know how the headers are generated; it simply relies on the AuthProvider to provide them. This promotes separation of concerns and allows for easier testing and maintenance.