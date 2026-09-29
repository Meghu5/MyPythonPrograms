test_ids = ["TC001", "TC002", "TC003", "TC002", "TC004", "TC001"]

seen = set()
duplicates = []

for test_id in test_ids:
    if test_id in seen:
        duplicates.append(test_id)
    else:
        seen.add(test_id)

duplicates.sort() # Ascending order
duplicates.sort(reverse=True) # Descending order
print("Duplicates:", duplicates)
print("Unique IDs:", sorted(seen))