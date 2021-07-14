from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from .models import Customer, Product, Cart, OrederPlaced
from django.db.models import Q
from .forms import RegistrationForm, CustomerProfileForm
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='MP')
        laptops = Product.objects.filter(category='LT')
        return render(request, 'bezo/home.html', {'topwears':topwears,
         'bottom_wears':bottomwears, 'mobiles':mobiles, 'laptops':laptops})

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        item_already_in_cart = Cart.objects.filter(Q(product=product.id)& Q(user=request.user)).exists()
        return render(request, 'bezo/productdetail.html', {'product_details':product, 'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
def cartshow(request):
    if request.user.is_authenticated:
        user = request.user
        carts = Cart.objects.filter(user=user)
        shipping_price = 70.0
        total_amount = 0.0
        amount = 0.0
        total_cart_products = [p for p in Cart.objects.all() if p.user == user]
        if total_cart_products:
            for i in total_cart_products:
                temp_amount = (i.quantity * i.product.discount_price)
                amount += temp_amount
                total_amount = amount + shipping_price
                print(total_amount)
                
            return render(request, 'bezo/addtocart.html',  {'carts':carts, 'temp_amount':temp_amount, 
            'amount':amount, 'total_amount':total_amount})
        
        else:
            return render(request, 'bezo/emptycart.html')

    else:
        return redirect('/login/')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_price = 70.0
        cart_product= [p for p in Cart.objects.all() if p.user==request.user]
        
        for i in cart_product:
            temp_amount = (i.quantity * i.product.discount_price)
            amount += temp_amount

            data={
                'quantity':c.quantity,
                'amount':amount,
                'total_amount':amount + shipping_price
            }
            return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_price = 70.0
        cart_product= [p for p in Cart.objects.all() if p.user==request.user]
        
        for i in cart_product:
            temp_amount = (i.quantity * i.product.discount_price)
            amount += temp_amount

            data={
                'quantity':c.quantity,
                'amount':amount,
                'total_amount':amount + shipping_price
            }
            return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_price = 70.0
        cart_product= [p for p in Cart.objects.all() if p.user==request.user]
        for i in cart_product:
            temp_amount = (i.quantity * i.product.discount_price)
            amount += temp_amount

            data={
                'amount':amount,
                'total_amount':amount + shipping_price,
            }
            return JsonResponse(data)
    
 

def buy_now(request):
    return render(request, 'bezo/buynow.html')


@login_required
def orders(request):
    op = OrederPlaced.objects.filter(user=request.user)
    return render(request, 'bezo/orders.html', {'order_placed':op})

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'bezo/address.html',{'add':add, 'active':'btn-primary'})


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrederPlaced(user=user, customer=customer, product = c.product,
        quantity = c.quantity).save()
        c.delete()
    return redirect('orders')    
    

def mobile(request, data=None ):
    if data == None:
        mobiles = Product.objects.filter(category='MP')
    elif data == 'mi' or data == 'samsung':    
        mobiles = Product.objects.filter(category='MP').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='MP').filter(discount_price__lt=15000)
    elif data == 'above':
       mobiles = Product.objects.filter(category='MP').filter(discount_price__gt=15000)    
    return render(request, 'bezo/mobile.html', {'mobiles':mobiles})

def laptop(request, data=None ):
    if data == None:
        laptops = Product.objects.filter(category='LT')

    elif data == 'lenovo' or data == 'dell' or data == 'hp': 
        laptops = Product.objects.filter(category='LT').filter(brand=data)

    elif data == 'below':
        laptops = Product.objects.filter(category='LT').filter(discount_price__lt=35000)

    elif data == 'above':
        laptops = Product.objects.filter(category='LT').filter(discount_price__gt=35000)  
    return render(request, 'bezo/laptops.html', {'laptops':laptops})

def bottom(request):
    bottoms = Product.objects.filter(category='BW')
    return render(request, 'bezo/bottom.html', {'bottoms':bottoms})

def tops(request):
    tops = Product.objects.filter(category='TW')
    return render(request, 'bezo/tops.html', {'tops':tops})    


class CustomerRegistration(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'bezo/customerregistration.html', {'form':form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratualations!! Registered successfully')
            form.save()    
        return render(request, 'bezo/customerregistration.html', {'form':form})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_item = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_price = 70.0
    cart_product= [p for p in Cart.objects.all() if p.user==request.user]
    for i in cart_product:
        temp_amount = (i.quantity * i.product.discount_price)
        amount += temp_amount
        total_amount = amount + shipping_price

    return render(request, 'bezo/checkout.html', {'add':add, 'total_amount':total_amount, 'cart_item':cart_item})

@method_decorator(login_required, name='dispatch')
class CustomerProfile(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'bezo/profile.html', {'form':form, 'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        usr = request.user
        if form.is_valid():
            nme = form.cleaned_data['name']
            local = form.cleaned_data['locality']
            cty = form.cleaned_data['city']
            zcode = form.cleaned_data['zipcode']
            stte = form.cleaned_data['state']
            data = Customer(user=usr,name=nme,locality=local,city=cty,zipcode=zcode,state=stte)
            data.save()
            messages.success(request, 'Address saved successfully')
        form = CustomerProfileForm()    
        return render(request, 'bezo/profile.html', {'form':form, 'active':'btn-primary'})    

def search_view(request):
    pass
    # if request.method == 'POST':
    #     data = request.POST['search']
    #     if data != None:
    #         match = Product.objects.filter(Q(title__icontains=data))
    #     else:
    #         return HttpResponseRedirect('/')    
    #     return render(request, 'bezo/search.html', {'match':match})
    # else:
    #     return HttpResponseRedirect('/')       