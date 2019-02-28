
from django.urls import path

from .views import MembershipSelectView, payment_view

app_name = 'memberships'

urlpatterns = [
    path('', MembershipSelectView.as_view(), name='select'),
    path('payment', payment_view, name='payment')
]