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

class Show(BaseModel):
    quiz_time = models.TimeField()
    name = models.CharField(max_length=36)
    def __str__(self):
        """A string representation of the model."""
        return self.name

class Transaction(BaseModel):
    reference_number = models.UUIDField(default=uuid.uuid4, editable=False)
    amount = models.FloatField()
    sender = models.CharField(max_length=20)
    recipient = models.CharField(max_length=20)
    successful = models.BooleanField(default=False)
    time = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.recipient} | {self.amount}'
