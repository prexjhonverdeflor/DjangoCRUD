from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from .models import Record, BICSetup, MCRegister, PesoNet

from django import forms

from django.forms.widgets import PasswordInput, TextInput, DateInput, Textarea
from django.contrib.auth.forms import AuthenticationForm



BRANCH_TYPE_CHOICES = [
    ('head', 'Head Office'),
    ('camalig', 'Camalig Office'),
    ('daraga', 'Daraga Office'),
    ('manito', 'Manito Office'),
    ('legazpi', 'Legazpi Office'),
]

USER_TYPE_CHOICES = [
    ('admin', 'Admin'),
    ('cashier', 'Cashier'),
]

# Custom form for creating a new user with additional fields for user type and branch type
class CreateUserForm(UserCreationForm):
    # User type is a required field with radio button selection
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES, 
        required=True, 
        widget=forms.RadioSelect
    )

    # Branch type is a required field with a simple dropdown (select) menu
    branch_type = forms.ChoiceField(
        choices=BRANCH_TYPE_CHOICES, 
        required=True
    )

    # Meta class defines the associated model and the form fields
    class Meta:
        model = User  # Using Django's built-in User model
        fields = ['username', 'password1', 'password2', 'user_type', 'branch_type']




class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


#create record
class CreateRecordForm(forms.ModelForm):

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, label='Status')

    class Meta:
        model = Record
        fields = ['branch_code', 'branch_name', 'status']





#update record
class UpdateRecordForm(forms.ModelForm):

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, label='Status')

    class Meta:
        model = Record
        fields = ['branch_code','branch_name', 'status']


#BIC SETUP
class BICSetupForm(forms.ModelForm):
    class Meta:
        model = BICSetup
        fields = ['branch_code', 'bank_name', 'BRSTN', 'BIC'] 



#CASHIER
class MCRegisterForm(forms.ModelForm):

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, label='Status', required=True)

    class Meta:
        model = MCRegister
        fields = ['branch_name', 'date_issued', 'payee', 'amount', 'check_number', 'status', 'branch_remarks']
        
        widgets = {
            'date_issued': DateInput(attrs={'type': 'date'}),
            'branch_remarks': Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        

#PESOT
class PesoNetForm(forms.ModelForm):

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, label='Status', required=True)

    class Meta:
        model = PesoNet
        fields = ['branch_name', 'OFI_reference_num', 'transact_amount', 'transact_date', 'status']
        
        widgets = {
            'transact_date': DateInput(attrs={'type': 'date'}),
        }


    