#countdown timer 
import time 

number = int(input("Enter your Number : "))

while number >= 0: 
    time.sleep(1)
    print(number)
    number= number - 1 