from django.contrib.auth.forms import UserCreationForm
from .models import User, Products
from django.forms import ModelForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
class ProductsForm(ModelForm):
     class Meta:
        model = Products
        fields = '__all__'

class UserForm(ModelForm):
     class Meta:
         model = User
         fields = ['avatar', 'username', 'email', 'bio', 'products_user']

