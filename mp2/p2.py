class Student:
    def _init_(self, name, marks):
        self._name = name           
        self._marks = marks
    @property
    def marks(self):
        return self._marks
    @marks.setter
    def marks(self, value):
        if 0 <= value <= 100:
            self._marks = value
        else:
            raise ValueError("Marks must be between 0 and 100")
    def _str_(self):
        return f"Student Name: {self._name}, Marks: {self._marks}"
s1 = Student("Arun", 85)
print(s1)    
s1.marks = 95        
print(s1.marks)         
# s1.marks = 120