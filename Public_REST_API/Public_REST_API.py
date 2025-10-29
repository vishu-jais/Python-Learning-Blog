import requests
url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    for user in data[:3]:  # Displaying only the first three users
        print("Name:", user["name"])
        print("Email:", user["email"])
        print()
else:
    print("Error:", response.status_code)
