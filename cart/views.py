from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cart.forms import CartAddItemForm

from .cart import Cart
from raffles.models import Raffle

@require_POST
def cart_add(request, raffle_slug):
    cart = Cart(request)
    raffle = get_object_or_404(Raffle, slug=raffle_slug)

    form = CartAddItemForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            raffle=raffle,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )

    return redirect('cart:detail')

def cart_remove(request, raffle_slug):
    cart = Cart(request)
    raffle = get_object_or_404(Raffle, slug=raffle_slug)
    cart.remove(raffle)
    return redirect('cart:detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', { 'cart': cart })