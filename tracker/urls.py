from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('delete-transaction/<id>/',views.delete_transaction,name='delete_transaction'),
    
    path('login_page/',views.login_view,name='login-view'),
    path('login_out/',views.logout_view,name='logout-view'),
    path('register_page/',views.register_view,name='register-view'),
]