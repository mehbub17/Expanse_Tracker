from django.shortcuts import render,redirect
from .models import TrackingHistory,CurrentBalance
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login



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

def login_view(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = username)
        if not user.exists():
            messages.success(request, "account not found")
            return redirect("/login_page/")
        user = authenticate(username=username,password=password)
        
        if not user:
            messages.success(request,"Incorrect Password")
            return redirect('/login_page/')
        login(request,user)
        return redirect('/')
            
    
    return render(request,'login.html')


def register_view(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.success(request,"Username is already taken")
            return redirect("/register_page/")

        user = User.objects.create(
            username =username,
            first_name=first_name,
            last_name = last_name,
            
        )
        user.set_password(password) #encrypts password
        user.save()
        messages.success(request,"account created")
        return redirect("/register_page/")
    
    return render(request,'register.html')