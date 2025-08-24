"""
Service layer for business logic
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from .repositories import RestaurantRepository, OSMBuildingRepository, RestaurantSearchRepository
from .models import Restaurant, OSMBuilding


class RestaurantSearchService:
    """
    レストラン検索ビジネスロジック
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.search_repo = RestaurantSearchRepository(db)
        self.restaurant_repo = RestaurantRepository(db)
        self.osm_building_repo = OSMBuildingRepository(db)
    
    def search_nearest_restaurant(self, lat: float, lng: float) -> Optional[Dict[str, Any]]:
        """
        最寄りレストラン検索（建物ポリゴン付き）
        """
        result = self.search_repo.search_restaurant_with_building(lat, lng)
        
        if not result:
            return None
        
        restaurant, osm_building, distance = result
        
        # レスポンス構築
        response = {
            'restaurant': restaurant.to_dict(),
            'buildingPolygon': osm_building.to_geojson_feature() if osm_building else None,
            'message': f'{restaurant.name}が見つかりました',
            'distance': distance
        }
        
        return response
    
    def search_nearest_restaurant_optimized(self, lat: float, lng: float) -> Optional[Dict[str, Any]]:
        """
        最寄りレストラン検索（OSM ID最適化版）
        """
        result = self.restaurant_repo.find_nearest_restaurant(lat, lng)
        
        if not result:
            return None
        
        restaurant, distance = result
        
        # OSM ID最適化版レスポンス
        response = {
            'restaurant': restaurant.to_dict(),
            'osmBuildingId': restaurant.osm_building_id,
            'message': f'{restaurant.name}が見つかりました (OSM ID最適化)',
            'distance': distance
        }
        
        return response
    
    def get_all_restaurants(self) -> List[Dict[str, Any]]:
        """
        全レストラン一覧取得
        """
        restaurants = self.restaurant_repo.get_all()
        return [restaurant.to_dict() for restaurant in restaurants]
    
    def get_restaurant_detail(self, restaurant_id: str) -> Optional[Dict[str, Any]]:
        """
        レストラン詳細情報取得
        """
        result = self.search_repo.get_restaurant_with_building(restaurant_id)
        
        if not result:
            return None
        
        restaurant, osm_building = result
        
        return {
            'restaurant': restaurant.to_dict(),
            'buildingPolygon': osm_building.to_geojson_feature() if osm_building else None,
        }
    
    def search_restaurants_by_location(self, lat: float, lng: float, radius_km: float = 1.0) -> List[Dict[str, Any]]:
        """
        位置ベースレストラン検索（範囲指定）
        """
        results = self.restaurant_repo.find_restaurants_within_radius(lat, lng, radius_km)
        
        response_list = []
        for restaurant, distance in results:
            response_list.append({
                'restaurant': restaurant.to_dict(),
                'distance': distance
            })
        
        return response_list
    
    def search_restaurants_by_name(self, name: str) -> List[Dict[str, Any]]:
        """
        名前検索
        """
        restaurants = self.restaurant_repo.search_by_name(name)
        return [restaurant.to_dict() for restaurant in restaurants]


class OSMBuildingService:
    """
    OSM建物データビジネスロジック
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.osm_repo = OSMBuildingRepository(db)
    
    def get_building_by_osm_id(self, osm_id: str) -> Optional[Dict[str, Any]]:
        """
        OSM IDで建物データ取得
        """
        building = self.osm_repo.get_by_osm_id(osm_id)
        
        if not building:
            return None
        
        return building.to_geojson_feature()
    
    def get_all_buildings(self) -> List[Dict[str, Any]]:
        """
        全建物データ取得
        """
        buildings = self.osm_repo.get_all()
        return [building.to_dict() for building in buildings]
    
    def get_commercial_buildings(self) -> List[Dict[str, Any]]:
        """
        商業建物一覧取得
        """
        buildings = self.osm_repo.get_commercial_buildings()
        return [building.to_geojson_feature() for building in buildings]


class ValidationService:
    """
    入力値検証サービス
    """
    
    @staticmethod
    def validate_coordinates(lat: float, lng: float) -> Dict[str, Any]:
        """
        座標の有効性検証
        """
        errors = []
        
        # 緯度の範囲チェック（-90 to 90）
        if not (-90 <= lat <= 90):
            errors.append("緯度は-90から90の範囲で指定してください")
        
        # 経度の範囲チェック（-180 to 180）
        if not (-180 <= lng <= 180):
            errors.append("経度は-180から180の範囲で指定してください")
        
        # 日本の座標範囲チェック（おおよそ）
        if not (24 <= lat <= 46) or not (123 <= lng <= 146):
            errors.append("座標が日本の範囲外です")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }
    
    @staticmethod
    def validate_search_radius(radius: float) -> Dict[str, Any]:
        """
        検索半径の検証
        """
        errors = []
        
        if radius <= 0:
            errors.append("検索半径は0より大きい値を指定してください")
        
        if radius > 50:  # 50km以上は制限
            errors.append("検索半径は50km以下で指定してください")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }