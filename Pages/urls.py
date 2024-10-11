


from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("" , views.home_page , name= "home_page"),
    path('Login/' , views.login_form ,  name= "login_form"),
    path('CreatePassword/' , views.set_password ,  name= "create_password"),
    path("verify-otp/" , views.verify_otp , name= "verify_otp"),
    path("CreateAccount/", views.create_account , name= "create_account"),
    path('success/', views.success_page , name= "success_page"),
    path('forget-password/', views.forget_pass , name ="forgot_password"),
    path('reset-password/', views.reset_password , name ="reset_password"),
    path('verify-email/', views.forget_password_otp , name ="verify_email"),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)