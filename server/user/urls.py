from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('login/', views.CreateTokenView.as_view(), name='login'),
    path('', views.ManageUserView.as_view(), name='index')
]
