#area calculator 

print("===Area calculator===")
print("1. rectangle")
print("2. circle")
print("3. triangle")

choice= int(input("Enter your choice:  "))
if choice == 1:
    length= float(input("enter length: "))
    width= float(input("enter width:  "))
    area= length * width 
    print("area of rectangle is=", area)
elif choice == 2:
    radius = float(input("enter radius:  "))
    area= 3.14 * radius* radius 
    print("area of circle is=", area) 
elif choice == 3:
    base= float(input("enter base: "))   
    height= float(input("enter height: "))
    area= 0.5 * base* height
    print("area of traingle is", area) 
else:
    print("invalid choice")        