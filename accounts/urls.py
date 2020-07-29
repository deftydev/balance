from django.urls import include, path

from . import views

urlpatterns = [
    path('create/', views.TransactionCreateView.as_view() ,name='create'),
    path('payment/',views.PaymentCreateView.as_view(), name='paymentt'),
    path('spending/',views.SpendingCreateView.as_view(), name='spendingg'),
    path('balance/',views.BalanceCreateView.as_view(), name='balance'),
    path('logout', views.logout ,name='logout'),
    path('login', views.login ,name='login'),

]
