import csv


with open('students.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
   
    writer.writerow(['Name', 'Age', 'Course'])
    
    writer.writerow(['Madhu', 21, 'Python'])
    writer.writerow(['John', 22, 'Java'])
    writer.writerow(['Anita', 20, 'DSA'])

print("Data written successfully to students.csv")


with open('students.csv', mode='r') as file:
    reader = csv.reader(file)
    print("\nReading data from students.csv:")
    for row in reader:
        print(row)
