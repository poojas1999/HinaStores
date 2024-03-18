from django import forms
from django.contrib.auth.forms import UserCreationForm

from myapp.models import Complaint, Customer, Paymentz, Paystatus, Product, Review, User

class dateinput(forms.DateInput):
    input_type='date'
class userreg(UserCreationForm):

    username=forms.CharField()
    password1=forms.CharField(label='password',widget=forms.PasswordInput)
    password2=forms.CharField(label='password',widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','password1','password2']

class customerreg(forms.ModelForm):
    dob=forms.DateField(widget=dateinput)
    class Meta:
        model=Customer
        exclude=('user',)


class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields= "__all__"

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject','description']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Paymentz
        fields = ['amount','card_number','card_expiry','card_cvv','pname','quantity']

class RatingForm(forms.Form):
    rating = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label='Rating')


class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=['rate','comment']