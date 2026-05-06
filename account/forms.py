from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput

MAX_EMAIL_LENGTH = 254  # RFC 5321 standard


# Registration Form
class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=MAX_EMAIL_LENGTH)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Python 3 style
        # Mark email field as required
        self.fields['email'].required = True

    # Email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")

        if len(email) >= MAX_EMAIL_LENGTH:
            raise forms.ValidationError("Email is too long")
        return email


# Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))


# Update Form
class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
        exclude = ('password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark email field as required
        self.fields['email'].required = True

    # Email validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Email already exists")

        if len(email) >= MAX_EMAIL_LENGTH:
            raise forms.ValidationError("Email is too long")
        return email
