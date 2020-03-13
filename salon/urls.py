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
    path('sportclub-profile/<slug:slug>/createsalon/', SalonCreateView, name='createsalon'),
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
    path('confirm/<int:pk>/',SalonConfirmView, name='confirm'),
    path('accounting-detail/<int:pk>/',SalonAccountingDetailView, name='accountingdetail'),
    path('picture-update/<int:pk>/',SalonPictureUpdateView, name='pictureupdate'),
    path('picture-add/<int:pk>/',SalonPictureAddView, name='pictureadd'),
    path('confirm-2/<int:pk>/',SalonConfirmView_2, name='confirm_2'),
    path('delete/<int:pk>/',SalonDeleteView, name='delete'),
    path('ban/<int:pk>/',SalonBanView, name='ban'),
    path('reckoning/<int:pk>/',SalonReckoningView, name='reckoning'),
    path('reckoning-list/<int:pk>/',SalonReckoninglistView, name='reckoninglist'),
    path('ban-2/<int:pk>/',SalonBanView_2, name='ban_2'),

    path('detail-masteruser/<int:pk>/',SalonDetailViewMasterUser, name='detail'),
    path('set-profit-percentage/<int:pk>/',SalonSetProfitPercentage, name='setprofitpercentage'),

]
