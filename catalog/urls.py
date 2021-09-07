from django.urls import path

from catalog.views import GoodItemListView, GoodItemCreateView, add

app_name = 'catalog'

urlpatterns = [
    path('', GoodItemListView.as_view(), name='index'),
    # path('product/add/', GoodItemCreateView.as_view(), name='product-add'),
    path('product/add', add, name='product-add'),
]

