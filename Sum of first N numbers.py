# sum of first N numbers 

n =int(input("Enter your number: "))
total = 0 

for number in range(1, n+1 ):
    total= number + total
print("the sum of numbers :", total )    