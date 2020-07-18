from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #path('', include('allauth.urls', namespace='social')),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.register, name="register"),
    path('products/', views.products, name="products"),
    path('customer_order/', views.customerorder, name='customer_order'),
    path('user_order/', views.customerorder, name='user_order'),
    path('user_profile/', views.userpage, name='user_profile'),
    path('customer/<str:pk_test>', views.customer, name="customer"),
    path('create_order/<slug:pk>', views.createOrder, name="create_order"),
    path('update_order/<str:pk>', views.UpdateOrder, name="update_order"),
    path('delete_order/<str:pk>', views.deleteOrder, name="delete_order"),
    path('showusertoadmin/', views.showtotaluser, name="showusertoadmin"),
    path('userprofiledata/', views.userprofile, name="userprofiledata"),
    path('add_product/', views.addProduct, name="add_product"),
    path('add_tags/', views.addTag, name="add_tags"),

    #Auth password reset URL's
    path('reset_password/', auth_views.PasswordResetView.as_view
    (template_name="salesforce/password_reset_files/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view
    (template_name="salesforce/password_reset_files/password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
template_name="salesforce/password_reset_files/password_reset_form.html"
    ), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
template_name="salesforce/password_reset_files/password_reset_done.html"
    ),
         name="password_reset_complete"),
    ]