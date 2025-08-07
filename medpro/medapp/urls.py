from django.urls import path
from . import views
urlpatterns = [
    path('',views.homepage,name='home'),
    path('login/',views.login_view,name='login'),
    path('signup/',views.signup_view,name='signup'),
    path('userhome/',views.homepage_user,name='userhome'),
    path('pharmacyhome/',views.homepage_pharmacy,name='pharmacyhome'),
    path('profile/',views.profile_view,name='profile'),
    path('pharmacysignup/',views.pharmacy_signup, name='pharmacy_signup'),
    path('logout/',views.logout_view, name='logout'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('payment/<int:medicine_id>/', views.payment_view, name='payment'),
    path('about/', views.about, name='about'),
    path('addmedicine/', views.add_medicine, name='addmedicine'),
    path('booking/<int:id>/',views.booking,name='booking'),
    path('payments/', views.payment_list, name='payment_list'),
    path('delete-medicine/<int:id>/', views.delete_medicine, name='delete_medicine'),

]