from django.shortcuts import render,redirect
from .models import TrackingHistory,CurrentBalance
from django.db.models import Sum



def index(request):
    
    if request.method == "POST":
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        
        
        current_balance,_ = CurrentBalance.objects.get_or_create(id = 1)
        if float(amount) < 0:
            expense_type = "DEBIT"
        else:
            expense_type="CREDIT"
        
 
        
        tracking_history = TrackingHistory.objects.create(
            amount = amount,
            description = description,
            expense_type = expense_type,
            current_balance_id = current_balance.id
            
        )
        current_balance.current_balance += float(tracking_history.amount)
        current_balance.save()
        
        return redirect('/')
    current_balance,_ = CurrentBalance.objects.get_or_create(id = 1)
    
    income = 0
    expense = 0
    for track in TrackingHistory.objects.all():
        if track.amount < 0:
            expense-=track.amount
        else:
            income+=track.amount
        
        
            
    context = {"transactions":TrackingHistory.objects.all(),'current_balance':current_balance,'income':income,'expense':expense}
        
    
    return render(request,'index.html',context)


def delete_transaction(request,id):
    tracking_history  = TrackingHistory.objects.filter(id = id)
    
    if tracking_history.exists():
        current_balance,_ = CurrentBalance.objects.get_or_create(id = 1)
        
        tracking_history = tracking_history[0]
        
        current_balance.current_balance -= float(tracking_history.amount)
        current_balance.save()
    
    tracking_history.delete()
    return redirect('/')