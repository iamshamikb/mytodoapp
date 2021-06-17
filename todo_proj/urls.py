from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('loggedinpage/', views.loggedinpage, name='loggedinpage'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),
    path('loginuser/', views.loginuser, name='loginuser'),
    path('createtodo/', views.createtodo, name='createtodo'),
    path('todo/<int:todo_pk>', views.viewtodo, name='viewtodo'),
    path('todo/<int:todo_pk>/completetodo', views.completetodo, name='completetodo'),
    path('todo/<int:todo_pk>/deletetodo', views.deletetodo, name='deletetodo'),
    path('completed/', views.completedtodos, name='completedtodos'),
    path('home/', views.home, name='home')
    
]
