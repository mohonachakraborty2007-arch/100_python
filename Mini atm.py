#mini atm 

balence = 10000

withdraw= int(input(" Enter your withdrwal ammount: "))

if withdraw <= 10000:
   balence = balence - withdraw
   print("Your withdrwal ammount :", withdraw )
   print(" Your balence is :", balence)

else: 
   print( "GARIBB!! insuffiecient balence")
