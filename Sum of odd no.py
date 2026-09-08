#sum of odd numbers 

start = int(input("Enter your starting number: "))
end = int(input("Enter your ending number: "))

total = 0 

for number in range ( start, end+1 ): 
    number % 2 != 0 
    total += number 

    print("The sum of the odd numbers:", total )
