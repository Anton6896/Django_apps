from decimal import Decimal
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Cart
from billing.models import BillingProfile, BillingAddress
from order.models import Order
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from products.models import Product
from django.contrib import messages
from billing.forms import BillingAddressForm
from users.forms import ShippingAddressForm
from users.models import Profile
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import stripe
from django.contrib.sites.models import Site

User = settings.AUTH_USER_MODEL

stripe.api_key = settings.STRIPE_SECRET_KEY


def cart_home(request):
    # in will create new cart or return cart that exists in session
    # or is user is have already a not empty cart (return in on log in)
    cart_obj = Cart.objects.get_cart(request)

    request.session["cart_total"] = cart_obj.get_amount()

    if request.is_ajax():
        json_data = {
            'amount_of_items': f'cart {cart_obj.products.count()}'
        }

        return JsonResponse(json_data)

    return render(request, 'carts/cart_home.html', {"cart": cart_obj})


def cart_update(request):
    # from product detail page will create or update the cart detail
    product_pk = request.POST['product_pk']
    product_obj = Product.objects.get(pk=product_pk)
    cart_obj = Cart.objects.get_cart(request)  # create or get my cart obj
    product_in_cart = product_obj in cart_obj.products.all()

    if product_in_cart:
        cart_obj.products.remove(product_obj)
        # messages.info(request, 'product was deleted from cart')
        product_added = False

    else:
        cart_obj.products.add(product_obj)
        # messages.success(request, 'product was added to cart')
        product_added = True

    request.session["cart_total"] = cart_obj.get_amount()

    # ajax
    if request.is_ajax():
        json_data = {
            "added": product_added,
            'amount_of_items': f'cart {cart_obj.products.count()}'
        }

        return JsonResponse(json_data)

    return redirect(product_obj.get_absolute_url())


def delete_from_cart(request):
    product_obj = Product.objects.get(pk=request.POST['product_pk'])
    cart_obj = Cart.objects.get_cart(request)
    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
        messages.info(request, 'product was deleted from cart')

    # push number of products to query session
    request.session["cart_total"] = cart_obj.products.count()
    return redirect(cart_obj.get_absolute_url())


class CheckOutView(LoginRequiredMixin, UserPassesTestMixin, generic.View):
    """
    in this point user already created and 
    user in the cart view so cart is exists !
    will (get or crete) user order and attach to it users
    (billing profile <- created with users sign up  )
    """

    # def get_success_url(self):
    #     return reverse_lazy('cart:cart_checkout')

    def __init__(self):
        super().__init__()
        self.order = None
        self.cart = None
        self.billing_profile = None
        self.billing_form = None
        self.shipping_form = None
        self.user = None

    def test_func(self):
        self.user = self.request.user
        self.cart = Cart.objects.get_cart(self.request)

        # after finish an checkout (set active->False)
        order, created = Order.objects.get_or_create(
            cart=self.cart, active=True)
        if created:
            messages.info(self.request, 'new order created ... for checkout ')
        self.billing_profile = BillingProfile.objects.get(
            user=self.request.user)

        if order:
            self.order = order
        return self.request.user == self.cart.user

    def get(self, *args, **kwarg):
        """
        # do not check for the amount of products
        # in card before transfer user to checkout
        # this was checked before in html view
        # (user cant see the checkout without products in cart)
        """

        # get form with data if exists in it (crete or update)
        self.shipping_form = ShippingAddressForm(
            instance=Profile.objects.get(user=self.user))
        addr = BillingAddress.objects.filter(
            billing_profile=self.billing_profile).first()
        if addr:
            self.billing_form = BillingAddressForm(instance=addr)
        else:
            self.billing_form = BillingAddressForm()

        context = {
            "title": "check out",
            "order": self.order,
            "end_price": format((Decimal(self.order.total) + Decimal(self.order.shipping_total)), '.2f'),
            "billing_profile": self.billing_profile,
            "billing_form": self.billing_form,
            "shipping_form": self.shipping_form,
        }

        return render(self.request, "carts/cart_checkout.html", context)

    def post(self, *args, **kwarg):
        self.shipping_form = ShippingAddressForm(self.request.POST)
        self.billing_form = BillingAddressForm(self.request.POST)

        if self.shipping_form.is_valid() and self.billing_form.is_valid():

            # user profile contains shipping address
            shipping_address = Profile.objects.get(user=self.user)
            bill_address, created = BillingAddress.objects.get_or_create(
                billing_profile=self.billing_profile)

            # create or update shipping info
            shipping_address.address_1 = self.shipping_form.cleaned_data.get(
                'address_1')
            shipping_address.city = self.shipping_form.cleaned_data.get('city')
            shipping_address.country = self.shipping_form.cleaned_data.get(
                'country')
            shipping_address.postalcode = self.shipping_form.cleaned_data.get(
                'postalcode')
            shipping_address.save()

            # get or crete billing address
            if self.shipping_form.cleaned_data.get('billing_is_shipping'):
                if created:
                    messages.success(self.request, f'billing profile created')

                bill_address.address_1_b = shipping_address.address_1
                bill_address.city_b = shipping_address.city
                bill_address.country_b = shipping_address.country
                bill_address.postcode_b = shipping_address.postalcode
                bill_address.save()

            else:
                bill_address.address_1_b = self.billing_form.cleaned_data.get(
                    'address_1_b')
                bill_address.address_2_b = self.billing_form.cleaned_data.get(
                    'address_2_b')
                bill_address.city_b = self.billing_form.cleaned_data.get(
                    'city_b')
                bill_address.country_b = self.billing_form.cleaned_data.get(
                    'country_b')
                bill_address.postcode_b = self.billing_form.cleaned_data.get(
                    'postcode_b')
                bill_address.save()

            # attach to addresses to this order
            self.order.shipping_address = shipping_address
            self.order.billing_address = bill_address
            self.order.save()

            messages.success(
                self.request, f'billing and shipping  address updated')

            return redirect("cart:payment_redirect", pk=self.order.pk)


"""
after user submit the billing form redirect ro payment at stripe app (outsourcing)
"""


class PayStripe(generic.View):

    def __init__(self):
        super(PayStripe, self).__init__()
        self.order = None
        self.end_price = None

    def get(self, request, *args, **kwargs):
        self.order = Order.objects.get(pk=self.kwargs['pk'])
        self.end_price = format((Decimal(self.order.total) + Decimal(self.order.shipping_total)), '.2f')

        shipping_address = Profile.objects.get(pk=self.order.shipping_address.pk)

        return render(request, 'carts/summary.html', {
            "order_id": self.order.order_id,
            'stripe_key': settings.STRIPE_PUB_KEY,
            'order': self.order,
            "end_price": self.end_price,
            "shipping_ad": shipping_address
        })

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])  ## <--
        cart = order.cart
        products = cart.products.all()

        items_json_list = []  # list of json data [{},{}]

        for p in products:
            items_json_list.append({
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': (int(p.price) * 100),  # in cents
                    'product_data': {
                        'name': p.title,
                        # 'images': [p.get_absolute_image_url],
                        "description": p.description
                    },
                },
                'quantity': 1,
            })

        """
        the total price is wrong due to bad calculation (for learning purpose only !! )
        """

        YOUR_DOMAIN = 'http://127.0.0.1:8000/'
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=items_json_list,
            # with meta data can identify the cart that was payed (cart id or some other identity info)
            metadata={
                "order_id": order.order_id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '',
            cancel_url=YOUR_DOMAIN + 'cart/',
        )

        return JsonResponse({
            'id': checkout_session.id
        })


"""
stripe verification server responce function 
after responce from server can clean up the users cart 

"""
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def stripe_webhook(request):
    """
     stripe listen --forward-to http://127.0.0.1:8000/cart/webhook/stripe/
    """
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_LISTENER_CODE
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        order_id = session['metadata']['order_id']
        order = Order.objects.get(order_id=order_id)
        cart = order.cart

        # change the order status
        # clear the products from cart
        order.status = 'paid'
        for item in cart.products.all():
            cart.products.remove(item)

        request.session["cart_total"] = cart.get_amount()
        order.save()
        cart.save()

    # Passed signature verification
    return HttpResponse(status=200)
