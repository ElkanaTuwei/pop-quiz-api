import random
import time
from datetime import datetime
from django.core import serializers
import json

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from rest_framework import viewsets, permissions, parsers, renderers
from django.contrib.auth.models import User,Group

from core.models import *

from .serializers import *
from api.tasks import *


class PhoneRegistrationView(APIView):
    def post(self, request):
        request_data = request.data
        print(request_data)
        phone_number = request_data['phone_number']
        code = random.randint(100000, 999999)
        saved_otp = PhoneOtp.objects.filter(phone_number__iexact=phone_number)
        try:
            loanee = Loanee.objects.get(phone_number=phone_number)
        except ObjectDoesNotExist:
            loanee = None
        if saved_otp.exists():
            saved_otp = saved_otp.first()
            if saved_otp.validated and loanee:
                resp = {
                    'phone_validated': True,
                    'message': 'phone number already validated'
                }
                return Response(resp) 
            else:
                send_registration_sms(phone_number, code, saved_otp.id)
                saved_otp.otp_code = code
                saved_otp.count += 1
                saved_otp.save()
                resp = {
                    'phone_validated': False,
                    'otp_code': code,
                    'phone_number': phone_number
                }
                return Response(resp)
        else:
            phone_otp = PhoneOtp(phone_number=phone_number, otp_code=code)
            phone_otp.save()
            send_registration_sms(phone_number, code, phone_otp.id)
            resp = {}
            resp['data'] = {
                'phone_validated': False,
                'otp_code': code,
                'phone_number': phone_number
            }
            return Response(resp)


    def get(self, request):
        pass

class ResendCodeView(APIView):
    def post(self, request):
        request_data = request.data
        print(request_data)
        phone_number = request_data['phone_number']
        code = random.randint(100000, 999999)
        saved_otp = PhoneOtp.objects.filter(phone_number__iexact=phone_number)
        if saved_otp.exists():
            saved_otp = saved_otp.first()
            send_registration_sms(phone_number, code, saved_otp.id)
            saved_otp.count += 1
            saved_otp.otp_code = code
            saved_otp.save() 
            resp = {
                'status': True,
                'otp_code': code,
                'phone_number': phone_number
            }
            return Response(resp)
        else:
            phone_otp = PhoneOtp(phone_number=phone_number, otp_code=code)
            phone_otp.save()
            send_registration_sms(phone_number, code, phone_otp.id)
            resp = {
                'status': True,
                'otp_code': code,
                'phone_number': phone_number
            }
            return Response(resp)


    def get(self, request):
        pass


class PhoneValidationView(APIView):
    def post(self, request):
        request_data = request.data
        print(f'request data {request_data}')
        phone_number = request_data['phone_number']
        otp_code = request_data['otp_code']
        saved_otp = PhoneOtp.objects.filter(phone_number__iexact=phone_number)
        if saved_otp.exists():
            saved_otp = saved_otp.first()
            otp = saved_otp.otp_code
            if str(otp_code) == str(otp):
                saved_otp.validated = True
                saved_otp.save()
                resp = {
                    'phone_validated': True,
                    'message': 'phone number validated'
                }
                return Response(resp)
            else:
                resp = {
                    'phone_validated': False,
                    'message': 'OTP incorrect'
                }
                return Response(resp)
        else:
            resp = {
                'status': False,
                'phone_validated': False,
                'message': 'OTP record not found'
            }
            response = Response()
            response.data = resp
            return response  

    def get(self, request):
        pass



class RegistrationView(APIView):
    authentication_classes = ''
    permission_classes = ''

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        resp = {}
        if serializer.is_valid():
            email_ = serializer.validated_data['email']
            phone_number_ = serializer.validated_data['phone_number']
            first_name_ = serializer.validated_data['first_name']
            last_name_ = serializer.validated_data['last_name']
            try:
                loanee = Loanee.objects.get(phone_number=phone_number_)
                loanee_serializer = LoaneeSerializer(loanee)
                token, created = Token.objects.get_or_create(user=loanee.user)
                resp = {"loanee": loanee_serializer.data,
                    "token":token.key}
                return Response(resp)
            except ObjectDoesNotExist:
                user = User.objects.create_user(username=phone_number_, email=email_, first_name=first_name_, last_name=last_name_)
                user.set_password(serializer.validated_data['password'])
                user.save()

                g, created = Group.objects.get_or_create(name='Loanees')
                # g = Group.objects.get(name='Loanees')
                g.user_set.add(user)
                g.save()

                wallet = Wallet()
                wallet.save()

                if user.id:
                    loanee = Loanee.objects.create(first_name=first_name_, last_name=last_name_, phone_number=phone_number_, email=email_, user=user, wallet=wallet)
                    loanee.save()
                    token, created = Token.objects.get_or_create(user=user)
                    if loanee.user.id:
                        send_registration_welcome(loanee)
                        loanee_serializer = LoaneeSerializer(loanee)
                        resp = {"loanee": loanee_serializer.data,
                            "token": token.key}
                        return Response(resp)
        else:
            resp = {
                'status': False,
                'body': 'incorrect data provided'
            }
            return Response(resp)            

    def get(self, request):
        pass

class LoginView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        data = {}
        try:
            loanee = Loanee.objects.get(user=user)
            if loanee is not None:
                loanee_serializer = LoaneeSerializer(loanee)
                print(loanee_serializer.data)
                wallet = loanee.wallet
                wallet_serializer = WalletSerializer(wallet)
                # saving_method = wallet.saving_method
                # loanee_wallet = {"id":wallet.id,
                #     "account_balance":wallet.account_balance,
                #     "savings_balance":wallet.savings_balance,
                #     "total_spending":wallet.total_spending,
                #     "saving_method":{
                #         "id":saving_method.id,
                #         "saving_rate":saving_method.saving_rate,
                #         "frequency":saving_method.frequency,
                #         "saving_type":{
                #             "id":saving_method.saving_type.id,
                #             "name":saving_method.saving_type.name
                #         },                        
                #     }
                # }
                loans = Loan.objects.filter(loanee=loanee)
                loans_serializer = LoanSerializer(loans, many=True)
                data['loanee'] = loanee_serializer.data
                # data['loanee'] = {
                #             'user_id': loanee.user.id,
                #             'first_name': loanee.first_name,
                #             'last_name': loanee.last_name,
                #             'email': loanee.email,
                #             'phone_number': loanee.phone_number,
                #             'wallet':wallet_serializer.data,
                #             'loans':loans_serializer.data
                #         }
        except ObjectDoesNotExist:
            loanee = {}
            data['loanee'] = loanee

        data['token'] = token.key
        return JsonResponse(data)


class LoaneesView(APIView):
    def post(self, request):
        request_data = request.data
        res = {
            "ResultCode": 0,
            "data": request_data,
        }
        return Response(res)

    def get(self, request):
        loanees = Loanee.objects.all()
        serializer = LoaneeSerializer(loanees, many=True)
        res = {
            "ResultCode": 0,
            "data": serializer.data,
        }

        return Response(res)

class SavingMethodView(APIView):
    def post(self, request):
        request_data = request.data
        user_id = request_data['user']['id']
        _saving_method = request_data['saving_method']
        _saving_type_id = _saving_method['saving_type']['id']
        _frequency_id = _saving_method['frequency']['id']
        _rate = _saving_method['rate']
        try:
            loanee = Loanee.objects.get(user_id=user_id)
            saving_type = SavingMethodType.objects.get(id=_saving_type_id)
            frequency = SavingFrequency.objects.get(id=_frequency_id)
            saving_method = SavingMethod()
            saving_method.saving_type = saving_type
            saving_method.frequency = frequency
            saving_method.saving_rate = _rate
            saving_method.save()
            if saving_method.id:
                wallet = Wallet.objects.get(id=loanee.wallet.id)
                wallet.saving_method = saving_method
                wallet.save()
            loanee = Loanee.objects.get(user_id=user_id)
            serializer = LoaneeSerializer(loanee)
            res = {
                    "ResultCode": 0,
                    "user": serializer.data,
                    "message": "Saving method setup successfully",
                }
            return Response(res)
        except ObjectDoesNotExist:
            res = {
                "ResultCode": 1,
                "message": "User not found"
            }
            return Response(res)

    def get(self, request):
        saving_methods = SavingMethod.objects.all()
        serializer = SavingMethodSerializer(saving_methods)
        res = {
            "ResultCode": 0,
            "data": serializer.data,
        }

        return Response(res)



class LoansView(APIView):
    def post(self, request):
        request_data = request.data
        user_id = request_data['user']['id']
        try:
            loanee = Loanee.objects.get(user_id=user_id)
            for loan in request_data['loan']:
                _amount = loan['amount']
                _financier_id = loan['financier']['id']
                _interest_rate = loan['interest_rate']
                _period = loan['period']
                _disbursement_date = loan['disbursement_date']
                lender = Lender.objects.get(id=_financier_id)

                loanee_loan = Loan()
                loanee_loan.amount = _amount
                loanee_loan.interest_rate = _interest_rate
                loanee_loan.period = _period
                loanee_loan.financier = lender
                loanee_loan.disbursement_date = _disbursement_date
                loanee_loan.loanee = loanee
                loanee_loan.save()

                if loanee_loan.id:
                    lender = Lender.objects.get(id=_financier_id)
                    loanee_loan.financier = lender
            res = {
                "ResultCode": 0,
                "data": request_data,
                "message": "Loans setup successfully"
            }
            return Response(res)
        except ObjectDoesNotExist:
            res = {
                "ResultCode": 1,
                "message": "User not found"
            }
            return Response(res)

    def get(self, request):
        request_data = request.GET
        loanee_id = request_data['loanee_id']
        print(loanee_id)
        if loanee_id:
            try:
                loans = Loan.objects.filter(loanee_id=loanee_id)
                serializer = LoanSerializer(loans, many=True)
                res = {
                    "ResultCode": 0,
                    "data": serializer.data,
                }
                return Response(res)
            except Exception:
                res = {
                    "ResultCode": 1,
                    "message": "Loan details for that user not found",
                }
                return Response(res)
        else:
            loans = Loan.objects.all()
            serializer = LoanSerializer(loans, many=True)
            res = {
                "ResultCode": 0,
                "data": serializer.data,
            }
            return Response(res)

# class ListTodo(generics.ListCreateAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer


class ListLoanee(generics.ListCreateAPIView):
    queryset = Loanee.objects.all()
    serializer_class = LoaneeSerializer


# class DetailTodo(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer


class B2BTransaction(APIView):

    def post(self, request):
        recipient = request.data['recipient']
        amount = request.data['amount']
        account_reference = request.data['account_reference']

        resp = {
            'success': False,
            'message': ""
        }
        try:
            responseData = initiateB2BTransaction(recipient, amount, account_reference)
            resp["message"] = f"{responseData}"
            resp["success"] = 'Request posted'

        except Exception as e:
            resp["message"] = f'{e}'

        return Response(resp)


class C2BTransaction(APIView):

    def post(self, request):
        phone_number = request.data['phone_number']
        amount = request.data['amount']

        resp = {
            'info': False,
            'message': ""
        }
        try:
            res = initiateC2BTransaction(phone_number, amount)
            resp["message"] = f'{res}'
            resp["info"] = 'Request posted'

        except Exception as e:
            resp["message"] = f'{e}'

        return Response(resp)


class B2BListener(APIView):
    def post(self, request):
        request_data = request.data
        print(request_data)
        message = {
            "ResultCode": 0,
            "ResultDesc": "The service was accepted successfully",
            "ThirdPartyTransID": "1234567890"
        }

        return Response(message)

    def get(self, request):
        request_data = request.GET
        print(request_data)

        return Response(request_data)


class C2BListener(APIView):
    def post(self, request):
        request_data = request.data
        print(request_data)
        message = {
            "ResultCode": 0,
            "ResultDesc": "The service was accepted successfully",
            "ThirdPartyTransID": "1234567890"
        }

        return Response(message)

    def get(self, request):
        request_data = request.GET
        print(request_data)

        return Response(request_data)
