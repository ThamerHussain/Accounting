from typing import List
from ninja import Router

from Accounting.models import JournalEntry
from Accounting.schemas import JournalEntryOut

je_router = Router()

@je_router.get('/get-all', response = List[JournalEntryOut])
def get_all(request):
    jes = JournalEntry.objects.all()
    return 200, jes