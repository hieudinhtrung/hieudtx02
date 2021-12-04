from django.urls import path
from phonemanage import views
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
     path("logout/", views.user_logout, name="logout"),
     path('contact/listcontact/', views.listcontact,name= 'listcontact'),
     path('add_contact/', views.create_contact, name="create_contact"),
     path('edit_contact/<int:pk>', views.edit_contact, name="edit_contact"),
     path('delete_contact/<int:pk>', views.delete_contact, name="delete_contact"),
     path('show_contact/<int:pk>', views.show_contact, name="show_contact"),
     path('importexcel_contact/', views.impo, name="import_contact")
]
