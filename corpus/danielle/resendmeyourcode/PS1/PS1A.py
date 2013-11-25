#Problem Set 1A
#Name:Danielle Chow
#Collaborators:Sammy Khalifa
#Time Spent: 1:00
#
NumberOfMonths=12
Balance=float(raw_input('Enter the outstanding balance on your credit card: '))
Interest=float(raw_input('Enter the annual credit card interest rate as a decimal: '))
PaymentRate=float(raw_input('Enter the minimum monthly payment rate as a decimal: '))
TotalAmountPaid=0

i=1
while i<=NumberOfMonths:
    MinimumMonthlyPayment=PaymentRate*Balance
    InterestPaid=(Interest/12)*Balance
    PrincipalPaid=MinimumMonthlyPayment-InterestPaid
    RemainingBalance=Balance-PrincipalPaid
    Balance=RemainingBalance
    TotalAmountPaid=MinimumMonthlyPayment+TotalAmountPaid
    
    print('Month:'+ str(i))
    print('Minumum Monthly Payment: '+ str(round(MinimumMonthlyPayment,2)))
    print('Remaining Balance: '+ str(round(RemainingBalance,2)))
    i=i+1
    
print('RESULT')
print('Total amount paid: '+ str(round(TotalAmountPaid,2)))
print('Remain balance: '+ str(round(Balance,2)))

