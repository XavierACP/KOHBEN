"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView
from sales.views import IndexView, BlogView, PostView, RegisterView, AboutView, ContactView, RegisterOk, PostListView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('index', IndexView.as_view(), name='index'),
    # path('blog', BlogView.as_view(), name='blog'),
    # path('post', PostView.as_view(), name='post'),
    path('about', AboutView.as_view(), name='about'),
    path('contact', ContactView.as_view(), name='contact'),
    path('login', PostView.as_view(), name='post'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    url(r'register', RegisterView.as_view(), name='register'),
    path('regOk', RegisterOk.as_view(), name='registerOk'),
    path('accounts/post/list', PostListView.as_view(), name='post_list'),

    #     path('regOk', RegisterOk.as_view(), name='registerOk'),
# # for password reset views:
#     url('^', include('django.contrib.auth.urls')),
#     url(r'^password_reset/$', auth_views.PasswordResetView, {'template_name': 'accounts/password_reset_form'},
#         name='password_reset'),
#     url(r'^password_reset/done/$', auth_views.PasswordResetDoneView, name='password_reset_done'),
#     url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
#         auth_views.PasswordResetConfirmView, name='password_reset_confirm'),
#     url(r'^reset/done/$', auth_views.PasswordResetCompleteView, name='password_reset_complete'),
#     url(r'^password_reset_form/$', auth_views.PasswordResetView, name='password_reset_form'),
]
