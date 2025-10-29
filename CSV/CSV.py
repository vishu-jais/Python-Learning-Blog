import csv

# Writing to a CSV file
with open('students.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(['Name', 'Age', 'Course'])
     # Write data rows
    writer.writerow(['Madhu', 21, 'Python'])
    writer.writerow(['John', 22, 'Java'])
    writer.writerow(['Anita', 20, 'DSA'])

print("Data written successfully to students.csv")

# Reading from a CSV file
with open('students.csv', mode='r') as file:
    reader = csv.reader(file)
    print("\nReading data from students.csv:")
    for row in reader:
        print(row)
