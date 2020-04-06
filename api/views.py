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
        data['token'] = token.key
        return JsonResponse(data)

# class ListTodo(generics.ListCreateAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer


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
