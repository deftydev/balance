from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView

from .forms import OfficeSignUpForm,EmployerSignUpForm,AgentSignUpForm

from django.views.generic import TemplateView
from django.contrib import auth

from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction,Payment,Employee_spending,User,Balance
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from .decorators import agent_required,employer_required,office_required


def login(request):
    if request.method == 'POST':
        user=auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request,user)
            if user.is_employer:
                return redirect('signup')
            elif user.is_agent:
                return redirect('payment')
            else:
                return redirect('spending')

        else:
            return render(request, 'accounts/signup.html', {'error':'Username or password is incorrect'})


    else:
        return render(request, 'accounts/login.html')

class OfficeSignUpView(CreateView):
    model = User
    form_class = OfficeSignUpForm
    template_name = 'accounts/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'office'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request,user)
        return redirect('payment')

class EmployerSignUpView(CreateView):
    model = User
    form_class = EmployerSignUpForm
    template_name = 'accounts/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request,user)
        return redirect('homee')

class AgentSignUpView(CreateView):
    model = User
    form_class = AgentSignUpForm
    template_name = 'accounts/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'agent'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request,user)
        return redirect('payment')


class SignUpView(TemplateView):
    template_name = 'accounts/signup.html'


def home1(request):
    if request.user.is_authenticated:
        if request.user.is_employer:
            return redirect('homee')
        else:
            return redirect('payment')
    return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')
    else:
        return render(request, 'accounts/logout.html')


@method_decorator([login_required], name='dispatch')
class TransactionCreateView(CreateView):
    model=Transaction
    template_name='accounts/create.html'
    fields=['to_user','amount']
    def form_valid(self,form):
        instance=form.save(commit=False)
        instance.user=self.request.user
        instance.save()
        return redirect('homee')


class TransactionPageView(LoginRequiredMixin,ListView):
    template_name='accounts/homee.html'
    model = Transaction
    context_object_name='transactions'

    def get_queryset(self):
        transactions = super().get_queryset()
        return transactions


class PaymentPageView(LoginRequiredMixin,ListView):
    template_name='accounts/payment.html'
    model = Payment
    context_object_name='payments'

    def get_queryset(self):
        payments = super().get_queryset()
        return payments



@method_decorator([login_required], name='dispatch')
class PaymentCreateView(CreateView):
    model=Payment
    template_name='accounts/createee.html'
    fields=['customer_name','amount']
    def form_valid(self,form):
        instance=form.save(commit=False)
        instance.user=self.request.user
        instance.save()
        return redirect('payment')


@method_decorator([login_required], name='dispatch')
class BalanceCreateView(CreateView):
    model=Balance
    template_name='accounts/balance.html'
    fields=['user','balance','contact']
    def form_valid(self,form):
        instance=form.save(commit=False)
        instance.save()
        return redirect('homee')



class SpendingPageView(LoginRequiredMixin,ListView):
    template_name='accounts/employee.html'
    model = Employee_spending
    context_object_name='employees'

    def get_queryset(self):
        employees = super().get_queryset()
        return employees


@method_decorator([login_required ], name='dispatch')
class SpendingCreateView(CreateView):
    model= Employee_spending
    template_name='accounts/createe.html'
    fields=['name','description','quantity','image','amount']
    def form_valid(self,form):
        instance=form.save(commit=False)
        instance.user=self.request.user
        instance.save()
        return redirect('spending')
