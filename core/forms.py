from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, BusinessProfile

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )


class BusinessProfileForm(forms.ModelForm):
    # User fields (from CustomUser model)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    
    # Business Profile fields
    business_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your business name'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describe your business, services, and what makes you unique...'
        })
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your business address or location'
        })
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your contact phone number'
        })
    )
    timing = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 9:00 AM - 8:00 PM'
        })
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = BusinessProfile
        fields = ['business_name', 'description', 'location', 'phone', 'timing', 'image']
    
    def clean_email(self):
        """Custom validation for email field"""
        email = self.cleaned_data.get('email')
        if email:
            # Check if email is already taken by another user
            user = getattr(self, 'user', None)
            if user and CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
                raise forms.ValidationError("This email is already registered by another user.")
        return email
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Store user for validation
            self.user = user
            # Set initial value for email field
            self.fields['email'].initial = user.email
            # Set the widget value attribute for proper rendering
            self.fields['email'].widget.attrs['value'] = user.email
