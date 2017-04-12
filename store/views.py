from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.template import RequestContext

import datetime

from .models import Cart, Product, Profile, Purchase, CartItem


class IndexView(generic.ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'


class ProductView(generic.DetailView):
    model = Product
    template_name = 'detail.html'
    context_object_name = 'product'


@login_required
def add_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    profile = request.user.profile

    ccart = profile.current_cart
    if ccart is None:
        ccart = Cart(user=profile)
        ccart.save()
        profile.current_cart = ccart
        profile.save()

    for cartitem in ccart.items.all():
        if cartitem.product == product:
            cartitem.quantity += 1
            cartitem.save()
            break
    else:
        cartitem = CartItem(product=product)
        cartitem.save()
        ccart.items.add(cartitem)
        ccart.save()

    return redirect('/c/')


@login_required
def remove_cart(request, pk):
    cartitem = get_object_or_404(CartItem, pk=pk)
    cartitem.delete()

    return redirect('/c/')


@login_required
def cart_view(request):
    template_name = 'cart.html'

    ccart = request.user.profile.current_cart

    return render(request, template_name, context={'cart': ccart})


def register(request):
    if request.POST:
        user = User(username=request.POST['email'], password=request.POST['password'], email=request.POST['email'])
        user.set_password(request.POST['password'])
        user.save()
        profile = Profile(full_name=request.POST['fullname'], address=request.POST['address'], zipcode=request.POST['zipcode'], phone=request.POST['phone'], user=user)
        profile.save()
        return redirect('/login/')
    else:
        return render(request, 'register.html')


def checkout(request):
    if request.POST:
        profile = request.user.profile

        purchase = Purchase(
            cart=profile.current_cart,
            buyer=profile,
            resolved=False,
            full_name=request.POST['full_name'],
            address=request.POST['address'],
            zipcode=request.POST['zipcode'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            cc=request.POST['cc'],
            cvv=request.POST['cvv'],
            cc_expiration_date=request.POST['cc_expiration_date']
        )
        purchase.save()

        profile.current_cart = None
        profile.save()
        return redirect('/')
    else:
        return render(request, 'checkout.html')


def orders(request):
    return render(request, 'orders.html', {'orders': Purchase.objects.filter(resolved=False)})


def order(request, pk):
    return render(request, 'order.html', {'order': get_object_or_404(Purchase, pk=pk)})


def resolve_order(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    purchase.resolved = True
    purchase.save()
    return redirect('/orders/')


def statistics(request):
    monthstart = datetime.date.today().replace(day=1)
    thismonth_orders = Purchase.objects.filter(created_date__gte=monthstart)

    return render(request, 'statistics.html', {'tmo': thismonth_orders.count()})
