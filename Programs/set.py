items = {1, 2, 3}
seta = {1, 2, 3,4,"Meghu"}
setb = {3, 4, 5, 6}

items.add(4) # adds a single element {1, 2, 3, 4}
items.update({5, 6}) # adds multiple elements {1, 2, 3, 4, 5, 6}

items.remove(2) #throws KeyError if 2 is not present
items.discard(10) # no error if 10 is not present

result1 = seta | setb #union
result2 = seta & setb #intersection
result3 = seta - setb #difference
result4 = seta ^ setb #symmetric difference - unique elements in both sets

is_subset = seta.issubset(setb)
is_superset = seta.issuperset(setb)

print(result1)  # {1, 2, 3, 4, 5, 6}
print(result2)  # {3, 4}
print(result3)  # {1, 2}
print(result4)  # {1, 2, 5, 6}
print(is_subset)  # False
print(is_superset)  # False

#Detect Duplicate Order IDs Across Paginated Results

#This is a realistic QA/SDET use case. You collect order IDs from charset_normalizer import detect

#from multiple pages and must detect duplicates.

pages = [
    {
        "page": 1,
        "orders": ["ORD1001", "ORD1002", "ORD1003"]
    },
    {
        "page": 2,
        "orders": ["ORD1004", "ORD1005", "ORD1003"]
    },
    {
        "page": 3,
        "orders": ["ORD1006", "ORD1007", "ORD1002"]
    }
]

seen_order_ids = set()
duplicate_order_ids = set()
all_order_records = []

for page in pages:
    page_number = page["page"] #get the page number
    order_ids = page.get("orders", []) #get the order IDs for the current page, defaulting to an empty list if "orders" key is missing

    for order_id in order_ids:
        all_order_records.append((page_number, order_id)) #adding a tuple of (page_number, order_id) to the all_order_records list for later analysis

        if order_id in seen_order_ids:
            duplicate_order_ids.add(order_id) #add the order ID to the duplicate_order_ids set if it has already been seen -2nd time or more
        else:
            seen_order_ids.add(order_id) #add the order ID to the seen_order_ids set if it is new-1st time

print("All unique order IDs:", seen_order_ids) # Print all unique order IDs- (ORD1001, ORD1002, ORD1003, ORD1004, ORD1005, ORD1006, ORD1007)
print("Duplicate order IDs:", duplicate_order_ids) # Print duplicate order IDs-(ORD1002, ORD1003)
print("Total unique orders:", len(seen_order_ids)) # Print the total number of unique orders- 7

#The set gives fast membership testing.
#The duplicate set stores each duplicate only once.
#The tuple records where the value appeared.
#The algorithm works efficiently for large result sets.
#It avoids repeated list.count() calls, which can be expensive.

# Response validation

required_fields = {
    "pnr",
    "status",
    "passenger",
    "flight",
    "payment"
}  #mandatory fields in the API response

actual_fields = {
    "pnr",
    "status",
    "passenger",
    "flight",
    "payment",
    "created_at",
    "trace_id"
}  # fields in the actual API response

missing_fields = required_fields - actual_fields # fields that are required but missing
unexpected_fields = actual_fields - required_fields # fields that are present but not required
common_fields = required_fields & actual_fields # fields that are both required and present

print("Missing fields:", missing_fields) # set() - no missing fields
print("Unexpected fields:", unexpected_fields) # {"created_at", "trace_id"}
print("Validated required fields:", common_fields) # {"pnr", "status", "passenger", "flight", "payment"}
#This is much clearer than writing many individual if statements.

#pytest parameterization can be used to validate multiple API responses in a single test function.

import pytest

browser_matrix = (
    ("Chrome", "Windows", "headed"),
    ("Firefox", "Linux", "headless"),
    ("Edge", "Windows", "headed")
) # This is a tuple of tuples, where each inner tuple represents a combination of browser, operating system, and mode for testing.


@pytest.mark.parametrize(
    "browser, operating_system, mode", # Parameters for the test function
    browser_matrix  # This decorator will run the test_cross_browser function multiple times, once for each tuple in the browser_matrix
)
def test_cross_browser(browser, operating_system, mode): 
    print(browser, operating_system, mode)
    assert browser in {"Chrome", "Firefox", "Edge"} # Validate that the browser is one of the supported browsers