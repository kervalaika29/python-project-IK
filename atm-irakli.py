import os


class Account:
    """საბაზისო საბანკო ანგარიშის კლასი — ინახავს სახელსა და დაცულ ბალანსს"""

    def __init__(self, name, balance):
        self.name = name
        self.__balance = balance  # __ (ორმაგი ხაზგასმა) — დაცული მონაცემი, გარედან პირდაპირ არ ჩანს

    def get_balance(self):
        """აბრუნებს მიმდინარე ბალანსს"""
        return self.__balance

    def deposit(self, amount):
        """ამატებს თანხას ბალანსს"""
        self.__balance = self.__balance + amount

    def withdraw(self, amount):
        """აკლებს თანხას ბალანსს, თუ საკმარისია. აბრუნებს True თუ მოხერხდა, False თუ არა"""
        if amount > self.__balance:
            return False
        self.__balance = self.__balance - amount
        return True

    def get_type(self):
        """საბაზისო ტიპი — ქვეკლასები ამას გადაფარავენ (override)"""
        return "ჩვეულებრივი ანგარიში"


class SavingsAccount(Account):
    """შემნახველი ანგარიში — Account-ის მემკვიდრეა, პლუს აქვს საპროცენტო განაკვეთი"""

    def __init__(self, name, balance, interest_rate):
        super().__init__(name, balance)
        self.interest_rate = interest_rate

    def get_type(self):
        return "შემნახველი ანგარიში"

    def add_interest(self):
        """ახალი მეთოდი — მხოლოდ SavingsAccount-ს აქვს"""
        interest = self.get_balance() * self.interest_rate
        self.deposit(interest)
        return interest


class CheckingAccount(Account):
    """მიმდინარე ანგარიში — Account-ის მემკვიდრეა, პლუს აქვს overdraft ლიმიტი"""

    def __init__(self, name, balance, overdraft_limit):
        super().__init__(name, balance)
        self.overdraft_limit = overdraft_limit

    def get_type(self):
        return "მიმდინარე ანგარიში"

    def withdraw(self, amount):
        """გადაფარული withdraw — საშვებელია მინუსში წასვლა overdraft_limit-ის ფარგლებში"""
        if amount > self.get_balance() + self.overdraft_limit:
            return False
        self.deposit(-amount)
        return True


def get_valid_amount(prompt):
    """მომხმარებელს სთხოვს რიცხვს მანამ, სანამ არ მიიღებს ვალიდურ, დადებით რიცხვს"""
    while True:
        text = input(prompt)
        try:
            amount = float(text)
            if amount <= 0:
                print("თანხა უნდა იყოს დადებითი რიცხვი")
            else:
                return amount
        except:
            print("გთხოვთ, შეიყვანოთ სწორი რიცხვი")


def save_accounts(accounts):
    """ინახავს ანგარიშების სიას accounts.txt ფაილში: ტიპი,სახელი,ბალანსი,დამატებითი-პარამეტრი"""
    with open("accounts.txt", "w", encoding="utf-8") as f:
        for acc in accounts:
            if isinstance(acc, SavingsAccount):
                f.write("savings," + acc.name + "," + str(acc.get_balance()) + "," + str(acc.interest_rate) + "\n")
            elif isinstance(acc, CheckingAccount):
                f.write("checking," + acc.name + "," + str(acc.get_balance()) + "," + str(acc.overdraft_limit) + "\n")


def load_accounts():
    """კითხულობს ანგარიშების სიას accounts.txt ფაილიდან და აღადგენს სწორ ტიპებად (Savings/Checking)"""
    accounts = []
    with open("accounts.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            acc_type = parts[0]
            name = parts[1]
            balance = float(parts[2])
            extra = float(parts[3])
            if acc_type == "savings":
                accounts.append(SavingsAccount(name, balance, extra))
            elif acc_type == "checking":
                accounts.append(CheckingAccount(name, balance, extra))
    return accounts


def reset_accounts():
    """შლის accounts.txt ფაილს და ქმნის ახალ, ნაგულისხმევ მონაცემებს"""
    try:
        os.remove("accounts.txt")
    except:
        pass  # ფაილი ისედაც არ არსებობდა — პრობლემა არ არის

    new_accounts = [
        SavingsAccount("ნინო", 1000.0, 0.05),
        CheckingAccount("გიორგი", 500.0, 300.0),
    ]
    save_accounts(new_accounts)
    return new_accounts


# ვცდილობთ ანგარიშების წაკითხვას ფაილიდან; თუ ფაილი ჯერ არ არსებობს (პირველი გაშვება),
# ვიყენებთ ნაგულისხმევ მონაცემებს და ვქმნით ფაილს
try:
    accounts = load_accounts()
except:
    accounts = [
        SavingsAccount("ნინო", 1000.0, 0.05),
        CheckingAccount("გიორგი", 500.0, 300.0),
    ]
    save_accounts(accounts)

# ანგარიშების ჩვენება და არჩევა (ჰგავს ბარათის ჩასმას ბანკომატში)
print("=== ანგარიშის არჩევა ===")
number = 1
for acc in accounts:
    print(number, "-", acc.name, "(" + acc.get_type() + ")")
    number = number + 1

while True:
    account_choice = input("აირჩიე ანგარიში ნომრით: ")
    try:
        account_choice = int(account_choice)
        if account_choice < 1 or account_choice > len(accounts):
            print("გთხოვთ, აირჩიოთ 1-დან", len(accounts), "-მდე")
        else:
            break
    except:
        print("გთხოვთ, შეიყვანოთ სწორი რიცხვი")

account = accounts[account_choice - 1]

print("მოგესალმებით,", account.name, "-", account.get_type())

# ბანკომატის მთავარი მარყუჟი — მენიუ მეორდება, სანამ მომხმარებელი არ აირჩევს გასვლას
while True:
    print("=== ბანკომატი ===")
    print("1. ბალანსის ნახვა")
    print("2. თანხის შეტანა")
    print("3. თანხის გატანა")
    print("4. გასვლა")
    print("5. ანგარიშების საწყის მდგომარეობაზე დაბრუნება")

    choice = input("აირჩიე მოქმედება (1-5): ")

    if choice == "1":
        print("თქვენი ბალანსია:", account.get_balance())
    elif choice == "2":
        amount = get_valid_amount("რამდენის შეტანა გსურთ? ")
        account.deposit(amount)
        save_accounts(accounts)
        print("ჩაირიცხა:", amount)
        print("ახალი ბალანსია:", account.get_balance())
    elif choice == "3":
        amount = get_valid_amount("რამდენის გატანა გსურთ? ")
        success = account.withdraw(amount)
        if success:
            save_accounts(accounts)
            print("გატანილია:", amount)
            print("ახალი ბალანსია:", account.get_balance())
        else:
            print("არასაკმარისი თანხაა ანგარიშზე!")
    elif choice == "4":
        print("ნახვამდის!")
        break
    elif choice == "5":
        confirm = input("დარწმუნებული ხართ? ეს წაშლის ყველა შენახულ მონაცემს! (კი/არა): ")
        if confirm == "კი":
            accounts = reset_accounts()
            account = accounts[account_choice - 1]
            print("ანგარიშები დაბრუნდა საწყის მდგომარეობაზე!")
        else:
            print("გაუქმებულია")
    else:
        print("არასწორი არჩევანი — გთხოვთ, აირჩიოთ 1-დან 5-მდე")