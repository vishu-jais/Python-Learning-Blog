# Define a class called Student
class Student:
    # Constructor (initialize properties)
    def __init__(self, name, roll_no, marks):
        self.name = name
        self.roll_no = roll_no
        self.marks = marks

    # Method to display student details
    def display_details(self):
        print(f"Name: {self.name}")
        print(f"Roll No: {self.roll_no}")
        print(f"Marks: {self.marks}")

    # Method to calculate grade
    def calculate_grade(self):
        if self.marks >= 90:
            grade = "A+"
        elif self.marks >= 80:
            grade = "A"
        elif self.marks >= 70:
            grade = "B"
        elif self.marks >= 60:
            grade = "C"
        else:
            grade = "Fail"
        return grade

    # Method to show full result
    def show_result(self):
        grade = self.calculate_grade()
        print(f"Student {self.name} has secured Grade: {grade}\n")

# Create Student objects
student1 = Student("Ranjith", 101, 92)
student2 = Student("Raja", 102, 76)
student3 = Student("Rajesh", 103, 58)

# Use methods
student1.display_details()
student1.show_result()

student2.display_details()
student2.show_result()

student3.display_details()
student3.show_result()
