"""
URL patterns for restaurants app
"""
from django.urls import path
from . import views

urlpatterns = [
    # ヘルスチェック
    path('health/', views.health_check, name='health_check'),
    
    # レストラン検索
    path('search/', views.search_restaurant, name='search_restaurant'),
    path('search/optimized/', views.search_restaurant_optimized, name='search_restaurant_optimized'),
    path('search/location/', views.search_restaurants_by_location, name='search_by_location'),
    
    # レストラン情報
    path('restaurants/', views.get_restaurants, name='get_restaurants'),
    path('restaurants/<str:restaurant_id>/', views.get_restaurant_detail, name='get_restaurant_detail'),
    
    # OSM建物データ
    path('buildings/', views.get_buildings, name='get_buildings'),
    path('buildings/<str:osm_id>/', views.get_osm_building, name='get_osm_building'),
]