# Topic 8 Introduction to Object Oriented Programming

class Car:
    def __init__(self, brand, color, speed): #constructor method
        self.brand = brand
        self.color = color
        self.speed = speed

    def display_info(self): #method to display car information
        print(f"Brand: {self.brand}")
        print(f"Color: {self.color}")
        print(f"Speed: {self.speed} km/h")

    def drive(self): #method to simulate driving the car
        print(f"The {self.brand} is moving at {self.speed} km/h.")

# objects
car1 = Car("Toyota", "Red", 120) 
car2 = Car("Honda", "Blue", 150)
car3 = Car("Ford", "Black", 100)

# calling the methods
print("TOPIC 8")
print("\nCar 1 Information:")
car1.display_info()
car1.drive()
print()
print("Car 2 Information:")
car2.display_info()
car2.drive()
print()
print("Car 3 Information:")
car3.display_info()
car3.drive()
print()

# Topic 9 Object Behavior and Encapsulation
class EmployeeSalary:
    def __init__(self, name, salary):
        self.name = name
        self.__salary = salary

    def get_salary(self):
        return self.__salary

    def set_salary(self, new_salary):
        if new_salary > 0:
            self.__salary = new_salary
        else:
            print("Salary must be positive.")

    def current_salary(self):
        print(f"{self.name}'s salary is: ${self.__salary}")

print("\n\nTOPIC 9")
employee1 = EmployeeSalary("Alice", 50000)
employee1.current_salary() 

#Update salary using setter
employee1.set_salary(55000)
employee1.current_salary()

# invalid salary
employee1.set_salary(-1000)

employee1.__salary = 1000000 # This will not change the salary due to encapsulation
employee1.current_salary()

# Topic 10 Inheritance and Method Overriding

class SmartDevice:
    def __init__(self, device_name, energy):
        self.device_name = device_name
        self.status = 'ON'
        self.__energy = energy

    def turn_on(self):
        self.status = 'ON'
        print(f'{self.device_name} is now ON')

    def turn_off(self):
        self.status = 'OFF'
        print(f'{self.device_name} is now OFF')

    def get_energy(self):
        return self.__energy

    def set_energy(self, value):
        self.__energy = value

class SmartLight(SmartDevice):
    def __init__(self, device_name, energy):
        super().__init__(device_name, energy)
    
    def turn_on(self):
        self.status = 'ON'
        print(f'SmartLight {self.device_name} is now ON')

    def changed_color(self, color):
        self.status = 'ON'
        print(f'SmartLight {self.device_name} is glowing in {color}.')   
    
class SmartThermostat(SmartDevice):
    def __init__(self, device_name, energy):
        super().__init__(device_name, energy)

    def turn_on(self):
        self.status = 'ON'
        print(f'SmartThermostat {self.device_name} is now ON')

    def set_temperature(self, temp):
        print(f'SmartThermostat {self.device_name} is heating to {temp}°C.')

print("\n\nTOPIC 10")
light = SmartLight("Living Room Light", 10)
thermo = SmartThermostat("Bedroom Thermostat", 20)

light.turn_on()
light.changed_color("Blue")
print(light.get_energy())

thermo.turn_on()
thermo.set_temperature(24)

# Topic 11: Advanced Concepts in Python: Polymorphism
from abc import ABC, abstractmethod

class Food(ABC):
    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def serve(self):
        pass

    def serve(self):
        print(self)
        pass

class Pizza(Food):
    def prepare(self):
        print("Preparing pizza dough and adding toppings.")

    def serve(self):
        print("Serving the pizza hot and fresh.")

    def price(self):
        print("Prize: 120")

class Burger(Food):
    def prepare(self):
        print("Grilling the patty and assembling the burger.")

    def serve(self):
        print("Serving the burger with fries.")

    def price(self):
        print("Prize: 80")

class Pasta(Food):
    def prepare(self):
        print("Boiling pasta and preparing the sauce.")

    def serve(self):
        print("Serving the pasta with grated cheese.")

    def price(self):
        print("Prize: 60")

food = [Pizza(), Burger(), Pasta()]

print("\n\nTOPIC 11")
print("Preparing Food")
for f in food:
    f.prepare()

print("\nServing Food")
for item in food:
    item.serve()

print("\nPrice")
for item in food:
    item.price()

# Topic 12: Error Handling and Debugging Techniques in python


# Topic 13: Introduction to Unit Testing for Object Oriented Code
import unittest

class BankAccount:
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False
        
    def withdraw(self, amount):
        if amount > self.balance:
            return False
        if amount > 0:
            self.balance -= amount
            return True
        return False
    
class TestBankAccount(unittest.TestCase):
    def testdeposit(self):
        b = BankAccount()
        result = b.deposit(100)
        self.assertTrue(result)
        self.assertEqual(b.balance, 100)

    def testwithdraw(self):
        b = BankAccount()
        b.deposit(100) 
        result = b.withdraw(50)
        self.assertTrue(result)
        self.assertEqual(b.balance, 50)

    def test_withdraw_insufficient(self):
        b = BankAccount()
        b.deposit(50)
        result = b.withdraw(100)
        self.assertFalse(result)
        self.assertEqual(b.balance, 50)

    def test_multiple_deposits(self):
        b = BankAccount()
        b.deposit(100)
        b.deposit(200)
        self.assertEqual(b.balance, 300)

    def test_sequence_operations(self):
        b = BankAccount()
        b.deposit(200)
        b.withdraw(50)
        b.deposit(30)
        self.assertEqual(b.balance, 180)


if __name__ == "__main__":
    unittest.main()