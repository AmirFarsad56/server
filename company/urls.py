from django.urls import include, path
from company.views import (CreateTermsView, UpdateTermsView, AccountingDetailView, ReckoninglistView,
                            SalonAdvertisementCreateView, SalonAdvertisementListView,
                            SalonAdvertisementDeleteView, TermsDetailView, FAQsView,
                            AboutUsView, ContactUsView, TestView, ThanksView, SportClubContactView,
                            ContactSuccessView)


app_name ='company'
urlpatterns = [
    path('create-terms/', CreateTermsView.as_view(), name='createterms'),
    path('terms-detail/', TermsDetailView, name='termsdetail'),
    path('about-us/', AboutUsView, name='aboutus'),
    path('thanks/', ThanksView, name='thanks'),
    path('contact-success/', ContactSuccessView, name='contactsuccess'),
    path('contact-us/', ContactUsView, name='contactus'),
    path('sportclub-contact/', SportClubContactView, name='sportclubcontact'),
    path('FAQs/', FAQsView, name='faqs'),
    path('accounting-detail/', AccountingDetailView, name='accountingdetail'),
    path('reckoning-list/', ReckoninglistView, name='reckoninglist'),
    path('update-terms/<int:pk>/', UpdateTermsView.as_view(), name='updateterms'),
    path('salon-advertisement-add/<int:pk>/', SalonAdvertisementCreateView, name='salonadvertisementcreate'),
    path('salon-advertisement-list/', SalonAdvertisementListView.as_view(), name='salonadvertisementlist'),
    path('salon-advertisement-delete/<int:pk>/', SalonAdvertisementDeleteView, name='salonadvertisementdelete'),
    path('test/', TestView, name='test'),

]
