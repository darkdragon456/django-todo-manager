from django.urls import path
from users import views as users_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', users_views.register, name='register'),

    path(
        'login/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login'
    ),

    path(
        'logout/',
        users_views.logout_view,
        name='logout'
    ),
]