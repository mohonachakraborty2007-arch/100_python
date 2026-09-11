#digit counter 

number = int(input("Enter your number :  "))

count = 0 
while number > 0 : 
    number = number // 10 
    count += 1 

print("The number of digits: ", count )    