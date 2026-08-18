#simple interest calculator

principle= float(input("Enter the principle amount:"))
rate= float(input("Enter the rate of interest: "))
time= float(input("Enter the time is years: "))

simple_interest= (principle* rate* time)/100

print("simple interest=", simple_interest)
