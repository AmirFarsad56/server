from django.urls import include, path
from accounts.views import (SuperUserProfileView, SuperUserUpdateView,
                            CloudMessageView, CloudEmailView, PasswordChangeView,
                            SuperUserWorkSpaceView, DeleteInactiveUsersView,
                            ForgotPasswordView, WrongPhoneNumberView)

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
]
