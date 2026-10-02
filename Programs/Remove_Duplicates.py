from enum import unique


test_ids = ["TC001", "TC002", "TC003", "TC002", "TC004", "TC001"]

seen = set()
duplicates = []

for test_id in test_ids:
    if test_id in seen:
        duplicates.append(test_id)
    else:
        seen.add(test_id)
# Ascending order
duplicates.sort() # Ascending order
# Descending order
duplicates.sort(reverse=True) # Descending order
print("Duplicates:", duplicates)
print("Unique IDs:", sorted(seen)) # Ascending order
print("Unique IDs (Descending):", sorted(seen, reverse=True)) # Descending order

#rem dups
values = [1, 2, 2, 3, 1]
unique_values = list(set(values)) # dont preserve order as it is set
print("Unique values:", unique_values) #[1, 2, 3]

#To preserve order, you can use a loop or a dictionary:
values = [1, 2, 2, 3, 1]
unique_values = list(dict.fromkeys(values)) # dict.fromkeys(values) creates a dictionary using the list 
#items as keys.Dictionary keys are unique.The order of keys is preserved.

print(unique_values)
# [1, 2, 3]




#**********************************************************************************************

# Adding items to different lists based on conditions

test_results = [
    {"id": "TC001", "status": "PASS", "duration": 2.4},
    {"id": "TC002", "status": "FAIL", "duration": 3.1},
    {"id": "TC003", "status": "PASS", "duration": 1.8},
    {"id": "TC004", "status": "BLOCKED", "duration": 0.0},
    {"id": "TC005", "status": "FAIL", "duration": 4.2},
]

passed_tests = []
failed_tests = []
blocked_tests = []
durations = []

for result in test_results:
    status = result["status"]
    durations.append(result["duration"])

    if status == "PASS":
        passed_tests.append(result["id"])
    elif status == "FAIL":
        failed_tests.append(result["id"])
    elif status == "BLOCKED":
        blocked_tests.append(result["id"])

total_tests = len(test_results)
pass_count = len(passed_tests)
fail_count = len(failed_tests)
blocked_count = len(blocked_tests)

execution_time = sum(durations)

pass_percentage = (pass_count / total_tests) * 100 if total_tests else 0
fail_percentage = (fail_count / total_tests) * 100 if total_tests else 0

print("Passed:", passed_tests)
print("Failed:", failed_tests)
print("Blocked:", blocked_tests)
print("Total tests:", total_tests)
print("Pass count:", pass_count)
print("Fail count:", fail_count)
print("Blocked count:", blocked_count)
print("Pass percentage:", round(pass_percentage, 2))
print("Fail percentage:", round(fail_percentage, 2))
print("Total execution time:", round(execution_time, 2), "seconds")