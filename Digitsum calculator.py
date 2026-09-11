# digit sum calculator 

number = int(input("Enter your number:  "))

total = 0 
while number > 0: 
    digit = number % 10
    total = total + digit 
    number = number // 10 

print(" the sum of the digit is:", total )    
 