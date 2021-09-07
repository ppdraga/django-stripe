import os

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from catalog.models import GoodItem
from catalog.forms import GoodItemForm
import stripe

stripe.api_key = os.getenv("API_KEY")

# Create your views here.

class GoodItemListView(ListView):
    model = GoodItem
    template_name = 'catalog/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return GoodItem.objects.all()

class GoodItemDetailView(DetailView):
    model = GoodItem

class GoodItemCreateView(CreateView):
    model = GoodItem
    fields = ['title', 'vendor', 'price', 'unit_of_measure']
    success_url = '/'

class GoodItemUpdateView(UpdateView):
    model = GoodItem

class GoodItemDeleteView(DeleteView):
    model = GoodItem

def add(request):
    data = dict()
    if request.method == 'POST':
        form = GoodItemForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            products = GoodItem.objects.all()
            data['products_html'] = render_to_string('catalog/list.html', {'products': products})
        else:
            data['form_html'] = render_to_string('catalog/gooditem_modal_form.html', {'form': form}, request=request)

    else:
        data['form_is_valid'] = False
        data['form_html'] = render_to_string('catalog/gooditem_modal_form.html', {'form': GoodItemForm()}, request=request)

    return JsonResponse(data)


# @csrf_exempt
def bay(request):
    HOST = "https://1c86-77-220-184-10.ngrok.io"
    m_data = {"transaction_id": "777"}

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # TODO: replace this with the `price` of the product you want to sell
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'CDN service',
                        },
                        'unit_amount': 200,
                    },
                    'quantity': 1,
                },
            ],
            payment_method_types=[
              'card',
            #   'p24',
            ],
            mode='payment',
            success_url=HOST + '/success',
            cancel_url=HOST + '/cancel',
            payment_intent_data={"metadata": m_data},
        )

    except Exception as e:
        return str(e)
    
    print(checkout_session.url)
    return redirect(checkout_session.url, status=303)
    

def success(request):
    return render(request, "catalog/success.html")


def cancel(request):
    return render(request, "catalog/cancel.html")


@csrf_exempt
def webhook(request):
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    print(endpoint_secret)
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object  # contains a stripe.PaymentIntent
        print('PaymentIntent was successful!')
    elif event.type == 'payment_method.attached':
        payment_method = event.data.object  # contains a stripe.PaymentMethod
        print('PaymentMethod was attached to a Customer!')
    # ... handle other event types
    else:
        print('Unhandled event type {}'.format(event.type))
    return HttpResponse(status=200)
