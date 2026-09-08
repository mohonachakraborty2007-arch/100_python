#sum of odd numbers 

start = int(input("Enter the starting number: "))
end = int(input("Enter the ending number: "))

total = 0

for number in range(start, end + 1):
    if number % 2 != 0:
        total += number

print("Sum of odd numbers:", total)
