from django.urls import include, path

from . import views

urlpatterns = [
    path('register-phone/', views.PhoneRegistrationView.as_view(), name='PhoneRegistrationView'),
    path('resend-code/', views.ResendCodeView.as_view(), name='ResendCodeView'),
    path('validate-phone/', views.PhoneValidationView.as_view(), name='PhoneValidationView'),
    path('register/', views.RegistrationView.as_view(), name='RegistrationView'),
    path('login/', views.LoginView.as_view(), name='LoginView'),
    path('loan/', views.LoansView.as_view(), name='LoansView'),
    path('lonees/', views.LoaneesView.as_view(), name='LoaneesView'),
    path('saving-method/', views.SavingMethodView.as_view(), name='SavingMethodView'),
    # path('todos/', views.ListTodo.as_view()),
    path('loanees/', views.ListLoanee.as_view()),
    path('initc2b/',views.C2BTransaction.as_view(),name='C2BTransaction'),
    path('initb2b/',views.B2BTransaction.as_view(),name='B2BTransaction'),
    path('listenb2b/',views.B2BListener.as_view(),name='B2BListener'),
    path('listenc2b/',views.C2BListener.as_view(),name='C2BListener'),
    # path('<int:pk>/', views.DetailTodo.as_view()),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
]
