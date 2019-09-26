from django.urls import include, path
from masteruser.views import (MasterUserSignupView, MasterUserListView,
                              MasterUserBanView,MasterUserUnBanView,
                              MasterUserDeleteView,MasterUserProfileView,
                              BannedMasterUserListView, MasterUserDetailView,
                              MesssageSendingView, EmailSendingView,
                              MasterUserUpdateView, WorkSpaceView,BanModalView,
                              DeleteModalView,UnBanModalView)

app_name ='masteruser'
urlpatterns = [
    path('signup/', MasterUserSignupView, name='signup'),
    path('profile/<slug:slug>', MasterUserProfileView, name='profile'),
    path('workspace/<slug:slug>/', WorkSpaceView, name='workspace'),
    path('list/', MasterUserListView.as_view(), name='list'),
    path('bannedlist/', BannedMasterUserListView.as_view(), name='bannedlist'),
    path('<slug:slug>/ban/',MasterUserBanView, name='ban'),
    path('<slug:slug>/ban-modal/',BanModalView, name='banmodal'),
    path('<slug:slug>/unban/',MasterUserUnBanView, name='unban'),
    path('<slug:slug>/unban-modal/',UnBanModalView, name='unbanmodal'),
    path('<slug:slug>/delete/',MasterUserDeleteView, name='delete'),
    path('<slug:slug>/delete-modal/',DeleteModalView, name='deletemodal'),
    path('detail/<slug:slug>/',MasterUserDetailView, name='detail'),
    path('sendsms/<slug:slug>/',MesssageSendingView, name='sendsms'),
    path('sendemail/<slug:slug>/',EmailSendingView, name='sendemail'),
    path('update/<slug:slug>/', MasterUserUpdateView, name='update'),

]
