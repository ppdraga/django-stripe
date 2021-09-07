from django.shortcuts import render
from django.http import JsonResponse
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
