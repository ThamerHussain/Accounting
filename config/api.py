from os import scandir
from ninja import NinjaAPI
from ninja.security import django_auth
from Accounting.api.account import account_router
from Accounting.api.transaction import t_router
from Accounting.api.journal_entry import je_router

api = NinjaAPI(
    title = 'My Practicing Project "Accounting"',
    version = '0.1',
    description = 'He said that this project will cover lots of aspects',
    csrf = True
)

api.add_router('/Account/', account_router)
api.add_router('/transaction/', t_router)
api.add_router('/journal_entry/', je_router)