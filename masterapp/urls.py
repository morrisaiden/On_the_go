from django.conf.urls.static import static
from django.urls import path

from On_the_go import settings
from . import views

app_name = 'masterapp' #name space

urlpatterns = [
    # path('', views.shop_home, name='shop_home'),
    # path('items', views.item_list, name='item_list'),
    # path('masterapp/', views.cart_detail, name='cart_detail'),
    # path('add_to_cart/<str:item_type>/<int:item_id>/<int:quantity>/', views.add_to_cart, name='add_to_cart'),
    # path('add_to_cart/<str:item_type>/<int:item_id>/<int:quantity>/', views.add_to_cart, name='add_to_cart'),

    path('', views.product_list, name='product_list'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart_count/', views.cart_count, name='cart_count'),
    path('details/', views.details, name='details'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    # path('Shoes/', views.Footwear_list, name='Footwear_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)