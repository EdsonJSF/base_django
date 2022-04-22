import copy
from raffles.models import Raffle

from .forms import CartAddItemForm

class Cart:
    def __init__(self, request):
        if request.session.get('cart') is None:
            request.session['cart'] = {}

        self.cart = request.session['cart']
        self.session = request.session

    def __iter__(self):
        raffles = Raffle.objects.filter(id__in=self.cart)
        for raffle in raffles:
            self.cart[str(raffle.id)]['raffle'] = raffle

        for item in self.cart.values():
            item['total_price'] = item['quantity'] * item['price']
            item['form'] = CartAddItemForm(
                initial = {
                    'quantity': item['quantity'],
                    'override': True
                }
            )
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, raffle, quantity=1, override_quantity=False):
        raffle_id = str(raffle.id)

        if raffle_id not in self.cart:
            self.cart[raffle_id] = {
                'quantity': 0,
                'price': raffle.ticket_price
            }

        if override_quantity:
            self.cart[raffle_id]['quantity'] = quantity
        else:
            self.cart[raffle_id]['quantity'] += quantity
        self.session.modified = True

    def remove(self, raffle):
        raffle_id = str(raffle.id)

        if raffle_id in self.cart:
            del self.cart[raffle_id]
            self.save()

    def get_total_price(self):
        return sum(item["price"] * item["quantity"] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()

    def save(self):
        self.session.modified = True