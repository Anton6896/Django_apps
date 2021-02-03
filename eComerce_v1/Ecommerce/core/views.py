from django.shortcuts import render, get_object_or_404, redirect
from . import models, forms
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import stripe
from django.conf import settings
from django.http import request
import secrets


# random ref code creator
def create_ref_code():
    # import random
    # import string
    # return ''.join(random.choices(
    #     string.ascii_lowercase + string.digits, k=20
    # ))
    return secrets.token_hex(nbytes=10)


class HomeView(generic.ListView):
    # this is the home page
    model = models.Item
    template_name = 'item_list.html'
    context_object_name = 'items'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class Checkout(LoginRequiredMixin, UserPassesTestMixin, generic.View):
    template_name = 'checkout.html'

    # security check if current user is owner of this order
    def test_func(self):
        order = models.Order.objects.get(
            user=self.request.user,
            ordered=False
        )
        return self.request.user == order.user

    def get(self, *args, **kwarg):
        # form
        form = forms.CheckoutForm()

        try:
            order = models.Order.objects.get(
                user=self.request.user,
                ordered=False
            )

            context = {
                'order': order.item.all(),
                'havecoupon': order.coupon,
                'total_price': order.get_total(),
                'title': 'checkout page',
                'form': form,
                'couponform': forms.CouponForm(),  # get new coupon code
            }

            return render(self.request, 'checkout.html', context)

        except ObjectDoesNotExist:
            messages.warning(self.request, 'have no data for this order !')
            return redirect('core:checkout')

    def post(self, *args, **kwarg):
        form = forms.CheckoutForm(self.request.POST or None)

        try:
            order = models.Order.objects.get(
                user=self.request.user,
                ordered=False
            )

            print(self.request.POST)
            if form.is_valid():
                # todo function to pay for the order
                # same_shipping_address = form.cleaned_data.get(
                #     'same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                # create billing address
                billing_address = models.Address(
                    user=self.request.user,
                    street_address=form.cleaned_data.get('street_address'),
                    apartment_address=form.cleaned_data.get(
                        'apartment_address'),
                    country=form.cleaned_data.get('country'),
                    zip=form.cleaned_data.get('zip'),
                    address_type = 'billing'
                )

                # update and save the new data
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                if payment_option == 'debit':
                    return redirect('core:payment', option='debit')
                elif payment_option == 'paypal':
                    return redirect('core:payment', option='paypal')
                else:
                    messages.warning(self.request, 'failed to checkout')
                    return redirect('core:checkout')

            messages.warning(self.request, 'failed to checkout')
            return redirect('core:checkout')

        except ObjectDoesNotExist:
            messages.warning(self.request, 'have no data for this order !')
            return redirect('core:checkout')


class PaymentView(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwarg):

        order = models.Order.objects.get(
            user=self.request.user,
            ordered=False
        )

        if order.billing_address:
            context = {
                'title': 'checkout page',
                'order': order.item.all(),
                'total_price': order.get_total(),
            }
            return render(self.request, 'payment.html', context)

        else:
            messages.warning(self.request, 'you must have billing address')
            return redirect('core:checkout')

    def post(self, *arg, **kwarg):
        try:
            order = models.Order.objects.get(
                user=self.request.user,
                ordered=False
            )
            payment = models.Payment()
            stripe.api_key = settings.STRIPE_TEST_KEY
            token = self.request.POST.get('stripeToken')
            amount = int(order.get_total() * 100)  # in cents
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
            )

            # update order and payment status
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = amount
            payment.save()

            # update all ordered item in
            order_item = order.item.all()
            order_item.update(ordered=True)
            for item in order_item:
                item.save()

            order.ordered = True
            order.payment = payment
            order.ref_code = create_ref_code()
            order.save()

            # redirect to confirm order page or some like that
            messages.success(self.request, 'order is complite , thnx ! ')
            return redirect('/')

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            print('Status is: %s' % e.http_status)
            print('Type is: %s' % e.error.type)
            print('Code is: %s' % e.error.code)
            # param is '' in this case
            print('Param is: %s' % e.error.param)
            print('Message is: %s' % e.error.message)

            # message to user
            messages.warning(self.request, f'{e.error.message}')
            return redirect('/')

        except stripe.error.RateLimitError as e:
            messages.warning(self.request, f'{e.error.message}')
            return redirect('/')

        except stripe.error.InvalidRequestError as e:
            messages.warning(self.request, f'{e.error.message}')
            return redirect('/')
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, f'{e.error.message}')
            return redirect('/')
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, f'{e.error.message}')
            return redirect('/')
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(self.request, f'{e.error.message}')
            return redirect('/')
        except Exception as e:
            # send email to my self to see the problem
            messages.warning(
                self.request, ' error for me : somthing is not right ')
            return redirect('/')


class ItemDetailView(generic.DetailView):
    model = models.Item
    template_name = 'product.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product page'
        return context


@login_required
def add_to_card(request, pk):
    item = get_object_or_404(models.Item, pk=pk)
    order_item, created = models.OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    # see incomplete order
    order_qs = models.Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # see if order item is in the order
        if order.item.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.item.add(order_item)
    else:
        # or create the new order with this item
        ordered_date = timezone.now()
        order = models.Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.item.add(order_item)

    messages.success(request, f'item addad {item}')
    return redirect('core:product', pk=pk)


@login_required
def remove_from_card(request, pk):
    item = get_object_or_404(models.Item, pk=pk)
    order_qs = models.Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        # see if order item is in the order
        if order.item.filter(item__pk=item.pk).exists():
            order_item = models.OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity == 1:
                order_item.delete()
                messages.info(request, "This item was removed from your cart.")
            else:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, " -1 from card ")

        else:
            messages.warning(request, f'no {item} here !')
            return redirect('core:product', pk=pk)

    else:
        messages.warning(request, f'order problem')
        return redirect('core:product', pk=pk)

    return redirect('core:product', pk=pk)


class OrderSummary(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwarg):

        try:
            order = models.Order.objects.get(
                user=self.request.user,
                ordered=False
            )

            context = {
                'order': order.item.all(),
                'total_price': order.get_total(),
                'title': 'summary page'
            }

            return render(self.request, 'order_summary.html', context)

        except ObjectDoesNotExist:
            messages.warning(self.request, 'have no data for this order !')
            return redirect('/')


# add and remove the items from the order summary
@login_required
def append_item_tolist(request, pk):
    item = get_object_or_404(models.Item, pk=pk)
    order_item, created = models.OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    # see incomplete order
    order_qs = models.Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # see if order item is in the order
        if order.item.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.item.add(order_item)
    else:
        # or create the new order with this item
        ordered_date = timezone.now()
        order = models.Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.item.add(order_item)

    return redirect('core:order_summary')


@login_required
def remove_item_fromlist(request, pk):
    item = get_object_or_404(models.Item, pk=pk)
    order_qs = models.Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        # see if order item is in the order
        if order.item.filter(item__pk=item.pk).exists():
            order_item = models.OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity == 1:
                order_item.delete()
            else:
                order_item.quantity -= 1
                order_item.save()
        else:
            return redirect('core:order_summary')

    else:
        return redirect('core:order_summary')

    return redirect('core:order_summary')


@login_required
def to_trash_item(request, pk):
    item = get_object_or_404(models.Item, pk=pk)
    order_qs = models.Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        # see if order item is in the order
        if order.item.filter(item__pk=item.pk).exists():
            order_item = models.OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
        else:
            return redirect('core:order_summary')

    else:
        return redirect('core:order_summary')

    return redirect('core:order_summary')

# create discount from promocode


def get_coupon(request, code):
    try:
        coupon = models.Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.warning(request, 'you have no coupon ! ')
        return redirect('core:order_summary')


class AddCouponView(generic.View):
    def post(self, *arg, **kwarg):
        form = forms.CouponForm(self.request.POST or None)

        if form.is_valid():
            try:
                order_qs = models.Order.objects.get(
                    user=self.request.user,
                    ordered=False
                )
                code = form.cleaned_data.get('code')
                coupon = get_coupon(self.request, code)

                if coupon and coupon.active:
                    order_qs.coupon = coupon
                    order_qs.save()
                    messages.success(self.request, 'coupon is activated ! ')
                    return redirect('core:checkout')

            except ObjectDoesNotExist:
                messages.warning(self.request, 'you have no order ! ')
                return redirect('core:checkout')

        messages.warning(request, 'coupon not active ! or other ? ')
        return redirect('core:checkout')


class RequestRefoundView(generic.View):
    template_name = 'refound.html'

    def get(self, *args, **kwarg):
        form = forms.RefoundForm()

        context = {
            'title': 'refound',
            'form': form
        }

        return render(self.request, 'refound.html', context)

    def post(self, *arg, **kwarg):
        form = forms.RefoundForm(self.request.POST or None)

        print(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            mail = form.cleaned_data.get('email')

            # edit the order
            try:
                order = models.Order.objects.get(ref_code=ref_code)
                order.refound_requested = True
                order.save()

                # store the refound data
                refound = models.Refound()
                refound.order = order
                refound.reason = message
                refound.mail = mail
                refound.save()

                messages.success(
                    self.request, 'refound message sent . ')
                return redirect('/')

            except ObjectDoesNotExist:
                messages.warning(
                    self.request, 'ref code is not found  ')
                return redirect('/')
