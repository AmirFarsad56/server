from django.urls import include, path
from commonuser.views import (CommonUserSignupView, CommonUserProfileView,
                              CommonUserListView, CommonUserBanView,
                              CommonUserUnBanView,
                              CommonUserDeleteView, BannedCommonUserListView,
                              MesssageSendingView, EmailSendingView,
                              CommonUserUpdateView, UserConfirmView, TwoMinWaitView,
                              CommonUserDashboardView,)

app_name ='commonuser'
urlpatterns = [
    path('signup/', CommonUserSignupView, name='signup'),
    path('profile/<slug:slug>/',CommonUserProfileView,
         name = 'profile'),
    path('list/', CommonUserListView.as_view(), name='list'),
    path('confirm/', UserConfirmView, name='confirmation'),
    path('two-min-wait/', TwoMinWaitView, name='twominwait'),
    path('bannedlist/', BannedCommonUserListView.as_view(), name='bannedlist'),
    path('<slug:slug>/dashboard/', CommonUserDashboardView, name='dashboard'),
    path('ban/<slug:slug>/', CommonUserBanView, name='ban'),
    path('unban/<slug:slug>/', CommonUserUnBanView, name='unban'),
    path('delete/<slug:slug>/', CommonUserDeleteView, name='delete'),
    path('sendsms/<slug:slug>/',MesssageSendingView, name='sendsms'),
    path('sendemail/<slug:slug>/',EmailSendingView, name='sendemail'),
    path('update/<slug:slug>/', CommonUserUpdateView, name='update'),

]
