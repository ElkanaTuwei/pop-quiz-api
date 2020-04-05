from rest_framework import serializers
from core.models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs


# class TodoSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = (
#             'id',
#             'title',
#             'description',
#         )
#         model = Todo

class LenderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'account_number',
            'name',
            'interest_rate'
        )
        model = Lender


class SavingMethodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name'
        )
        model = SavingMethodType


class SavingFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',  
            'duration'
        )
        model = SavingFrequency


class SavingMethodSerializer(serializers.ModelSerializer):
    saving_type = SavingMethodTypeSerializer()
    frequency = SavingFrequencySerializer()
    class Meta:
        fields = (
            'id',
            'saving_type',
            'frequency',
            'saving_rate'
        )
        model = SavingMethod


class WalletSerializer(serializers.ModelSerializer):
    saving_method = SavingMethodSerializer()
    class Meta:
        fields = (
            'id',
            'account_balance',
            'savings_balance',
            'total_spending',
            'saving_method'
        )
        model = Wallet

class LoaneeSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()
    id = serializers.IntegerField(source="user.id")
    class Meta:
        fields = (
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'wallet')
        model = Loanee

class LoanSerializer(serializers.ModelSerializer):
    loanee = LoaneeSerializer()
    class Meta:
        fields = (
            'id',
            'reference_number',
            'amount',
            'financier',
            'interest_rate',
            'period',
            'disbursement_date',
            'loanee'
        )
        model = Loan


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs
