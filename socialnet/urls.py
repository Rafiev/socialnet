"""
URL configuration for socialnet project.

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
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage),
    path('posts/<int:id>/', views.post_detail),
    path('profile/<int:id>/', views.profile_detail, name='profile'),
    path('shorts/', views.shorts, name='shorts-list'),
    path('short/<int:id>/', views.short_info, name='shorts-info'),
    path('saved_posts/', views.saved_posts, name='saved-posts'),
    path('<int:user_id>/', views.user_posts, name='user-posts'),
    path('add_post/', views.create_post, name='add-post'),
    path('add_short/', views.add_short, name='add-short'),
    path('add-saved/', views.add_saved, name='add-saved'),
    path('users/', include('userapp.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
