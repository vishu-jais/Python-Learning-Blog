# Ask the user to enter numbers separated by spaces
numbers = list(map(int, input("Enter numbers separated by space: ").split()))
# Sort the list of numbers in ascending order
numbers.sort()
# Print the second largest number
print("Second largest number is:", numbers[-2])
