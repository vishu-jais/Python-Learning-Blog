a=int(input("a:"))
b=int(input("b:"))
print(f"sum of {a} and {b} is {a+b}")
print(f"subraction of {a} and {b} is {a-b}")
print(f"multiplication  of {a} and {b} is {a*b}")
try:
    print(f"division of {a} and {b} is {a/b}")
except Exception as e:
    print("division by 0 is impossible")
