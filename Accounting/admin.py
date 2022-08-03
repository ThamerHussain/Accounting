from unicodedata import name
from django.contrib import admin

from Accounting.models import Account, JournalEntry, Transaction

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'type', 'code', 'full_code']
    search_fields = ['name', 'code', 'full_code']
    list_filter = ['type']
    ordering = ['full_code']

admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction)
admin.site.register(JournalEntry)