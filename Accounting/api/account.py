from genericpath import exists
from unittest import result
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from urllib import request
from django.shortcuts import get_object_or_404
from ninja import Router
from rest_framework import status
# import re
from typing import List
from django.db.models import Sum
from ninja.security import django_auth
from Accounting.models import Account, AccountTypeChoices, Balance, JournalEntry
from Accounting.schemas import AccountOut, FourOFourOut, GeneralLedgerOut, TotalBalance
from ninja.security import HttpBearer

from Accounting.services import get_balance_by_id

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == 'supersecret':
            return token

account_router = Router()


@account_router.get('/accounts', response = List[AccountOut], auth = AuthBearer())
def list_accounts(request):
    # return Account.objects.all()
    print(request.auth)
    return status.HTTP_200_OK, Account.objects.order_by('full_code')


@account_router.get('/accounts/{account_id}', response = {
    200: AccountOut,
    404: FourOFourOut
})
def get_account(request, account_id: int):
    try: return Account.objects.get(id = account_id)
    except Account.DoesNotExist: 
        return 404, {'detail': f'Account with id {account_id} does not exist'}
    
@account_router.get('/get_account_type/')
def get_account_types(request):
    result = {}
    for t in AccountTypeChoices.choices:
        result[t[0]] = t[1]
    return result



@account_router.get('/account-balance/{account_id}', response = GeneralLedgerOut)
def get_account_balance(request, account_id: int):
    account = get_object_or_404(Account, id = account_id)
    
    journal_entries = account.journal_entries.all()
    # journal_entries = account.journal_entries.values()
    balance = account.journal_entries.values('currency').annotate(sum = Sum('amount')).order_by()
    # print(balance)
    #.aggregate(Sum('amount'))['amount__sum']
    return 200, {'account': account.name, 'balance': list(balance), 'jes': list(journal_entries)}




#Task 3 Functions ✍️(◔◡◔) ↓↓↓↓↓↓↓↓↓↓↓↓

@account_router.get('/total-account-balances/', response=List[TotalBalance])
def get_total_account_balances(request):
    accounts = Account.objects.all()
    total_balances = []
    for account in accounts:
        result = get_balance_by_id(account.id)
        total_balances.append(
            {'account': f'{result[1]}', 'account_id': account.id, 'children_ids': f'{result[2]}', 'total_balance': result[0]}
        )
    return status.HTTP_200_OK, total_balances


@account_router.get('/total-account-balance/', response = {200: TotalBalance, 404: FourOFourOut})
def get_total_account_balance(request, account_id: int):
    result = get_balance_by_id(account_id)
    try:
        result = {'account': f'{result[1]}', 'account_id': account_id, 'children_ids': f'{result[2]}', 'total_balance': result[0]}
        return 200, result
    except: 
        return 404, {'detail': f'Account with id {account_id} does not exist'}




def get_account_balances_old(request, id):
    # # print(Account)
    try:
        account = Account.objects.get(id = id)
        # print(account.id)
        # # print(account.child.all())
        # # [print(a.child.all()) for a in account.child.all()]
        # inc = '.child.all()'
        # children = []
        # # child = account.child.all()
        # rest = 'child'
        # x = 'account.child.all()'
        # myVars = vars()
        # myVars[x] = x
        # while 1:تكدر بدون سترنك جرّب
        # صارت ^_^
            
        #     if x.isidentifier():
        #         print(11111)
                
        #     else:break
        total_balance = Balance(account.balance())
        x = account
        print('\n\n\n\nParent ID:',x.id,'\n')
        # print('total_balance')
        # print('IQD', total_balance.balanceIQD)
        # print('USD', total_balance.balanceUSD)            
        c = 1
        while 1:
            try:
                x = x.child.all()[0]
                if x:
                    print('Child ID:',x.id)
                    balance_x = Balance(x.balance())
                    # print(balance_x.balanceUSD)
                    # print(x.id)
                    # print('------------------------')
                    print('child_balance:')
                    # print('------------------------')
                    
                    # try:
                        # if balance_x.balanceIQD:
                    print('IQD:', balance_x.balanceIQD)
                        # else:
                        #     print('IQD:', balance_x.balanceIQD)
                    
                    # except:
                    #     print("dont have IQD")
                    
                    # try:
                        # if balance_x.balanceUSD:
                    print('USD:', balance_x.balanceUSD)
                        # else:
                        #     print('USD:', balance_x.balanceUSD)
                        # print('//////////////////')
                        # print('9+++++++++++++++++++++++++++')
                    
                    # except:
                    #     print("dont have USD")
                    
                    total_balance.__add__(balance_x)
                    # print('total_balance')
                    # print('-------------------------')
                    # print('IQD', total_balance.balanceIQD)
                    # print('USD', total_balance.balanceUSD)
                    print(f'Child {c} done!\n')
                    c += 1
                    # print(x.id, x.balance())     
                # else: 
                #     balance_x = Balance(x.balance())
            except Exception:
                # print(x.id, 'USD', x.balance())
                # print(x.id, 'USD', Balance(x.balance()).balanceUSD)
                # print(9999999999999999)
                break
            #     print(Exception) 
            #     break
        print(f'The total_balance of account {account.id} is:')
        print('                                   IQD:', total_balance.balanceIQD)
        print('                                   USD:', total_balance.balanceUSD)
                    
        a = f'The total_balance of account {account.id} is:'
        b = 'IQD:', total_balance.balanceIQD
        c = 'USD:', total_balance.balanceUSD
        
        # print(total_balance)
        # return status.HTTP_200_OK
        # accounts = Account.objects.all()
        # result = []
        # for a in accounts:
        #     result.append({
        #         'account': a.name, 'balance': list(a.Tbalance())
        #     })
        return status.HTTP_200_OK, f"The total balance of account {account.id} is:     in USD ====> {total_balance.balanceUSD}     in IQD ====> {total_balance.balanceIQD} "
    except:
        print("\n\nThis Account doesn't exist\n\n")
        return "This Account doesn't exist"










# @account_router.get('/account-balances/', )#response=List[GeneralLedgerOut])
def get_account_balances_the_origin_function(request, id):
    # # print(Account)
    try:
        account = Account.objects.get(id = id)
        # print(account.id)
        # # print(account.child.all())
        # # [print(a.child.all()) for a in account.child.all()]
        # inc = '.child.all()'
        # children = []
        # # child = account.child.all()
        # rest = 'child'
        # x = 'account.child.all()'
        # myVars = vars()
        # myVars[x] = x
        # while 1:تكدر بدون سترنك جرّب
        # صارت ^_^
            
        #     if x.isidentifier():
        #         print(11111)
                
        #     else:break
        total_balance = Balance(account.balance())
        x = account
        print('\n\n\n\nParent ID:',x.id,'\n')
        # print('total_balance')
        # print('IQD', total_balance.balanceIQD)
        # print('USD', total_balance.balanceUSD)            
        c = 1
        while 1:
            try:
                x = x.child.all()[0]
                if x:
                    print('Child ID:',x.id)
                    balance_x = Balance(x.balance())
                    # print(balance_x.balanceUSD)
                    # print(x.id)
                    # print('------------------------')
                    print('child_balance:')
                    # print('------------------------')
                    
                    # try:
                        # if balance_x.balanceIQD:
                    print('IQD:', balance_x.balanceIQD)
                        # else:
                        #     print('IQD:', balance_x.balanceIQD)
                    
                    # except:
                    #     print("dont have IQD")
                    
                    # try:
                        # if balance_x.balanceUSD:
                    print('USD:', balance_x.balanceUSD)
                        # else:
                        #     print('USD:', balance_x.balanceUSD)
                        # print('//////////////////')
                        # print('9+++++++++++++++++++++++++++')
                    
                    # except:
                    #     print("dont have USD")
                    
                    total_balance.__add__(balance_x)
                    # print('total_balance')
                    # print('-------------------------')
                    # print('IQD', total_balance.balanceIQD)
                    # print('USD', total_balance.balanceUSD)
                    print(f'Child {c} done!\n')
                    c += 1
                    # print(x.id, x.balance())     
                # else: 
                #     balance_x = Balance(x.balance())
            except Exception:
                # print(x.id, 'USD', x.balance())
                # print(x.id, 'USD', Balance(x.balance()).balanceUSD)
                # print(9999999999999999)
                break
            #     print(Exception) 
            #     break
        print(f'The total_balance of account {account.id} is:')
        print('                                   IQD:', total_balance.balanceIQD)
        print('                                   USD:', total_balance.balanceUSD)
                    
        a = f'The total_balance of account {account.id} is:'
        b = 'IQD:', total_balance.balanceIQD
        c = 'USD:', total_balance.balanceUSD
        
        # print(total_balance)
        # return status.HTTP_200_OK
        # accounts = Account.objects.all()
        # result = []
        # for a in accounts:
        #     result.append({
        #         'account': a.name, 'balance': list(a.Tbalance())
        #     })
        return status.HTTP_200_OK, f"The total balance of account {account.id} is:  in USD: {total_balance.balanceUSD}  -  in IQD: {total_balance.balanceIQD}"
    except:
        print("\n\nThis Account doesn't exist\n\n")
        return "This Account doesn't exist"











#1, 15, 156, 2, 27, 278, 3, 4 work with iiiiiiiddddddd not code or full code


    # sum_USD = None
    # sum_IQD = None
    #     # if a.crn:#{list(a.balance())}
    #             # print('++++++++++++++++')
    # for a in accounts:
    #     print(f'{a.id} ====> {get_acc(a)}')
    #     # if list(a.crn.all()):
    #     # if a.crn:
    #     #     # print(f'{a.id} ====> ', *[b.id for b in a.crn.all() ])
    #     #     for i in a.crn.all():
    #     #[b for b in a.crn]
    #     #     print(f'{a.id} ====>  ====> {a.parent.id} ====> ')
    #     # else:print(f'{a.id} ====> ')
    #     # result.append({
    #     #     'account': a.name, 'balance': list(a.balance())
    #     # })

