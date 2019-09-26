from django.urls import include, path
from salon.views import (SalonCreateView, SalonUpdateView, SalonDetailView,
                        ConfirmedSalonListView, UnConfirmedSalonListView,
                        SalonConfirmView, SalonDeleteView, SalonBanView,
                        SalonDetailViewMasterUser,SalonSetProfitPercentage,
                        SalonConfirmView_2,SalonBanView_2,
                        SalonPictureUpdateView, SalonPictureAddView,
                        SalonAccountingDetailView, SalonReckoningView,SalonReckoninglistView,
                        SalonListSuperUserView, SalonPublicListView,
                        SalonPublicListForSpecificSportClubView, )


app_name ='salon'
urlpatterns = [
    path('profile/<slug:slug>/createsalon/', SalonCreateView, name='createsalon'),
    path('confirmed-salon-list/',ConfirmedSalonListView,
        name='confirmedsalonlist'),
    path('unconfirmed-salon-list/',UnConfirmedSalonListView,
        name='unconfirmedsalonlist'),
    path('salon-list-for-superuser/',SalonListSuperUserView,
        name='salonlistforsuperuser'),
    path('salon-Plist/',SalonPublicListView,
        name='publiclist'),
    path('salon-Plist-sportclub/<int:pk>/',SalonPublicListForSpecificSportClubView,
        name='publiclistforsportclub'),
    path('sportclub/<slug:slug>/profile/updatesalon/<int:pk>/',SalonUpdateView, name='update'),
    path('sportclub/profile/salondetail/<int:pk>/',SalonDetailView.as_view(), name='salondetail'),
    path('salon/confirm/<int:pk>/',SalonConfirmView, name='confirm'),
    path('salon/accounting-detail/<int:pk>/',SalonAccountingDetailView, name='accountingdetail'),
    path('salon/picture-update/<int:pk>/',SalonPictureUpdateView, name='pictureupdate'),
    path('salon/picture-add/<int:pk>/',SalonPictureAddView, name='pictureadd'),
    path('salon/confirm-2/<int:pk>/',SalonConfirmView_2, name='confirm_2'),
    path('salon/delete/<int:pk>/',SalonDeleteView, name='delete'),
    path('salon/ban/<int:pk>/',SalonBanView, name='ban'),
    path('salon/reckoning/<int:pk>/',SalonReckoningView, name='reckoning'),
    path('salon/reckoning-list/<int:pk>/',SalonReckoninglistView, name='reckoninglist'),
    path('salon/ban-2/<int:pk>/',SalonBanView_2, name='ban_2'),

    path('salon/detail/<int:pk>/',SalonDetailViewMasterUser, name='detail'),
    path('salon/setprofitpercentage/<int:pk>/',SalonSetProfitPercentage, name='setprofitpercentage'),

]
