from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import View

class Signup(View):

    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('first_name')
        last_name = postData.get('last_name')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'password': password
        }
        customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)

        error_message = self.validateCustomer(customer)
        if not error_message:
            customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
            customer.password = make_password(password)
            customer.register()

            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'value': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        # validation
        error_message = None

        if not customer.first_name:
            error_message = "First Name Required..."
        elif len(customer.first_name) < 4:
            error_message = "First Name must be four character or more"
        elif not customer.last_name:
            error_message = "Last Name Required..."
        elif len(customer.last_name) < 4:
            error_message = "Last Name must be four character or more"
        elif not customer.phone:
            error_message = "Phone Number Required..."
        elif len(customer.phone) < 10:
            error_message = "Phone Number must be ten character or more"
        elif not customer.email:
            error_message = "email Required..."
        elif len(customer.email) < 10:
            error_message = "email must be ten character or more"
        elif not customer.password:
            error_message = "password Required..."
        elif len(customer.password) < 6:
            error_message = "password must be 6 character or more"
        elif customer.isExist():
            error_message = "Email address already registerd"
        return error_message