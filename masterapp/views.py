from django.db.models import Sum
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import Product, Footwear, CartItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


def item_list(request):
    color = request.GET.get('color')

    if color:
        product = Product.objects.filter(color=color)
        footwears = Footwear.objects.filter(color=color)
    else:
        product = Product.objects.all()
        footwears = Footwear.objects.all()

    items = list(product) + list(footwears)

    cart_count = CartItem.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum']
    cart_count = cart_count if cart_count else 0

    price=0

    return render(request, "item_list.html", {
        'items': items,
        'color': color,
        'cart_count': cart_count,
        'price': price
    })


@login_required
def add_to_cart(request, item_type, item_id, quantity):
    user = request.user

    if request.method == 'POST':
        # Get the quantity from the form (POST data)
        quantity = int(request.POST.get('quantity', quantity))

        if item_type == 'product':
            product = get_object_or_404(Product, id=item_id)
            cart_item, created = CartItem.objects.get_or_create(
                user=user,
                product=product,
                footwear=None,
                defaults={'quantity': quantity, 'price': product.price}
            )
            if not created:
                cart_item.quantity += quantity
            cart_item.save()

            print(f"Added {quantity} of {product.name} to {user.username}'s cart")

        elif item_type == 'footwear':
            footwear = get_object_or_404(Footwear, id=item_id)
            cart_item, created = CartItem.objects.get_or_create(
                user=user,
                footwear=footwear,
                product=None,
                defaults={'quantity': quantity, 'price': footwear.price}
            )

            if not created:
                cart_item.quantity += quantity
            cart_item.save()

            print(f"Added {quantity} of {footwear.name} to {user.username}'s cart")

        return redirect('item_list')


@login_required
def cart_detail(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

#Debugging: Print cart items to check if they are being fetched correctly

    for item in cart_items:
        print(f"{item.product or item.footwear} - Quantity: {item.quantity}")

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'cart_detail.html', context)


def shop_home(request):
    # Logic to display homepage
    return render(request, 'cart_detail.html')


def members(request):
    return HttpResponse("Hello, world. You're at the shop_home view.")
