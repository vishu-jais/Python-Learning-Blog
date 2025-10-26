
numbers = list(map(int, input("Enter numbers separated by space: ").split()))

numbers.sort()
print("Second largest number is:", numbers[-2])
