#Problem Set 1B
#Name:Danielle Chow
#Collaborators: Sammy Khalifa
#Time Spent:1:45
#
InitialBalance=float(raw_input('Enter the outstanding balance on your credit card: '))
Interest=float(raw_input('Enter the annual credit card interest rate as a decimal: '))

i=1
Balance=1
while Balance>0:
    Guess=i*10
    m=1
    Balance=InitialBalance
    while m<= 12:
        if Balance>0:
            AccruedInterest=Balance*(Interest/12)
            Balance=Balance+AccruedInterest
            Balance=Balance-Guess
            m=m+1
        else:
            break
    i=i+1
print('RESULT')
print('Monthly payment to pay off debt in 1 year: ' + str(Guess))
print('Number of months needed: '+ str(m-1))
print('Balance: '+ str(round(Balance,2)))
