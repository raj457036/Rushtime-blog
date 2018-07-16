from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django import forms
from django.contrib.auth.models import User

Genders = (
    ('m', 'Male'),
    ('f', 'Female'),
    ('o', 'Others')
)
class DateInput(forms.DateInput):
    input_type = 'date'

class SignupForm(UserCreationForm):
    Genders = (
    ('m', 'Male'),
    ('f', 'Female'),
    ('o', 'Others')
    )  
    name = forms.CharField(max_length=255, help_text="Enter your full name")
    gender = forms.ChoiceField(choices=Genders, help_text="Choose your gender")
    # about_me = forms.CharField(widget=forms.Textarea(attrs={'rows':'4'}),
    #              required=False,help_text="Tell us something about yourself...")
    # profile_picture = forms.ImageField(required=False, help_text="Show the world who you are.")
    date_of_birth = forms.DateField(widget=DateInput, help_text="Enter your date of birth.")

    class Meta:
        model = User
        fields = ('username','email')
        help_texts = {
            'email' : 'Enter your email address. We\'ll never share your email with anyone else.',
        }

    def clean(self):
        email = self.cleaned_data['email']
        
        if True if User.objects.filter(email=email).first() is not None else False:
            raise forms.ValidationError("Email already taken by other user.")
        return self.cleaned_data

class LoginForm(AuthenticationForm):
    username = UsernameField(max_length=255,widget=
    forms.TextInput(attrs={'class':'form-control form-control-sm'}),
    help_text='We\'ll never share your email with anyone else.')

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm'}),
    )