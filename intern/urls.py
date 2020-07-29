from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from accounts import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('home/', views.home1 , name='home1'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/signup/agent/', views.AgentSignUpView.as_view(), name='agent_signup'),
    path('accounts/signup/employer/', views.EmployerSignUpView.as_view(), name='employer_signup'),
    path('accounts/signup/office/', views.OfficeSignUpView.as_view(), name='office_signup'),
    path('homee/',views.TransactionPageView.as_view(), name='homee'),
    path('payment/',views.PaymentPageView.as_view(), name='payment'),
    path('spending/',views.SpendingPageView.as_view(), name='spending'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
