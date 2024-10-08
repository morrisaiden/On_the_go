from django.shortcuts import render
from .models import Product, Footwear, CartItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


def item_list(request):
    color = request.GET.get('color')

    if color:
        product = Product.objects.filter(color=color)
        footwears = Footwear.objects.filter(color=color)
    else:
        product = Product.objects.all()
        footwears = Footwear.objects.all()

    items = list(product) + list(footwears)

    return render(request, "item_list.html", {'items': items, 'color': color})

@login_required
def add_to_cart(request, item_type, item_id, quantity):
    user = request.user
    quantity = int(quantity)

    if item_type == 'product':
        product = get_object_or_404(Product, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(user=user, product=product, defaults={'quantity': quantity})
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

    elif item_type == 'footwear':
        footwear = get_object_or_404(Footwear, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(user=user, footwear=footwear)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

    return redirect('item_list')

@login_required
def cart_detail(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'cart_detail.html', context)

def shop_home(request):
    # Logic to display homepage
    return render(request, 'cart_detail.html')
