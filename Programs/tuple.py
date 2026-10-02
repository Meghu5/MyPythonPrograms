
data = ("TC001", "PASS", 3.2, "API", "Smoke")

test_id, status, *metadata = data

print(test_id) # TC001
print(status) # PASS
print(metadata) # [3.2, "API", "Smoke"]

values = ("A", "B", "C")

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
first = values[0] # Access the first element -A
last = values[-1] # Access the last element -C

a, b, c = values # Unpack all elements

count = values.count("A") # Count occurrences of "A" -1
position = values.index("B") # Find the position of "B" - 1

#conversions

list_to_set = set([1, 2, 2, 3]) # Convert list to set - removes duplicates - {1, 2, 3}
set_to_list = list({1, 2, 3}) # Convert set to list - [1, 2, 3]

list_to_tuple = tuple([1, 2, 3]) # Convert list to tuple - (1, 2, 3)
tuple_to_list = list((1, 2, 3)) # Convert tuple to list - [1, 2, 3]