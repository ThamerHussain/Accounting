from decimal import Decimal
from locale import currency
from pydoc import describe
from typing import Optional
from Accounting.models import Account
from typing import List

# way 1
# from ninja import ModelSchema

# class AccountOut(ModelSchema):
#     class Config:
#         model = Account
#         model_fields = [
#             'parent',
#             'type',
#             'name',
#             'code',
#             'full_code'
#             ]

# way 2 _ manually _ 1
# from ninja import Schema

# class AccountOut(Schema):
#     parent_id: int = None
#     name: str
#     type: str
#     code: str
#     full_code: str

# way 2 _ manually _ 2
from ninja import Schema

class AccountOut(Schema):
    id: int
    parent: 'AccountOut' = None
    name: str
    type: str
    code: str
    full_code: str
AccountOut.update_forward_refs()

class FourOFourOut(Schema):
    detail: str
    
class StandAloneJournalEntry(Schema):
    id: int
    amount: Decimal
    currency: str

class TransactionOut(Schema):
    type: str
    description: str

class TransactionOutSchema(Schema):
    Transaction: TransactionOut
    jes: List[StandAloneJournalEntry]

class JournalEntry(Schema):
    account: AccountOut
    transaction: TransactionOut
    amount: Decimal
    currency: str
    
class JournalEntryOut(JournalEntry):
    id: int

class JournalEntryIn(JournalEntry):
    pass

class JournalEntryInTransaction(Schema):
    credit_account: int
    debit_account: int
    amount: Decimal
    currency: str

class TransactionIn(Schema):
    type: str
    description: str
    je: JournalEntryInTransaction

class CurrencyBalance(Schema):
    currency: str
    sum: str

class GeneralLedgerOut(Schema):
    account: str
    balance: List[CurrencyBalance]
    # jes: List[JournalEntryOut]

#Task 3 Schema ✍️(◔◡◔) ↓↓↓↓↓↓↓↓↓↓↓↓

class TotalBalance(Schema):
    account: str
    account_id: int
    children_ids: str
    total_balance: List[CurrencyBalance]