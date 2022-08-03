from typing import List
from ninja import Router
from rest_framework import status
from Accounting.exceptions import AccountingEquationError, AtomicAccountTransferException, ZeroAmountError

from Accounting.models import JournalEntry, Transaction
from Accounting.schemas import TransactionIn, TransactionOutSchema
from Accounting import services


t_router = Router()

# @t_router.get('/get-all', response = List[TransactionIn])
# def get_all(request):
#     Transactions = Transaction.objects.all()
#     return 200, Transactions

@t_router.post('/add-transaction', response = TransactionOutSchema)
def add_transaction(
    request,
    transaction_in: TransactionIn
    ):
    
    # operation = services.account_transfer(transaction_in)
    t = services.account_transfer(transaction_in)
    return status.HTTP_200_OK, {
        'transaction': t,
        'jes': t.journal_entries.all()# *_*
    }