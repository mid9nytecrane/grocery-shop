from core.models import Product
from .models import MyCart, CartItem

from django.contrib.auth.models import User 



class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        self.user = request.user 
        
        # get current session key
        cart = self.session.get('session_key')

        #if user is new, no session key, create one
        if "session_key" not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

        # if user is authenticated, sync session cart with database
        if self.user.is_authenticated:
            self.sync_with_database()

    
    def sync_with_database(self):
        """Sync session cart with database cart"""
        try:
            db_cart, created = MyCart.objects.get_or_create(user=self.user)
            
            # Add session items to database
            for product_id, quantity in self.cart.items():
                try:
                    product_id_int = int(product_id)
                    cart_item, created = CartItem.objects.get_or_create(
                        cart=db_cart,
                        product_id=product_id_int,
                        defaults={'quantity': quantity}
                    )
                    if not created:
                        # Update quantity if item already exists
                      
                        cart_item.quantity = quantity
                        cart_item.save()
                except (ValueError, Product.DoesNotExist):
                    continue
            
            # Clear session cart after syncing
            # self.cart = {}
            # self.session['session_key'] = {}
            #self.session.modified = True
            
        except Exception as e:
            print(f"Error syncing cart: {e}")


       

    def add(self, product,quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        
         #logic

        # if user is authenticated
        if self.user.is_authenticated:
            try:
                db_cart, created = MyCart.objects.get_or_create(user=self.user)
                cart_item, created = CartItem.objects.get_or_create(
                    cart=db_cart,
                    product=product,
                    defaults={'quantity': quantity}
                )

                if not created:
                    cart_item.quantity = product_qty
                    cart_item.save()

            except Exception as e:
                print(f"Error adding to cart database: {e}")
        else:
            if product_id in self.cart:
                pass
            else:
                # self.cart[product_id] = {'price':str(product_id)}
                self.cart[product_id] = int(product_qty)
                
                self.session.modified = True 

    #legth or get total number items in a cart
    def __len__(self):
        if self.user.is_authenticated:
            try:
                db_cart = MyCart.objects.get(user=self.user)
                return db_cart.items.count()
            except MyCart.DoesNotExist:
                return 0
        else:
            return len(self.cart)
    

    def __iter__(self):
        """
        Iterate over cart items and add subtotal to each.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            qty = self.cart[str(product.id)]
            subtotal = product.price * qty
            yield {
                'product': product,
                'qty': qty,
                'subtotal': subtotal,
            }

    

    def product_subtotal(self):
        if self.user.is_authenticated:
            try:
                db_cart = MyCart.objects.get(user=self.user)
                return {str(item.product.id): item.subtotal for item in db_cart.items.all()}
            except MyCart.DoesNotExist:
                return {}
            
        else:

            product_subtotals = {}
            for key,value in self.cart.items():
                try:
                    product_id = key
                    qty = value
                    product_id = int(product_id)
                    product = Product.objects.get(id=product_id)
                    product_subtotals[str(product_id)] = (product.price * qty)
                except (Product.DoesNotExist, ValueError):
                    product_subtotals[str(product_id)] = 0

            return product_subtotals





    def cart_total(self):
        #getting product ids from cart(dictionary)
        # product_ids = self.cart.keys()
        # quantities = self.cart 

        # #look up products in DB 
        # products = Product.objects.filter(id__in=product_ids)
        
        # total = 0

        # for key,value in quantities.items():
        #     key = int(key)
        #     for product in products:
        #         if product.id == key:
        #             total = total +  (product.price * value)
        # return total 

        subtotals = self.product_subtotal()
        return sum(subtotals.values())
    

    def get_prods(self):

        """Get products in cart"""
        if self.user.is_authenticated:
            try:
                db_cart = MyCart.objects.get(user=self.user)
                return [item.product for item in db_cart.items.all()]
            except MyCart.DoesNotExist:
                return []
        else:
            #get ids from cart
            product_ids = self.cart.keys()
            
            #use ids to lookup products in product DB model
            products = Product.objects.filter(id__in=product_ids)

            return products
    

    def get_quants(self):
        # get quantities in cart when user is authenticated
        if self.user.is_authenticated:
            try:
                db_cart = MyCart.objects.get(user=self.user)
                return {str(item.product.id): item.quantity for item in db_cart.items.all()}
            except MyCart.DoesNotExist:
                return {}

        else:
            quantities = self.cart 
            return quantities


    def update(self, product, quantity):
        """ update product quantity"""
        product_id = str(product)
        product_qty = int(quantity)

        if self.user.is_authenticated:
            try:
                db_cart = MyCart.objects.get(user=self.user)
                cart_item = CartItem.objects.get(cart=db_cart, product=product)
                cart_item.quantity = quantity
                cart_item.save()
            except (MyCart.DoesNotExist, CartItem.DoesNotExist):
                pass 
        else:
            updatecart = self.cart
            updatecart[product_id] = product_qty

            self.session.modified = True

            thing = self.cart
            return thing


    def delete(self,product):
        product_id = str(product)
        if self.user.is_authenticated:
            try:
                db_cart = MyCart.objects.get(user=self.user)
                CartItem.objects.filter(cart=db_cart, product=product).delete()
            except MyCart.DoesNotExist:
                pass 

        else:
            if product_id in self.cart:
                del self.cart[product_id]
            
            self.session.modified = True 


