class Owner:

    def __init__(self, name, monthly_income, spending_habit):
        self.name = name
        self.monthly_income = monthly_income
        self.spending_habit = spending_habit

    def get_monthly_income(self):
       print(self.monthly_income)

    def get_monthly_spending(self):
         print(self.spending_habit)

    def update_monthly_income(self, rate):
        self.monthly_income = monthly_income * rate

    def halve_spending(self):
        self.spending_habit = self.spending_habit/2

    def __str__(self):
        return "name:" + self.name + "\monthly income:" + self.monthly_income + \
               "spending habit:" + self.spending_habit



class Wallet:

    def __init__(self, initial_amount, owner):
       self.initial_amount = initial_amount
       self.owner = owner

    def deposit(self, amount):
       self.initial_amount += amount

    def withdraw(self, amount):
        self.initial_amount -= amount

    def check(self):
        print(self.withdraw)

    def get_owner(self):
        self.owner = owner


import random, urllib.request, time, copy

class WalletGame:

    def __init__(self, num_players, income_mean, income_sigma, spend_mean, spend_sigma, epoch):
        self.num = num_players
        self.mean = income_mean
        self.mean2 = spend_mean
        self.sigma = income_sigma
        self.sigma2 = spend_sigma
        self.epoch = epoch

    def play(self):
        print("num of players is:")
        print(self.num)
        print(self.mean)
        print(self.mean2)
        print(self.sigma)
        print(self.sigma2)
        print(self.epoch)




if __name__ == '__main__':
    wg = WalletGame(20, 5000, 500, 0.7, 0.5, 120)
    wg.play()
