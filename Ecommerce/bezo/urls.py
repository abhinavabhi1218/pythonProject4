from django.urls import path
from . import views
from .forms import LoginForm, MyPasswordForm, MyPasswordResetForm, MyPasswordResetConfirmForm
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.ProductView.as_view(), name='home'),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cartshow, name="cartshow"),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.CustomerProfile.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>/', views.mobile, name='mobile_data'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>/', views.laptop, name='laptop_data'),
    path('tops/', views.tops, name='tops'),
    path('bottoms/', views.bottom, name='bottoms'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='bezo/login.html', 
    authentication_form=LoginForm)  ,name='login'),
    path('registration/', views.CustomerRegistration.as_view(), name='customerregistration'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(
        template_name='bezo/passwordchange.html', form_class=MyPasswordForm,
         success_url='/passwrodchangedone/'), name='passwordchange'),
    path('passwrodchangedone/', auth_views.PasswordChangeView.as_view(
        template_name='bezo/passwordchangedone.html'), name='passwrodchangedone'),    

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='bezo/password_reset.html', form_class=MyPasswordResetForm),
         name='password_reset'),

    path('password-reset/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='bezo/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='bezo/password_reset_confirm.html',
         form_class=MyPasswordResetConfirmForm), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='bezo/password_reset_complete.html'), name='password_reset_complete'),
   
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('search/', views.search_view, name='search'),
]