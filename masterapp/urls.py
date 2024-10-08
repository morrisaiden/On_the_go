from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_home, name='shop_home'),
    path('masterapp/', views.cart_detail, name='cart_detail'),
    path('add_to_cart/<str:item_type>/<int:item_id>/<int:quantity>/', views.add_to_cart, name='add_to_cart'),
]