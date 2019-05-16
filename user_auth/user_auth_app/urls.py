from django.urls import path ,include
from user_auth_app import views

app_name = "user_auth_app"

urlpatterns = [
    path(r'',views.user_auth_index,name = "user_auth_index"),
    path(r'user_login/',views.user_login,name = "user_login"),
    path(r'register/',views.registration,name = "registration"),
    path(r'user_logout/',views.user_logout,name="user_logout"),
    path(r'special/',views.special,name="special"),

]