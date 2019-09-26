from django.urls import include, path
from accounts.views import (SuperUserProfileView, SuperUserUpdateView,
                            CloudMessageView, CloudEmailView, PasswordChangeView,
                            SuperUserWorkSpaceView, DeleteInactiveUsersView,
                            ForgotPasswordView, WrongPhoneNumberView)

app_name ='accounts'
urlpatterns = [
    path('profile/<slug:slug>/', SuperUserProfileView, name='profile'),
    path('workspace/<slug:slug>/', SuperUserWorkSpaceView, name='workspace'),
    path('update/<slug:slug>/', SuperUserUpdateView, name='update'),
    path('cloud-message/', CloudMessageView, name='cloudmessage'),
    path('cloud-email/', CloudEmailView, name='cloudemail'),
    path('passwordchange/<slug:slug>/', PasswordChangeView, name='passwordchange'),
    path('delete-inactive-users/', DeleteInactiveUsersView, name='deleteinactiveusers'),
    path('forgot-password/', ForgotPasswordView, name='forgotpassword'),
    path('wrong-phone-number/', WrongPhoneNumberView, name='wrongphonenumber'),
]
