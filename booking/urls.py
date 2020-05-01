from django.urls import include, path
from booking.views import (CreateProfitPercentageView, UpdateProfitPercentageView,
                            BookingView, CancellingView, CantCancellView,
                            CancellingErrorView, SignContractView, ContractSuccessView,
                            NotAvailableSessionsView, NoSessionErrorView, CancelSuccessView,
                            BookedSessionListView, ContractListView, ContractDetailView,
                            CancelSuccessBySportclubView, CancellingBySportclubView)


app_name ='booking'
urlpatterns = [
    path('create-profit-percentage/', CreateProfitPercentageView.as_view(), name='createprofitpercentage'),
    path('update-profit-percentage/<int:pk>/', UpdateProfitPercentageView.as_view(), name='updateprofitpercentage'),
    path('booking/<int:pk>/', BookingView, name='booksession'),
    path('contract-detail/', ContractDetailView, name='contractdetail'),
    path('sign-contract/<int:pk>/', SignContractView, name='signcontract'),
    path('cancelling/<int:pk>/', CancellingView, name='cancelsession'),
    path('booked-session-list/<int:pk>/', BookedSessionListView, name='bookedsessionlist'),
    path('contract-list/<int:pk>/', ContractListView, name='contractlist'),
    path('cancelling-error/', CancellingErrorView.as_view(), name='cancellingerror'),
    path('cant-cancel/', CantCancellView.as_view(), name='cantcancell'),
    path('contract-success/', ContractSuccessView.as_view(), name='contractsuccess'),
    path('not-available-sessions/', NotAvailableSessionsView.as_view(), name='notavailablesessions'),
    path('no-sessions/', NoSessionErrorView.as_view(), name='nosessionerror'),
    path('cancel-success/', CancelSuccessView.as_view(), name='cancelsuccess'),
    path('cancelling-by-sportclub/<int:pk>/', CancellingBySportclubView, name='cancelsessionbysportclub'),
    path('cancel-success-by-sportclub/', CancelSuccessBySportclubView.as_view(), name='cancelsuccessbysportclub'),


]
