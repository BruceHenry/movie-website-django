"""MovieHunter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.urls import include, path
from django.contrib import admin
from django.shortcuts import render
from . import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    url(r'^admin/', admin.site.urls, {'extra_context': views.get_dict_context()}),
    url(r'^movie/', include('movie.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^$', views.index, name='index'),
    # error here 
    # url(r'.*', lambda request: render(request, '404.html'), name='404'),
    #path('dict_context/', views.get_dict_context, name='get-dict-context'),
    path('fuck-chart/', views.population_chart, name='fuck-chart'),

    path('verification/', include('verify_email.urls')),] 



urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)