from django.urls import path

from account.views import AccountView, TransactionView


urlpatterns = [
    path('accounts/', AccountView.as_view(), name='account_create_list'),
    path('accounts/<uuid:account_uid>/', AccountView.as_view(), name='account_detail'),
    path('accounts/<uuid:account_uid>/transactions/', TransactionView.as_view(), name='transaction_list_create')
]
