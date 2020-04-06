from django.urls import include, path

from . import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='RegistrationView'),
    path('login/', views.LoginView.as_view(), name='LoginView'),
    path('initc2b/',views.C2BTransaction.as_view(),name='C2BTransaction'),
    path('initb2b/',views.B2BTransaction.as_view(),name='B2BTransaction'),
    path('listenb2b/',views.B2BListener.as_view(),name='B2BListener'),
    path('listenc2b/',views.C2BListener.as_view(),name='C2BListener'),
    # path('<int:pk>/', views.DetailTodo.as_view()),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
]
