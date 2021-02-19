import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.views import View
from django.conf import settings
from django.views.generic import TemplateView
from .models import Product
import stripe
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET


class SuccessView(TemplateView):
    template_name = 'products/success.html'


class CancelView(TemplateView):
    template_name = 'products/cancel.html'


class IndexView(View):
    def get(self, *args, **kwargs):
        p = Product.objects.all()

        return render(self.request, 'products/index.html', {
            'products': p,
            'stripe_key': settings.STRIPE_PUB,
        })


class CheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        """
        example use an all products from some hypothetic cart
        conbine all price in one and add cart_id for purchase  
        (for me is better than a costume methos but costume have more functionality  )
        """

        products = Product.objects.all()

        items_json_list = []
        YOUR_DOMAIN = 'http://127.0.0.1:8000/'

        for p in products:
            items_json_list.append({
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': p.price,  # in cents
                    'product_data': {
                        'name': str(p.name),
                        # 'images': [prod.image.url],
                    },
                },
                'quantity': 1,
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=items_json_list,
            # with meta data can identify the cart that was payed (cart id or some other identity info)
            metadata={
                "cart_id": 1
            },
            mode='payment',
            success_url=YOUR_DOMAIN + 'success/',
            cancel_url=YOUR_DOMAIN + '',
        )

        return JsonResponse({
            'id': checkout_session.id
        })


@csrf_exempt
def stripe_webhook(request):
    """
    check if your stripe is accepting the data (transaction complied )
    must have stripe cli installed
     stripe listen --forward-to localhost:8000/webhook/stripe/
     Your webhook signing secret is whsec_Fzg5Nt0vQ3BoCdq8zq8o8XylrATujJdb
    """
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # * get an end responce from stripe that operation is ok
        # * and do some action after transaction
        email = session['customer_details']['email']
        cart_id = session['metadata']['cart_id']
        print(f"costumer email : {email}")
        print(f"cart_id : {cart_id}")

        send_mail(
            subject=f"Transaction completed for cart {cart_id}",
            message="message about this transaction ",
            recipient_list=[email],
            from_email='site@mail.com'
        )

    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        print(intent)

    # Passed signature verification
    return HttpResponse(status=200)


class StripeIntentView(View):
    """
    costume payment a PaymentIntent
    grub an email from form -> adjust to stripe user ,
    cart pushed manually (for test data )
    """

    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            print(req_json)
            costumer = stripe.Customer.create(email=req_json['email'])
            products = Product.objects.all()
            amount = 0
            for pro in products:
                amount += pro.price  # simulate cart amount

            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                customer=costumer['id'],
                metadata={
                    "cart_id": 11
                }
            )

            return JsonResponse({
                'clientSecret': intent['client_secret']
            })

        except Exception as e:
            return JsonResponse({"error": str(e)})
