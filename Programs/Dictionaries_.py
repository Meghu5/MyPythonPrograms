#Merging two dictionaries in Python using the union operator (|) introduced in Python 3.9.
from operator import contains

from attr import In
from pytest import fail


common_headers = {
    "Accept": "application/json"
}

auth_headers = {
    "Authorization": "Bearer token"
}

merged_headers = common_headers | auth_headers
print(merged_headers)   #  {'Accept': 'application/json', 'Authorization': 'Bearer token'}

#update() method modifies the original dictionary in place, adding key-value pairs from another dictionary.

common_headers.update(auth_headers) # Modifies common_headers in place
print(common_headers)   #  {'Accept': 'application/json', 'Authorization': 'Bearer token'}

#If the same key exists in both dictionaries, the right-side value wins:
base_config = {"timeout": 30, "retries": 2}
env_config = {"timeout": 60} #latest 

final_config = base_config | env_config

print(final_config)
# {'timeout': 60, 'retries': 2}

#Syntax for creating a dictionary in Python:
# Create
data = {
    "key1": "value1",
    "key2": 100
}

# Read
value = data["key1"]
safe_value = data.get("missing_key", "default")

# Add or update
data["key3"] = True

# Delete
data.pop("key2", None)
del data["key1"]
data.clear()

# Check
if "key3" in data:
    print("Exists")

# Iterate
for key, value in data.items():
    print(key, value)

# Merge
merged = dict_a | dict_b
dict_a.update(dict_b)

# Nested access
value = data.get("outer", {}).get("inner")

# Airline response validation example

booking_response = {
    "status_code": 200,
    "booking": {
        "pnr": "DXB987",
        "status": "CONFIRMED",
        "passenger": {
            "first_name": "Meghana",
            "last_name": "M"
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

validation_errors = []

if booking_response.get("status_code") != 200:
    validation_errors.append("HTTP status code is not 200")

booking = booking_response.get("booking", {})

if not booking.get("pnr"):
    validation_errors.append("PNR is missing")

if booking.get("status") != "CONFIRMED":
    validation_errors.append("Booking is not confirmed")

passenger = booking.get("passenger", {})

required_passenger_fields = ["first_name", "last_name"]

for field in required_passenger_fields:
    if not passenger.get(field):
        validation_errors.append(f"Passenger field missing: {field}")

flight = booking.get("flight", {})

expected_flight_fields = {
    "origin": "AUH",
    "destination": "LHR",
    "flight_number": "EY101"
}

for field, expected_value in expected_flight_fields.items():
    actual_value = flight.get(field)

    if actual_value != expected_value:
        validation_errors.append(
            f"{field} mismatch: expected {expected_value}, got {actual_value}"
        )

payment = booking.get("payment", {})

if payment.get("status") != "CAPTURED":
    validation_errors.append("Payment is not captured")

if payment.get("currency") != "AED":
    validation_errors.append("Unexpected payment currency")

if not isinstance(payment.get("amount"), (int, float)):
    validation_errors.append("Payment amount must be numeric")

if validation_errors:
    print("Validation FAILED")
    for error in validation_errors:
        print("-", error)
else:
    print("Validation PASSED")  
    print("PNR:", booking["pnr"])
    print("Flight:", flight["flight_number"])
    print("Amount:", payment["amount"], payment["currency"])
    
    #Use .get() when the key may be missing:

age = data.get("age")

#In production test frameworks,# I choose direct access when the key is mandatory and 
# should fail immediately, and .get() when the field is optional or when I want controlled validation.

#Mask sensitive information in a dictionary using dictionary comprehension.This is essential in CI logs and reports to avoid exposing credentials or tokens.
payload = {
    "username": "user1",
    "password": "Secret123",
    "token": "abc123"
}

sensitive_fields = {"password", "token"}

safe_payload = {
    key: "***MASKED***" if key in sensitive_fields else value #if the key is in sensitive_fields, use "***MASKED***" otherwise, keep the original value
    for key, value in payload.items()
}

print(safe_payload) # {'username': 'user1', 'password': '***MASKED***', 'token': '***MASKED***'}
print(payload)      # {'username': 'user1', 'password': 'Secret123', 'token': 'abc123

#Important point payload still contains the real values safe_payload contains masked values
#So if you fetch from safe_payload, it stays masked.
#If you want the original value, you must fetch it from the original payload dictionary.
#In simple words #The code makes a safe copy for logging, reports, or API responses. It does not reverse the masking later.

#Analyze API response with dict
#input
test_report = {
    "suite": "Airline Booking API",
    "environment": "QA",
    "tests": [
        {"id": "TC001", "status": "PASS", "duration": 1.2},
        {"id": "TC002", "status": "FAIL", "duration": 2.8},
        {"id": "TC003", "status": "PASS", "duration": 0.9},
        {"id": "TC004", "status": "BLOCKED", "duration": 0.0},
        {"id": "TC005", "status": "FAIL", "duration": 3.4}
    ]
}
print(test_report["suite"])  # Airline Booking API
print(test_report["environment"])  # QA

passed_tests = [test for test in test_report["tests"] if test["status"] == "PASS"] # each iteration in tests stores in test now and all accessed using test["status"] and test["id"]
print("Passed Tests:", len(passed_tests)) # 3
failed_tests = [test for test in test_report["tests"] if test["status"] == "FAIL"]
print("Failed Tests:", len(failed_tests)) # 2
print("Failed Test IDs:", [test["id"] for test in failed_tests]) # ['TC002', 'TC005']
blocked_tests = [test for test in test_report["tests"] if test["status"] == "BLOCKED"]
print("Blocked Tests:", len(blocked_tests)) # 1
execution_times = [test["duration"] for test in test_report["tests"]]
print("Execution Times:", sum(execution_times)) # 8.3
pass_percentage = len(passed_tests) / len(test_report["tests"]) * 100   
print("Pass Percentage:", pass_percentage, "%") # 60.0

