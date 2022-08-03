# from decimal import Decimal
from pydoc import describe
from pyexpat import model
from tabnanny import verbose
from django.db import models
from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import post_save
from Accounting.exceptions import AccountingEquationError


# Create your models here.

class AccountTypeChoices(models.TextChoices):
    ASSETS = 'ASSETS', 'ASSETS'
    LIABILITLES = 'LIABILITLES', 'LIABILITLES'
    INCOME = 'INCOME', 'INCOME'
    EXPENSES = 'EXPENSES', 'EXPENSES'

class TransactionTypeChoices(models.TextChoices):
    invoice = 'invoice', 'Invoice',
    income = 'income', 'Income',
    expense = 'expense', 'Expense',
    bill = 'bill', 'Bill'

class CurrencyChoices(models.TextChoices):
    USD = 'USD', 'USD'
    IQD = 'IQD', 'IQD'


class AccountManager(models.Manager):
    def creaet_account(self):
        self.model(
            
        )


class Account(models.Model):
    parent = models.ForeignKey('self', null = True, blank = True,
                            on_delete = models.SET_NULL, related_name = 'child')
    type = models.CharField(max_length = 255, choices = AccountTypeChoices.choices
                            # choices = [
                            # ('ASSETS', 'ASSETS'),
                            # ('LIABILITLES', 'LIABILITLES'),
                            # ('INCOME', 'INCOME'),
                            # ('EXPENSES', 'EXPENSES')
                            # ])
    )
    name = models.CharField(max_length = 255)
    code = models.CharField(max_length = 20, blank = True, null = True)
    full_code = models.CharField(max_length = 25, blank = True, null = True)
    # extra = models.JSONField(default = dict, null = True, blank = True)
    
    def __str__(self):
        return f'{self.full_code} - {self.name}'
    
    
    def balance(self):
        return self.journal_entries.values('currency').annotate(sum=Sum('amount')).order_by()
    
# # manner 2
# @receiver(post_save, sender = Account)
# def add_code_and_full_code(sender, instance, **kwargs):
#     instance.code = instance.id
#     if instance.parent:
#         instance.fill_code = f'{instance.parent.full_code}{instance.id}'
#     else:
#         instance.fill_code = instance.id

    
    # manner 3
    # def save(
    #     self, 
    # ):
    #     creating = not bool(self.id)
        
    #     if creating:
    #         self.code = self.id
    #         if self.parent:
    #             self.fill_code = f'{self.parent.full_code}{self.id}'
    #         else:
    #             self.fill_code = self.id
        
    #     super(Account, self).save()
    
class Transaction(models.Model):
    type = models.CharField(max_length = 255, choices = TransactionTypeChoices.choices)
                            # [
                            # ('invoice', 'invoice'),
                            # ('income', 'income'),
                            # ('expense', 'expense'),
                            # ('bill', 'bill')
                            # ])
    description = models.CharField(max_length = 255)
    
    def validate_account_equation(self):
        transaction_sum = self.journal_entries.aggregate(Sum('amount'))['sum__amount']
        if transaction_sum != 0:
            raise AccountingEquationError


class JournalEntry(models.Model):
    
    class Meta:
        verbose_name_plural = 'Journal Entries'
    
    account = models.ForeignKey(Account, on_delete = models.CASCADE, related_name = 'journal_entries')
    transaction = models.ForeignKey(Transaction, on_delete = models.CASCADE, related_name = 'journal_entries')#, to='Accounting.journal_entries'
    amount = models.DecimalField(max_digits = 19, decimal_places = 2)
    currency = models.CharField(max_length = 3, choices = CurrencyChoices.choices)
                            #     [
                            # ('USD', 'USD'),
                            # ('IQD', 'IQD'),
                            # ])
    
    def __str__(self):
        return f'{self.account.name} - {self.amount} - {self.currency}'


#Task 3 Balance Function Alterations ✍️(◔◡◔) ↓↓↓↓↓↓↓↓↓↓↓↓

class Balance:
    def __init__(self, balances):
        if balances:
            balance1 = balances[0]
            try:
                if balances[1]:
                    balance2 = balances[1]

                    if balance1['currency'] == 'USD':
                        balanceUSD = balance1['sum']
                        balanceIQD = balance2['sum']
                    else:
                        balanceIQD = balance1['sum']
                        balanceUSD = balance2['sum']

                    self.balanceUSD = balanceUSD
                    self.balanceIQD = balanceIQD
            except:
                if balance1['currency'] == 'USD':
                    balanceUSD = balance1['sum']
                    self.balanceUSD = balanceUSD
                    self.balanceIQD = 0
                else:
                    balanceIQD = balance1['sum']
                    self.balanceIQD = balanceIQD
                    self.balanceUSD = 0
        else:
            balanceUSD = 0
            balanceIQD = 0
            self.balanceUSD = balanceUSD
            self.balanceIQD = balanceIQD
    def __add__(self, other):
        try:
            if other.balanceIQD:
                self.balanceIQD += other.balanceIQD
        except: pass
        try:
            if other.balanceUSD:
                self.balanceUSD += other.balanceUSD
        except: pass
        
        return [{
            'currency': 'USD',
            'sum': self.balanceUSD
        }, {
            'currency': 'IQD',
            'sum': self.balanceIQD
        }]