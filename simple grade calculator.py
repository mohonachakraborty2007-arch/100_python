#simple grade calculator 

marks= int(input("Enter your marks:  "))

if marks >= 90: 
    print("grade : A")
elif marks >= 80:     
    print("grade: B")
elif marks >= 70: 
    print("grade: C")
elif marks >= 60: 
    print("grade: D")
else:
    print("grade: F")            