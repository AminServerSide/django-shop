from decimal import Decimal
from product.models import Product

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()

        for key, item in list(cart.items()):
            try:
                product = Product.objects.get(id=int(item['id']))
            except Product.DoesNotExist:
                # Remove invalid product entry from session
                self.cart.pop(key, None)
                self.save()
                continue

            # yield data with product instance (not stored back in session)
            yield {
                'product': product,
                'price': Decimal(item['price']),
                'quantity': int(item['quantity']),
                'total': Decimal(item['price']) * int(item['quantity']),
                'color': item['color'],
                'size': item['size'],
                'unique_id': self.unique_id_generator(product.id, item['color'], item['size'])
            }

    def unique_id_generator(self, id, color, size):
        return f'{id}-{color}-{size}'

    def remove_cart(self):
        if CART_SESSION_ID in self.session:
            del self.session[CART_SESSION_ID]
            self.save()

    def add(self, product, quantity, color, size):
        unique = self.unique_id_generator(product.id, color, size)
        if unique not in self.cart:
            self.cart[unique] = {
                'quantity': 0,
                'price': str(product.price),  # keep Decimal precision
                'color': color,
                'size': size,
                'id': str(product.id),
            }
        self.cart[unique]['quantity'] += int(quantity)
        self.save()

    def total(self):
        return sum(Decimal(item['price']) * int(item['quantity']) for item in self.cart.values())

    def remove(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    def save(self):
        self.session.modified = True
