from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from .dash_apps.finished_apps import stock_graphic
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile.html',views.profile, name='profile'),
    path("register", views.register_request, name="register"),
    path('about.html', views.about, name='about'),
    path('add_stock.html', views.add_stock, name='add_stock'),
    path('list_stock.html', views.list_stock, name='list_stock'),
    path('stocks.html', views.view_stock, name='view_stock'),
    path('search',views.searchView,name='search'),
    path('predict_stock.html', views.predict_home,name='predict_home'),
    path('predict/', views.predict, name="predict"),
    path('delete/<stock_id>', views.delete, name='delete'),  # 'delete/<stock_id>' we will use this format when we create a path without create a html file.We call it from add_stock.html
    path('delete_stock.html', views.delete_stock, name='delete_stock'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')))
]

urlpatterns += staticfiles_urlpatterns()
