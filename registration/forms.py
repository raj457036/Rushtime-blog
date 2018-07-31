from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django import forms
from django.contrib.auth.models import User

Genders = (
    ('m', 'Male'),
    ('f', 'Female'),
)
class DateInput(forms.DateInput):
    input_type = 'date'

class SignupForm(UserCreationForm): 
    name = forms.CharField(max_length=255, help_text="Enter your full name")
    gender = forms.ChoiceField(choices=Genders, help_text="Choose your gender")
    about_me = forms.CharField(widget=forms.Textarea(attrs={'rows':'4','placeholder':"Tell us something about yourself..."}),
                 required=False)
    display_img = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class':'input_img','accept':'.jpg,.jpeg,.png,.gif'}))
    date_of_birth = forms.DateField(widget=DateInput)
    avatar_number = forms.CharField(max_length=2, required=False, widget=forms.NumberInput(attrs={'class':''}))
    class Meta:
        model = User
        fields = ('username','email')
        help_texts = {
            'email' : 'Enter your email address. We\'ll never share your email with anyone else.',
            'password':'Your password must contain at least 8 characters.'
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

    remember_me = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input ml-2'}),
                                    help_text='Remember me for 7 days')
