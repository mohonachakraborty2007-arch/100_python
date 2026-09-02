#Factorial calculator 

number = int(input("enter your number : "))
factorial= 1 

for i in range (1, number+1 ):
    factorial = factorial * i 
    print("factorial is : ", factorial ) 