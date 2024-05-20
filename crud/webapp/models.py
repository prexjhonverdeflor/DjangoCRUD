from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone



USER_TYPE_CHOICES = [
    ('admin', 'Admin'),
    ('cashier', 'Cashier'),
]

BRANCH_TYPE_CHOICES = [
    ('head', 'Head Office'),
    ('camalig', 'Camalig Office'),
    ('daraga', 'Daraga Office'),
    ('manito', 'Manito Office'),
    ('legazpi', 'Legazpi Office'),
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)  
    branch_type = models.CharField(max_length=20, choices=BRANCH_TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.user.username 


class Record(models.Model):
    branch = models.CharField(max_length=50)
    branch_code = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=100)
    status = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.branch} - {self.branch_code}"
    

class BICSetup(models.Model):
    branch = models.CharField(max_length=50, default="Default Branch")
    branch_code = models.CharField(max_length=50, unique=True)
    bank_name = models.CharField(max_length=100)
    BRSTN = models.CharField(max_length=100)
    BIC = models.CharField(max_length=100)

    def __str__(self):
        return self.branch + " " + self.branch_code


class MCRegister(models.Model):
    creation_date = models.DateTimeField(default=timezone.now)
    branch = models.CharField(max_length=50, default="Default Branch")
    branch_name = models.CharField(max_length=50, default='')
    date_issued = models.CharField(max_length=100, default='')
    payee = models.CharField(max_length=50, default='')
    amount = models.IntegerField(default='')  
    check_number = models.CharField(max_length=100, default='')
    status = models.CharField(max_length=100, default='')
    branch_remarks = models.TextField(default='')

    def __str__(self): 
        return f"{self.branch} ({self.creation_date})"
    


class PesoNet(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    branch = models.CharField(max_length=50, default="Default Branch")
    branch_name = models.CharField(max_length=100, default='')  
    OFI_reference_num = models.IntegerField( default='')
    transact_amount = models.IntegerField( default='')
    transact_date = models.CharField(max_length=100, default='')  
    status = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"{self.branch} ({self.OFI_reference_num})"

