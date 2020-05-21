from django.urls import include, path
from accounts.views import (SuperUserProfileView, SuperUserUpdateView,
                            CloudMessageView, CloudEmailView, PasswordChangeView,
                            SuperUserWorkSpaceView, DeleteInactiveUsersView,
                            ForgotPasswordView, WrongPhoneNumberView)
from django.contrib.auth import views as auth_views

app_name ='accounts'
urlpatterns = [
    path('superuser/profile/<slug:slug>/', SuperUserProfileView, name='profile'),
    path('superuser/workspace/<slug:slug>/', SuperUserWorkSpaceView, name='workspace'),
    path('superuser/update/<slug:slug>/', SuperUserUpdateView, name='update'),
    path('superuser/cloud-message/', CloudMessageView, name='cloudmessage'),
    path('superuser/cloud-email/', CloudEmailView, name='cloudemail'),
    path('passwordchange/<slug:slug>/', PasswordChangeView, name='passwordchange'),
    path('superuser/delete-inactive-users/', DeleteInactiveUsersView, name='deleteinactiveusers'),
    path('forgot-password/', ForgotPasswordView, name='forgotpassword'),
    path('wrong-phone-number/', WrongPhoneNumberView, name='wrongphonenumber'),
    path('auth/',auth_views.LoginView.as_view(template_name='registration/login0.html'), name='login'),
]
