from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  # If not required, put required = False.

    # Within meta class, I am going to specify the model that this form is going to interact with i.e. User model.
    # Bcz whenever this form validates, it's going to create new user.
    # This Meta class gives us a nested namespace for configurations and keeps the configurations in one place.
    # Here I'm telling that the User model is going to be affected, for example when we save, or the fields that this
    # form contains and its order.
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']          # This image we have defined in Profile model.
