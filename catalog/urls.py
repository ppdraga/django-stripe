from django.urls import path

from catalog.views import GoodItemListView, GoodItemCreateView, add, bay, success, cancel, webhook

app_name = 'catalog'

urlpatterns = [
    path('', GoodItemListView.as_view(), name='index'),
    # path('product/add/', GoodItemCreateView.as_view(), name='product-add'),
    path('product/add', add, name='product-add'),
    path('product/bay', bay, name='product-bay'),
    path('success', success, name='bay-success'),
    path('cancel', cancel, name='bay-cancel'),
    path('webhook', webhook, name='webhook'),
]

