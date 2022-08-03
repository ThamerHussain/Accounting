from .models import Account


def get_account_balances(id = 1):
    # print(Account)
    account = Account.objects.get(id = id)
    # print(account.id)
    # print(accounts)
    # result = [Account.objects.all()]

    return None

get_account_balances()
