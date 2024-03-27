from django import forms
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.contrib import auth,messages
from django.contrib.auth import login
from django.contrib.auth import logout
from myapp.forms import ComplaintForm, ContactForm, OrderForm, PaymentForm, ProductForm, RatingForm, ReviewForm, customerreg, userreg
from myapp.models import CartItem, Complaint, Contact, Customer, Order, Pay, Payment, Payments, Paymentss, Paymentz, Paystatus,Product, Rating, Rev, Review, Stocks, Stockz, Stockzz


stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

def home(request):
    # template = loader.get_template('index.html')
    # return HttpResponse(template.render(request))
    return render(request,'index.html')

def detail(request):
    return render(request,'about.html')

def contact(request):
    form= ContactForm(request.POST or None)
    if form.is_valid():
         form.save()
  
    context= {'form': form }
        
    return render(request, 'contact-us.html', context)


def shops(request):
    data=Product.objects.all()
    return render(request,'shop.html',{'data':data})

    
def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminindexpage')  
    return render(request, 'add_product.html', {'form': form})
            
def viewproduct(request):
    data=Product.objects.all()
    return render(request,'viewproduct.html',{'data':data})

def update_product(request,id):
    data=Product.objects.get(id=id)
    form=ProductForm(instance=data)
    if request.method=='POST':
        form=ProductForm(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
            return redirect('viewproduct')
    return render(request,'update_product.html',{'form':form})


def del_product(request,id):
    Product.objects.get(id=id).delete()
    return redirect("viewproduct")




def loginpage(request):
    if request.method=='POST':
     username=request.POST.get('uname')
     password=request.POST.get('pass')
     user=auth.authenticate(username=username,password=password)
     if user is not None and user.is_staff:
       login(request,user) 
       return redirect('adminindexpage') 
     elif user is not None and user.is_customer:
        login(request,user)
        return redirect('shops')
    else:
        messages.info(request,'You are not a registered customer')
 
    return render(request,'login.html')

def registerpage(request):
    form1=userreg()
    form2=customerreg()
    if request.method=='POST':
        form1=userreg(request.POST)
        form2=customerreg(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save(commit=False)
            user.is_customer=True
            user.save()
            customer=form2.save(commit=False)
            customer.user=user
            customer.save()
            return redirect('loginpage')    
    return render(request,'register.html',{'form1':form1,'form2':form2})

def adminndexpage(request):
    return render(request,'adminindex.html')

def add_complaint(request):
    form=ComplaintForm()
    u=request.user
    print(u)
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            obj= form.save(commit=False)
            obj.user=u
            # Accessing the Customer instance through the user attribute of the User object
            obj.save()
            return redirect('complaint_success')
    return render(request, 'add_complaint.html', {'form': form})

def complaint_success(request):
    return render(request, 'complaint_success.html')


def view_complaints(request):
    # Assuming customers are associated with users
    user_complaints = Complaint.objects.all()
    return render(request, 'view_complaint.html', {'user_complaints': user_complaints})

def pro(request,id):
    data=Product.objects.get(id=id)
    context = {
        'data':data,
        'stock_available':data.stock_available

    }
    return render(request,'productdetail.html',context)


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")

def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product,user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

def remove_from_cart(request, product_id):
    cart_item = CartItem.objects.get(id=product_id)
    cart_item.delete()
    return redirect('view_cart')


def admin_view_cart(request):
    # Retrieve all cart items from all users
    cart_items = CartItem.objects.all()
    context = {
        'cart_items': cart_items

    }
    return render(request, 'view_cart.html', context)

# def checkout(request):
#     if request.method == 'POST':
#         token = request.POST['stripeToken']
#         try:
#             charge = stripe.Charge.create(
#                 amount=1000,  # amount in cents
#                 currency='usd',
#                 description='Example charge',
#                 source=token,
#             )
#             return render(request, 'payment/success.html')
#         except stripe.error.CardError as e:
#             return render(request, 'payment/payment.html', {'error': e.error.message})
#     else:
#         return render(request, 'payment/payment.html', {'publishable_key': settings.STRIPE_PUBLISHABLE_KEY})
    

def test(request):
    return render(request, 'home.html')


def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
    

def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                       
                        'name': 'T-shirt',
                        'quantity': 1,
                        'price': 'usd',
                        'amount': '$2000',
                    
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        

def payment(request):
    if request.method=='POST':
        amount=3000
        print(amount)
        description="Sample Payment"
        try:
           payment_intent=stripe.PaymentIntent.create(
               amount=amount,
               currency='inr',
               description=description,
           )
           Pay.objects.create(amount=amount/100,description=description)
        except Exception as e:
          return redirect('payment_success')
        return render(request,'payment.html',{'client_secret': payment_intent.client_secret})
    return render(request,'payment.html')        

           
def payment_success(request):
    return render(request, 'payment_success.html')


def payment_status(request):
    customer_payments = Pay.objects.filter()
    return render(request, 'payment_status.html', {'customer_payments': customer_payments})


def cancelled(request):
    return render(request, 'cancelled.html')

def process_dummy_payment(request):
    # try:
    #     # Assuming Payment model has a field named 'customer_id' and 'status'
    #     payment = Pay.objects.get(id=id)
        
    #     # Simulate payment process (set payment status to 'Paid' for demonstration)
    #     payment.status = 'Paid'
    #     payment.save()
        
    #     return HttpResponse("Payment processed successfully.")
    # except Pay.DoesNotExist:
    #     return HttpResponse("Payment information not found for this customer.")
     return render(request, 'dummy_payment.html')

# def process_payment(request):
#     if request.method == 'POST':
#         amount = request.POST.get('amount')
#         card_number = request.POST.get('card_number')
#         card_expiry = request.POST.get('card_expiry')
#         card_cvv = request.POST.get('card_cvv')

#         # Simulate payment processing
#         # You can add actual payment processing logic here
#         Payment.objects.create(amount=amount, card_number=card_number, card_expiry=card_expiry, card_cvv=card_cvv)

#         return redirect('payment_successful') 
#     return render(request, 'payment_form.html')

def payment_successful(request):
    return render(request, 'payment_successful.html')

def process_pay(request):
    if request.method == 'POST':
        user = request.user
        amount = request.POST.get('amount')
        card_number = request.POST.get('card_number')
        card_expiry = request.POST.get('card_expiry')
        card_cvv = request.POST.get('card_cvv')
        Payment = Paymentz.objects.create(user=user,amount=amount,card_number=card_number,card_expiry=card_expiry,card_cvv=card_cvv)
        return redirect('payment_successful')
    return render(request, 'payment_form.html', {'form': forms})
        
    # form=PaymentForm()
    # u=request.user
    # print(u)
    # if request.method == 'POST':
    #     form = PaymentForm(request.POST)
    #     if form.is_valid():
    #         obj= form.save(commit=False)
    #         obj.user=u
    #         # Accessing the Customer instance through the user attribute of the User object
    #         obj.save()
    #         return redirect('payment_successful')
    # return render(request, 'payment_form.html', {'form': form})
# def process_payment(request):
#     if request.method == 'POST':
#         user = request.user
#         amount = request.POST.get('amount')
#         card_number = request.POST.get('card_number')
#         card_expiry = request.POST.get('card_expiry')
#         card_cvv = request.POST.get('card_cvv')
#         Paymentz = Paymentz.objects.create(user=user, amount=amount,card_number=card_number,card_expiry=card_expiry,card_cvv=card_cvv)
#         return redirect('payment_successful')
#     return render(request, 'payment_form.html', {'form': forms})




def view_paystatus(request):
    user_pay= Paymentz.objects.all()
    # Assuming customers are associated wit
    return render(request, 'payment_status.html', {'user_pay': user_pay})

   
# def payment_stat(request):
#     # customer = get_object_or_404(Customer, pk=customer_id)
#     # payments = Payment.objects.filter(customer=customer)
#     # return render(request, 'payment_status.html', {'customer': customer, 'payments': payments})
#     payment = Paystatus.objects.all()
#     return render(request, 'payment_status.html', {'payment': payment})

def rate(request, product_id):
    data = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            Rating.objects.create(product=data, user=request.user, rating=rating)
            # Update average rating for the product
            product_ratings = Rating.objects.filter(product=data)
            total_ratings = len(product_ratings)
            sum_ratings = sum([rating.rating for rating in product_ratings])
            data.avg_rating = sum_ratings / total_ratings
            data.save()
            return redirect('Review_rate', product_id=product_id)
    else:
        form = RatingForm()
    return render(request, 'rating.html', {'form': form, 'product': data})

def Review_rate(request,product_id):
    data = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review = form.save(commit=False)
            Review.product_id = product_id  # Assign product_id to review
            Review.save()
            return redirect('review_success')  # Redirect to a success page
    else:
        form = ReviewForm()
    return render(request, 'reviewpage.html', {'form': form})
    # product=get_object_or_404(Product,pk=id)
    # if request.method=="POST":
    #    form=ReviewForm(request.POST)
    #    if form.is_valid():
    #        Review=form.save(commit=False)
    #        Review.product=Product
    #        Review.user=request.user
    #        Review.save()
    #    return redirect('pro',product_id=id)
    # return render(request,'reviewpage.html',{'form':form,'product':id})


           
def review_success(request):
    return render(request, 'review_successful.html')

def view_reviews(request):
    datas= Review.objects.all()
    return render(request, 'view_review.html', {'datas': datas})


def reviews(request):
    datas= Review.objects.all()
    return render(request, 'view_review.html', {'datas': datas})


def view_booking(request):
    user_pay = Paymentz.objects.all()
    return render(request, 'booking.html',{'user_pay':user_pay})

def addorder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminindexpage')  
    return render(request, 'add_status.html', {'form': form})

# def custorders(request):
#     user_orders = Order.objects.filter()
#     return render(request, 'myorder.html', {'user_orders': user_orders})

def custorders(request):
    if request.method == 'POST':
        order_number = request.POST.get('order_number')
        pname = request.POST.get('pname')
       
        try:
            orders = Order.objects.get(order_number=order_number, product__pname=pname)
            status = orders.status
            return render(request, 'myorder.html', {'orders': orders, 'status': status})
        except Order.DoesNotExist:
            error_message = "Order not found for the given order number and product name."
            return render(request, 'myorder.html', {'error_message': error_message})

    return render(request, 'myorder.html')

def vieworder(request):
    orders=Order.objects.all()
    return render(request,'view_status.html',{'orders': orders})

def updateorder(request,id):
    orders=Order.objects.get(id=id)
    form=OrderForm(instance=orders)
    if request.method=='POST':
        form=OrderForm(request.POST,instance=orders)
        if form.is_valid():
            form.save()
            return redirect('vieworder')
    return render(request,'update_status.html',{'form':form})


    