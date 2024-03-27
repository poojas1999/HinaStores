from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='Customer')
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    gender=models.CharField(max_length=100)
    dob=models.DateField()
    email=models.EmailField()
    contact_no=models.IntegerField()

    def __str__(self):
        return self.name
    
class Product(models.Model):
    image1=models.ImageField(upload_to='images1')
    image2=models.ImageField(upload_to='images2')
    image3=models.ImageField(upload_to='images3')
    pname=models.CharField(max_length=200)
    price=models.IntegerField()
    sub=models.TextField()
    desc=models.TextField()
    stock_available = models.IntegerField(default=0)
    

    def __str__(self):
        return self.pname
    

class stock_avay(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
         return f'{self.quantity} x {self.product.pname}'
    


class Complaint(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class CartItem(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f'{self.quantity} x {self.product.pname}'
    

class Pay(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)



class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_number = models.CharField(max_length=16)
    card_expiry = models.CharField(max_length=5)
    card_cvv = models.CharField(max_length=4)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of ${self.amount} made at {self.timestamp}"
    
class Payments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_number = models.CharField(max_length=16)
    card_expiry = models.CharField(max_length=5)
    card_cvv = models.CharField(max_length=4)
    timestamp = models.DateTimeField(auto_now_add=True)
   


    def __str__(self):
        return f"Payment of ${self.amount} made at {self.timestamp}"
    
class Paymentz(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_number = models.CharField(max_length=16)
    card_expiry = models.CharField(max_length=5)
    card_cvv = models.CharField(max_length=4)
    timestamp = models.DateTimeField(auto_now_add=True)
    product= models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True)
    cart = models.ForeignKey(CartItem, on_delete=models.CASCADE,null=True, blank=True)


    def __str__(self):
        return f"Payment of ${self.amount} made at {self.timestamp}"
    
class Paymentss(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_number = models.CharField(max_length=16)
    card_expiry = models.CharField(max_length=5)
    card_cvv = models.CharField(max_length=4)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of ${self.amount} made at {self.timestamp}"

class Paystatus(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    status_choices = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )
    status = models.CharField(max_length=20, choices=status_choices, default='PENDING')   


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()




class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    comment=models.TextField(default=0)
    rate=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.id
    

class Rev(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    comment=models.TextField(default=3)
    rate=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)


class Stocks(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True)
    quantity = models.ForeignKey(CartItem, on_delete=models.CASCADE,null=True, blank=True)

class Stockz(models.Model):
    pname=models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('In Stock', 'In Stock'), ('Out of Stock', 'Out of Stock')])

    def __str__(self):
        return self.pname
    

class Stockzz(models.Model):
    names = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[('In Stock', 'In Stock'), ('Out of Stock', 'Out of Stock')])

    def __str__(self):
        return self.names

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    order_number=models.IntegerField()

class Contact(models.Model):
    nam=models.CharField(max_length=100)
    mailid=models.EmailField() 
    subject=models.CharField(max_length=100)
    msg=models.CharField(max_length=100)
    
