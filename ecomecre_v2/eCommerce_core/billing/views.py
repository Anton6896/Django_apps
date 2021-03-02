from django.shortcuts import render
from django.views.generic import View
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_PUB_KEY = settings.STRIPE_PUB_KEY


# payment stripe view
def payment_view(request):
    if request.method == "POST":
        print(request.POST)

    return render(request, "billing/payment.html", {
        "title": "Payment",
        "publish_key": STRIPE_PUB_KEY,

    })

# class PaymentView(View):
#     def post(self, request, *args, **kwargs):
#         card_num = request.POST['card_num']
#         exp_month = request.POST['exp_month']
#         exp_year = request.POST['exp_year']
#         cvc = request.POST['cvc']
#
#         token = stripe.Token.create(
#             card={
#                 "number": card_num,
#                 "exp_month": int(exp_month),
#                 "exp_year": int(exp_year),
#                 "cvc": cvc
#             },
#         )
#
#         charge = stripe.Charge.create(
#             amount=2000,
#             currency="usd",
#             source=token,  # obtained above
#             # source="tok_visa", # obtained with Stripe.js (JS)
#             description="Charge for jenny.rosen@example.com"
#         )
#
#         if charge['captured'] == True:
#             Sale.objects.create(product=product, amount=amount)
#             return redirect('app:success_page')
#
#         return redirect('app:fail_page')

