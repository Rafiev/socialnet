from django.urls import path
from . import views

urlpatterns = [
    path('posts/<int:id>/', views.post_detail, name='post-detail'),
    path('profile/<int:id>/', views.profile_detail, name='profile'),
    path('add-profile/', views.add_profile, name='add-profile'),
    path('shorts/', views.shorts, name='shorts-list'),
    path('short/<int:id>/', views.short_info, name='shorts-info'),
    path('saved_posts/', views.saved_posts, name='saved-posts'),
    path('<int:user_id>/', views.user_posts, name='user-posts'),
    path('add_post/', views.create_post, name='add-post'),
    path('add_short/', views.add_short, name='add-short'),
    path('add-saved/', views.add_saved, name='add-saved'),
    path('subscribe/<int:profile_id>/', views.subscribe, name='subscribe'),
    # path('search/', views.search, name='search'),
    path('search-result/', views.search_result, name='search-result'),
    path('notifications/', views.notifications, name='notifications'),
]