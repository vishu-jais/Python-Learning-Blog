import math
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

gcd = math.gcd(a, b)
lcm = abs(a * b) // gcd
print("GCD of", a, "and", b, "is:", gcd)
print("LCM of", a, "and", b, "is:", lcm)
