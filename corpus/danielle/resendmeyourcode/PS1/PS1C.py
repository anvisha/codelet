#Problem Set 1C
#Name: Danielle Chow
#Collaborators:Sammy Khalifa
#Time Spent:0:40
#
InitialBalance=float(raw_input('Enter the outstanding balance on your credit card: '))
Interest=float(raw_input('Enter the annual credit card interest rate as a decimal: '))

Balance=InitialBalance
Error=0.01
Low=InitialBalance/12
High=(InitialBalance*(1+(Interest/12))**12)/12

while abs(Balance)>Error:
    Guess=(High+Low)/2
    m=1
    Balance=InitialBalance
    while m<=12:
        if Balance>0:
            AccruedInterest=Balance*(Interest/12)
            Balance=Balance+AccruedInterest
            Balance=Balance-Guess
            m=m+1
        else:
            break
    if Balance>0:
        Low=Guess
    elif Balance<0:
        High=Guess
    elif abs(Balance)<=Error:
        break  
print('RESULT')
print('Monthly payment to pay off debt in 1 year: ' + str(round(Guess,2)))
print('Number of months needed: '+ str(m-1))
print('Balance: '+ str(round(Balance,2)))


