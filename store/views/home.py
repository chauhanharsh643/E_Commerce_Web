from django.shortcuts import render, redirect
from store.models.product import Product
from store.models.category import Category
from django.views import View

# Create your views here.

class Index(View):
    def get(self, request):
        products = None

        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        # request.session.get('cart').clear()
        if categoryID:
            products = Product.get_all_products_by_category_id(categoryID)
        else:
            products = Product.get_all_products()
        data = {}
        data['products'] = products
        data['categories'] = categories
        # return render(request, 'orders/order.html')
        print('you are: ', request.session.get('email'))
        return render(request, 'index.html', data)

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')

        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    cart[product] = quantity - 1
                    if cart[product] == 0:
                        cart.pop(product)
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart

        # print('cart', request.session['cart'])

        return redirect('homepage')

