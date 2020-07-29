from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Transaction,Payment, Balance,Employee_spending

User = get_user_model()

admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Balance)
admin.site.register(Payment)
admin.site.register(Employee_spending)
