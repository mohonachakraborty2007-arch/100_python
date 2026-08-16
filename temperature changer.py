#temperature converter

temperature= float(input("enter your temperature: "))
choice= input("Convert to celcius or Fahrenheit?: ").lower()

if choice=="Fahrenheit":
    result=(temperature*9/5)+32
    print("temperature in Fahrenheit is=", result)

elif choice=="celcius":
    result=(temperature-32)*5/9 
    print("temperature in celcius is=", result)
else:
    print("invalid choice.")        