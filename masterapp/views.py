from django.db.models import Sum
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Product, CartItem, Footwear
from django.contrib.auth.decorators import login_required


def product_list(request):
    products = Product.objects.all()

    cart_count = CartItem.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum']
    cart_count = cart_count if cart_count else 0
    price = 0
    return render(request, 'index.html', {'products': products, 'cart_count': cart_count, 'price': price})


def Footwear_list(request):
    footwears = Footwear.objects.all()

    # Get the count of items in the user's cart
    cart_count = CartItem.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum']
    cart_count = cart_count if cart_count else 0
    return render(request, 'shoes.html', {'footwears': footwears, 'cart_count': cart_count})


def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
        cart_item.quantity += 1
        cart_item.save()

        return redirect('masterapp:product_list')
    else:
        return HttpResponse('You must be logged in to add items to the cart.')


@login_required
def add_footwear_to_cart(request, footwear_id):
    footwear = Footwear.objects.get(id=footwear_id)
    cart_item, created = CartItem.objects.get_or_create(footwear=footwear, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('masterapp:Footwear_list')


def reset_cart(request):
    user_cart_items = CartItem.objects.filter(user=request.user)
    user_cart_items.delete()
    return HttpResponseRedirect('/cart/')


def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('masterapp:view_cart')


def shoes(request):
    return render(request, 'shoes.html')


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


def empty_cart(request):
    if 'cart' in request.session:
        request.session['cart'] = {}
        request.session.modified = True

    return redirect('your_desired_redirect_url')
