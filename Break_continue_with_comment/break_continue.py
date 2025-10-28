# Example 1: Using 'break' in a loop
print("Example 1: Using 'break'")
for i in range(1, 11):  # Loop from 1 to 10
    if i == 6:
        print("Number 6 found! Stopping the loop.")
        break  # Exit the loop when i = 6
    print("Current number:", i)

print("\n---\n")

# Example 2: Using 'continue' in a loop
print("Example 2: Using 'continue'")
for i in range(1, 11):
    if i % 2 == 0:
        continue  # Skip even numbers
    print("Odd number:", i)

print("\n---\n")

# Example 3: Combining break and continue
print("Example 3: Combining 'break' and 'continue'")
for i in range(1, 11):
    if i == 5:
        print("Skipping 5")
        continue  # Skip 5
    if i == 8:
        print("Stopping at 8")
        break  # Stop the loop at 8
    print("Number:", i)
