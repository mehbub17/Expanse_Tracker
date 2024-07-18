from django.contrib import admin
from tracker.models import *

# Register your models here.
admin.site.site_header = "Expense Tracker"
admin.site.site_title = "Expense Tracker"
admin.site.site_url = "Expense Tracker"

admin.site.register(CurrentBalance)

@admin.action(description="Mark selected expenses as Credit")
def make_credit(modeladmin, request, queryset):
    queryset.update(expense_type="CREDIT")
    current_balance = CurrentBalance.objects.get(id=1)
    for expense in queryset:
        if int(expense.amount) < 0:
            expense.amount = abs(expense.amount)
            current_balance.current_balance+=2*expense.amount
            current_balance.save()
            expense.save()

@admin.action(description="Mark selected expenses as DEBIT")
def make_debit(modeladmin, request, queryset):
    queryset.update(expense_type="DEBIT")
    current_balance = CurrentBalance.objects.get(id=1)
    for expense in queryset:
        if int(expense.amount) > 0:
            expense.amount = -expense.amount
            current_balance.current_balance+=2*expense.amount
            current_balance.save()
            expense.save()


class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display = ['amount','current_balance','expense_type','description','created_at','display_amount']
    search_fields=['expense_type','created_at','description']
    ordering = ['-created_at']
    list_filter = ['expense_type']
    actions = [make_credit,make_debit]
    
    def display_amount(self,obj):
        if obj.amount > 0:
            return "Positive"
        return "Negative"

admin.site.register(TrackingHistory,TrackingHistoryAdmin)