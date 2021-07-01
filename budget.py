BUFFER_SIZE = 30
DES_MAX_LENGTH = 23
AMO_MAX_LENGTH = 7

class Category:
    
    ledger = list()
    balance = int()

    def __init__(self, name):
        self.name = name
        self.ledger = []
        self.balance = 0

    def check_funds(self, amount):
        return amount <= self.balance

    def deposit(self, amount, description = ''):
        self.ledger.append({'amount' : amount, 'description' : description})
        self.balance += amount

    def withdraw(self, amount, description = ''):
        if self.check_funds(amount):
            self.ledger.append({'amount' : -amount, 'description' : description})
            self.balance -= amount
            return True
        return False
    
    def get_balance(self):
        return self.balance

    def transfer(self, amount, destination):
        check = self.withdraw(amount, 'Transfer to ' + destination.name)
        if check:
            destination.deposit(amount, 'Transfer from ' + self.name)
        return check
    
    def __str__(self):
        half = (BUFFER_SIZE - len(self.name)) // 2
        buffer = '*' * half + self.name + '*' * (BUFFER_SIZE - half - len(self.name)) + '\n'
        for item in self.ledger:
            std_description = item['description'][:DES_MAX_LENGTH]
            std_amount = "%.2f" % round(float(item['amount']), 2)
            std_amount = std_amount[:min(AMO_MAX_LENGTH, BUFFER_SIZE - DES_MAX_LENGTH)]
            buffer += std_description + ' ' * (BUFFER_SIZE - len(std_description) - len(std_amount)) + std_amount + '\n'
        buffer += 'Total: ' + "%.2f" % round(float(self.balance), 2)
        return buffer
    
def create_spend_chart(categories):
    total_withdraw = 0
    each_withdraw = {}
    chart = "Percentage spent by category\n"

    for category in categories:
        withdraw = 0
        for item in category.ledger:
            if item['amount'] < 0:
                total_withdraw += -item['amount']
                withdraw += -item['amount']
        each_withdraw[category] = withdraw

    percentage = {}
    for category in categories:
        percentage[category] = int(round(each_withdraw[category] / total_withdraw * 100, 0))

    for i in range(100, -10, -10):
        temp = str(i)
        while len(temp) < 3:
            temp = ' ' + temp
        chart += temp + '|'
        for category in categories:
            if percentage[category] >= i: 
                chart += ' o '
            else:
                chart += '   '
        chart += ' \n'
    chart += ' ' * 4
    for i in range(len(percentage)):
        chart += '---'
    chart += '-\n'
    check = True
    i = 0
    while check:
        chart += ' ' * 4
        check = False
        for category in categories:
            if i < len(category.name):
                check = True
                if i == 0:
                    chart += ' ' + category.name[i].capitalize() + ' '
                else:
                    chart += ' ' + category.name[i] + ' '
            else:
                chart += '   '
        if check: chart += ' \n'
        i += 1
    temp = chart[0:-14]

    return temp

