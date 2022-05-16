from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (
    ItemDetailView,

    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,

 
)

app_name = 'product_catalog_app'

urlpatterns = [
    path('login/', views.login_form, name='login_form'),
    path('waitingPage/',views.waitingPage,name="waitingPage"),
    path('products/', views.HomeView, name='products'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
     name='remove-single-item-from-cart'),
    path('',views.index,name = 'index'),
    path('<slug:category_slug>', views.HomeView, name='product_by_category'),
    path('', views.contact, name="contact"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

