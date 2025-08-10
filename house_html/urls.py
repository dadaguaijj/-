from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('index'), name='home'),  # 根路径重定向到index
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # 修复视图函数名冲突
    path('logout/', views.logout_view, name='logout'),  # 修复视图函数名冲突
    path('profile/', views.profile_view, name='profile'),
    
    # 房源相关路由
    path('houses/', views.houses_view, name='houses'),
    path('house/<int:house_id>/', views.house_detail, name='house_detail'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('api/add_favorite/', views.add_favorite, name='add_favorite'),
    path('api/remove_favorite/', views.remove_favorite, name='remove_favorite'),
    path('api/update_profile/', views.update_profile, name='update_profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]