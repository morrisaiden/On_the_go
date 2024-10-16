from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import Product, CartItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


def item_list(request):
    color = request.GET.get('color')

    if color:
        product = Product.objects.filter(color=color)
        # footwears = Footwear.objects.filter(color=color)
    else:
        product = Product.objects.all()
        # footwears = Footwear.objects.all()

    items = list(product)

    return render(request, "item_list.html", {'items': items, 'color': color})


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
        cart_item.quantity += 0
        cart_item.save()

        return redirect('masterapp:product_list')
    else:
        return HttpResponse('You must be logged in to add items to the cart.')


# def add_to_cart(request, item_type, item_id, quantity):
#     user = request.user
#     quantity = int(quantity)
#
# if item_type == 'product': product = get_object_or_404(Product, id=item_id) cart_item, created =
# CartItem.objects.get_or_create(user=user, product=product, defaults={'quantity': quantity}) if not created:
# cart_item.quantity += quantity cart_item.save()
#
#     elif item_type == 'footwear':
#         footwear = get_object_or_404(Footwear, id=item_id)
#         cart_item, created = CartItem.objects.get_or_create(user=user, footwear=footwear)
#         if not created:
#             cart_item.quantity += quantity
#         cart_item.save()
#
#     return redirect('item_list')


def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


# def add_footwear_to_cart(request, footwear_id):
#     # footwear = Footwear.objects.get(id=footwear_id)
#     cart_item, created = CartItem.objects.get_or_create(footwear=footwear, user=request.user)
#     cart_item.quantity += 1
#     cart_item.save()
#     return redirect('masterapp:Footwear_list')


def reset_cart(request):
    user_cart_items = CartItem.objects.filter(user=request.user)
    user_cart_items.delete()
    return HttpResponseRedirect('/cart/')


def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('masterapp:view_cart')


def shop_home(request):
    return render(request, 'cart_detail.html')


@login_required
def cart_detail(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'cart_detail.html', context)


def product_list(request):
    products = Product.objects.all()

    cart_count = CartItem.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum']
    cart_count = cart_count if cart_count else 0
    price = 0
    return render(request, 'index.html', {'products': products, 'cart_count': cart_count, 'price': price})


# def Footwear_list(request):
#     footwears = Footwear.objects.all()
#
#     # Get the count of items in the user's cart
#     cart_count = CartItem.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum']
#     cart_count = cart_count if cart_count else 0
#     return render(request, 'shoes.html', {'footwears': footwears, 'cart_count': cart_count})


# def shoes(request):
#     return render(request, 'shoes.html')


def details(request):
    return render(request, 'detail.html')


def contact(request):
    return render(request, 'contact.html')


def cart(request):
    return render(request, 'cart.html')


def cart_count(request):
    cart_count = CartItem.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum']
    cart_count = cart_count if cart_count else 0
    return JsonResponse({'cart_count': cart_count})
