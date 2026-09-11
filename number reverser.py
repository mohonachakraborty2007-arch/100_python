#number reverser 

number= int(input("Enter your number :  "))

reverse = 0 
while number > 0: 
    digit= number % 10 
    reverse= reverse * 10 + digit 
    number = number // 10 

print("reversed number :", reverse)      