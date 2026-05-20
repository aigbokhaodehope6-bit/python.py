Balance = 2000000

print("1. Check Balance")
print("2. Withdraw Money")
print("3. Deposit Money")
print("4. Exit")

choice = input("Choose option: (1,2,3,4) ")
if choice == "1":
    print("Your balance is:", Balance)
elif choice == "2":
    amount = int(input("Enter amount to withdraw: "))
    if amount > Balance:
        print("Insufficient funds!")
    else:
        Balance -= amount
        print("Withdrawal successful! New balance:", Balance)
        print("Thank you for using our ATM!")
        print("Have a great day!")
        print("Your balance is:", Balance)
        print("Goodbye!")
elif choice == "3":
    amount = int(input("Enter amount to deposit: "))
    Balance += amount
    print("Deposit successful! New balance:", Balance)
    print("Have a great day!")
    print("Your balance is:", Balance)
    print("Goodbye!")
elif choice == "4":
    print("Thank you for banking with us!")