from decimal import Decimal
from django.conf import settings
from shop.models import Product


ship_and_handle_cost = 0
get_total_price_cost = 0
get_estimated_tax_cost = 0

class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        another_cart = self.cart


    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        global global_ids
        product_ids = self.cart.keys()
        global_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            print(item)
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_price(self):
        global get_total_price_cost
        total_price = 0
        for item in self.cart.values():
            total_price = total_price + item['product'].price * item['quantity']
        get_total_price_cost = total_price
        return total_price

    def estimated_tax(self):
        global get_estimated_tax_cost
        total_price = 0
        for item in self.cart.values():
            total_price = total_price + item['product'].price * item['quantity']
        get_estimated_tax_cost = (total_price/100)*7
        return (total_price/100)*7

    def total_cart_items(self):
        total_quantity = 0
        for item in self.cart.values():
            total_quantity = total_quantity + item['quantity']
        return total_quantity

    def ship_and_handle(self):
        global ship_and_handle_cost
        total_price = 0
        for item in self.cart.values():
            total_price = total_price + item['product'].price * item['quantity']
        ship_and_handle_cost = (total_price/100)*2
        return (total_price/100)*2

    def total_before_tax(self):
        global get_total_price_cost, ship_and_handle_cost
        return get_total_price_cost + ship_and_handle_cost

    def final_price(self):
        global get_total_price_cost, ship_and_handle_cost, get_estimated_tax_cost
        return float(get_total_price_cost) + float(ship_and_handle_cost) + float(get_estimated_tax_cost)
