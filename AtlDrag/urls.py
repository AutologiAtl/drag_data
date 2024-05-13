"""
URL configuration for AtlDrag project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drag.views import * 

urlpatterns = [
    path('admin/', admin.site.urls),

    path('move_customer/', move_customer, name='move_customer'),
    path('index/', index, name='index'),
    path('table/', table_view, name='table_view'),
    path('edit/<int:pk>/', edit_row, name='edit_row'),
    path("add/",add_formdata , name="add"),
    path("save/",add_row , name = "save"),
    path("submit-form/", addNewEntry , name='submit-form'),
    path("search/",Search , name='Search'),
    path("list/",list_hystory , name='list'),
    path("login/",login_view, name="login"),
    path('logout/',logout_view,name='logout')
]
