from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

from .models import Membership, UserMembership, Subscription

import stripe



def get_user_membership(request):
    """
    Gets the membership of the user attached to request
    """

    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None


def get_user_subscription(request):
    """
    Get the current subscription of the user attached to the request
    """
    subsription_qs = Subscription.objects.filter(
        user_membership=get_user_membership(request),
    )
    if subsription_qs.exists():
        user_subscription = subsription_qs.first()
        return user_subscription
    return None


def get_selected_membership(request):
    """
    Gets the selected membership for payment form
    """

    membership_type = request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(
        membership_type=membership_type
    )
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None

class MembershipSelectView(ListView):
    """
    Select Membership
    """

    model = Membership
    # template_name = 'memberships/membership_list.html'
    
    
    def get_context_data(self, *args, **kwargs):
        """
        Gets the context data passed into the view
        Add current_membership variable to it
        """
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership)
        return context
    
    def post(self, request, *args, **kwargs):
        selected_membership_type = request.POST.get('membership_type')
        user_membership     = get_user_membership(request)
        user_subscription   = get_user_subscription(request)

        selected_membership_qs = Membership.objects.filter(
            membership_type=selected_membership_type
        )
        
        if selected_membership_qs.exists():
            selected_membership = selected_membership_qs.first()
        '''
        ==========
        VALIDATION
        ==========
        '''

        if user_membership == selected_membership:
            if user_subscription != None:
                messages.info(
                    request,
                    'You already have this membership. Your next payment is \
                    due {}'.format('get this value from the stripe')
                    )
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        # Assign to the session
        request.session['selected_membership_type'] = selected_membership.membership_type
        return HttpResponseRedirect(reverse('memberships:payment'))


def payment_view(request):
    """
    Provide the user with the stripe payment form
    and handle the actual payment form
    """

    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)

    publish_key = settings.STRIPE_PUBLISHABLE_KEY

    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            print(token)
            subscription = stripe.Subscription.create(
                customer=user_membership.stripe_customer_id,
                items=[
                    {
                        "plan": selected_membership.stripe_plan_id,
                    },
                ],
                # source=token
            )

            return redirect(reverse('memberships:update-transactions',
            kwargs={
                'subscription_id': subscription.id,
            }))
        except stripe.error.CardError as e:
            messages.info(request, 'Your card has been declined')
        except:
            messages.error(request, 'There was a problem')

    
    context = {
        'publish_key' : publish_key,
        'selected_membership' : selected_membership,
    }

    return render(request, 'memberships/membership_payment.html', context)



def update_transactions(request, subscription_id):
    
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)

    user_membership.membership = selected_membership
    user_membership.save()

    sub, created = Subscription.objects.get_or_create(user_membership=user_membership)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()

    try:
        del request.session['selected_membership_type']
    except:
        pass

    messages.info(request, "Successfully created {} membership".format(selected_membership))
    return redirect('/courses/')
