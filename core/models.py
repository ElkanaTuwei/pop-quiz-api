import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token


#token creation
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Lender(BaseModel):
    account_number = models.IntegerField()
    name = models.CharField(max_length=36)
    interest_rate = models.FloatField(default=1)
    def __str__(self):
        """A string representation of the model."""
        return self.name


class SavingMethodType(BaseModel):
    name = models.CharField(max_length=20)
    def __str__(self):
        """A string representation of the model."""
        return self.name

class SavingFrequency(BaseModel):
    name = models.CharField(max_length=20)
    duration = models.FloatField(default=1)
    def __str__(self):
        """A string representation of the model."""
        return self.name


class SavingMethod(BaseModel):
    saving_type = models.ForeignKey(SavingMethodType, on_delete=models.CASCADE)
    saving_rate = models.FloatField(default=1)
    frequency = models.ForeignKey(SavingFrequency, on_delete=models.CASCADE)

    def __str__(self):
        """A string representation of the model."""
        return  f'{self.saving_rate} - {self.saving_type.name}'


class Wallet(BaseModel):
    account_balance = models.FloatField(default=0)
    savings_balance = models.FloatField(default=0)
    total_spending = models.FloatField(default=0)
    saving_method = models.ForeignKey(SavingMethod, on_delete=models.CASCADE, null=True, blank=True)
   
    def to_json(self):
        return{
            'id':self.id,
            'account_balance':self.account_balance,
            'nasavings_balanceme': self.savings_balance,
            'total_spending':self.total_spending,
            'saving_method':self.saving_method.id,
        }

    def __str__(self):
        """A string representation of the model."""
        return f'{self.id} - {self.account_balance}'



class Loanee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    # @receiver(post_save, sender=User)
    # def create_user_loanee(sender, instance, created, **kwargs):
    #     if created:
    #         Loanee.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_loanee(sender, instance, **kwargs):
    #     instance.loanee.save()
        
    def to_json(self):
        return{
            'id':self.user.id,
            'first_name':self.first_name,
            'name': self.name,
            'last_name':self.last_name,
            'phone_number':self.phone_number,
            'email':self.email,
            'user':self.user.id,
            'wallet':self.wallet.id,
        }

    def __str__(self):
        return f'{self.first_name}  {self.last_name}'

    class Meta:
        db_table = "Loanee"


class Loan(BaseModel):
    reference_number = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField()
    financier = models.ForeignKey(Lender, on_delete=models.CASCADE)
    interest_rate = models.FloatField(default=1)
    period = models.FloatField(default=1)
    disbursement_date = models.DateField()
    loanee = models.ForeignKey(Loanee, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.loanee.phone_number} | {self.amount} | {self.financier}'



class Outbox(BaseModel):
    outbox_id = models.UUIDField(auto_created=True, default=uuid.uuid4, primary_key=True, editable=False)
    recipient = models.CharField(max_length=20)
    message = models.TextField()
    message_type = models.CharField(max_length=20)
    msg_content_id = models.CharField(max_length=50)
    sent = models.BooleanField(default=False)
    sent_time = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    delivered_time = models.DateTimeField(null=True)
    ait_delivery_status = models.CharField(max_length=10,null=True)
    ait_failure_reason = models.CharField(max_length=10,null=True)
    ait_message_id = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.recipient + '| ' + self.message


class Transaction(BaseModel):
    reference_number = models.UUIDField(default=uuid.uuid4, editable=False)
    amount = models.FloatField()
    sender = models.CharField(max_length=20)
    recipient = models.CharField(max_length=20)
    successful = models.BooleanField(default=False)
    time = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.recipient} | {self.amount}'

class PhoneOtp(BaseModel):
    otp_code = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    count = models.IntegerField(default=1)
    validated = models.BooleanField(default=False)

    def to_json(self):
        return{
            'otp_code':self.user.first_name,
            'phone_number':self.phone_number,
        }

    def __str__(self):
        return f'{self.phone_number}  {self.otp_code}'

    class Meta:
        db_table = "PhoneOtp"