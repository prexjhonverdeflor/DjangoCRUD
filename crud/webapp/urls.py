
from django.urls import path
from . import views 



urlpatterns = [
    path('add-record/', views.add_record, name='add-record'),
    
    path('', views.home, name=""),
    path('register', views.register, name="register"),
    path('my-login', views.my_login, name="my-login"),
    path('user-logout', views.user_logout, name="user-logout"),

    path('dashboard', views.admin_dashboard, name="dashboard"),
    path('update-record/<int:pk>', views.update_record, name="update-record"),
    path('delete-record/<int:pk>', views.delete_record, name="delete-record"),

    path('bic-setup/', views.bic_setup, name='bic_setup'),
    path('bic-create/', views.bic_setup_create, name='bic_setup_create'),
    path('bic-update/<int:bic_setup_id>', views.bic_setup_update, name='bic_setup_update'),
    path('bic-delete/<int:pk>/', views.bic_setup_delete, name='bic_setup_delete'),

    path('cashier-dashboard', views.cashier_dashboard, name='mc_register'),
    path('mc-create/', views.mc_register_create, name='mc_register_create'),
    path('mc-update/<int:mc_register_id>', views.mc_register_update, name='mc_register_update'),

    path('peso-net', views.peso_net, name='peso_net'),
    path('peso-create/', views.peso_create, name='peso_create'),
    path('peso-update/<int:peso_net_id>', views.peso_update, name='peso_update'),


]