class Car:
    # Constructor – used to initialize the properties of the object
    def __init__(self, brand, model, year):
        self.brand = brand   # Property 1  
        self.model = model   # Property 2
        self.year = year     # Property 3
   
    # Method to display the car's details
    def display_details(self):
        print(f"Car Brand: {self.brand}")
        print(f"Model: {self.model}")
        print(f"Year: {self.year}")

    # Method to start the car
    def start_engine(self):
        print(f"The {self.brand} {self.model}'s engine has started!")

     # Method to stop the car
    def stop_engine(self):
        print(f"The {self.brand} {self.model}'s engine has stopped.")

# Create objects of the Car class
car1 = Car("Toyota", "Innova", 2020)
car2 = Car("Hyundai", "Creta", 2023)

# Call methods for each car
car1.display_details()
car1.start_engine()
car1.stop_engine()

print()   #just to add a blank line

car2.display_details()
car2.start_engine()
car2.stop_engine()
