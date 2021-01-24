class Cat:
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age
    def getName(self):
        return self.name
    def getAge(self):
        return self.age
    def getGender(self):
        return self.gender

class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @property
    def human_age(self):
        return self.age * 7.3

    @property
    def happiness(self):
        return self._happiness

    @happiness.setter
    def happiness(self, value):
        if 0 <= value <= 100:
            self._happiness = value
        else:
            raise ValueError("Happiness must be between 0 ... 100")




jane = Dog("Jane", 4)
jane.happiness = 88
print(jane.human_age)
print(jane.happiness)
