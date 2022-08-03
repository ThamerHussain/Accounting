# from genericpath import exists
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
# from urllib import request
# from ninja import Router
# import re
# from typing import List

# from Accounting.models import Account
# from Accounting.schemas import AccountOut, FourOFourOut


# router = Router()


# @router.get('/accounts', response = List[AccountOut])
# def list_accounts(request):
#     return Account.objects.all()


# @router.get('/accounts/{account_id}', response = {
#     200: AccountOut,
#     404: FourOFourOut
# })
# def get_account(request, account_id: int):
#     try: return Account.objects.get(id = account_id)
#     except Account.DoesNotExist: 
#         return 404, {'detail': f'Account with id {account_id} does not exist'}