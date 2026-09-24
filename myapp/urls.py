from django.urls import path
from .views import *
urlpatterns =[
    path('',index_view, name='index_page'),
    path('about/',about_view, name='about_page'),
   
   
    path('Login/',login_view, name='Login_page'),
    path('Register/',register_view, name='Register_page'),

    path('logout/',Logout_view, name='Logout_page'),

    path('forgotpassword/', forgot_password_view, name='forgot_password_page'),

    path('add_to_cart/<int:product_id>/', add_to_cart_view, name='add_to_cart'),

    path('cart_count/',cart_count, name='cart_count'),

    path('cart_item_page_view/',cart_item_page_view, name='cart_item_page_view'),

    path(' update_cart_item_quantity/<int:item_id>/<str:action>/', update_cart_item_quantity,
          name='update_cart_item_quantity'),

]