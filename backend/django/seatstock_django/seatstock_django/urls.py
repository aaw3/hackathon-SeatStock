"""
URL configuration for seatstock_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
#    path("",include('django_mongo.urls')), 
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
    path("tickets", views.tickets, name="tickets"),
    path("market", views.marketdata, name="marketdata"),
    path("FAQ", views.FAQ, name="FAQ"),
    path("account_session_data", views.account_session_data, name="account_session_data"),
    path("buy", views.buy, name="buy"),
    path("sell", views.sell, name="sell")
]
