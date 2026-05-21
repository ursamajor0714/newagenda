from django.urls import path,include
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name="post_detail"),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/hate/', views.hate_post, name='hate_post'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('post/<int:pk>/comment/', views.comment, name="comment"),
    path('write/', views.write, name='write'),
    path('trap/', views.trap, name='trap'),
]
