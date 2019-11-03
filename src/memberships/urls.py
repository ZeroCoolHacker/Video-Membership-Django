
from django.urls import path

from .views import MembershipSelectView, payment_view, update_transactions

app_name = 'memberships'

urlpatterns = [
    path('', MembershipSelectView.as_view(), name='select'),
    path('payment/', payment_view, name='payment'),
    path('update-transactions/<subscription_id>/', update_transactions, name='update-transactions')
]