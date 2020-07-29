from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from accounts.models import Office, User, Agent

class OfficeSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_office = True
        user.save()
        office = Office.objects.create(user=user)
        return user

class AgentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_agent = True
        user.save()
        agent = Agent.objects.create(user=user)
        return user


class EmployerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employer = True
        if commit:
            user.save()
        return user
