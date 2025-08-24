"""
Repository layer for data access operations
"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from .models import Restaurant, OSMBuilding
import math


class RestaurantRepository:
    """
    レストランデータアクセス用リポジトリ
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[Restaurant]:
        """全レストランを取得"""
        return self.db.query(Restaurant).order_by(Restaurant.rating.desc()).all()
    
    def get_by_id(self, restaurant_id: str) -> Optional[Restaurant]:
        """IDでレストランを取得"""
        return self.db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    
    def find_nearest_restaurant(self, lat: float, lng: float) -> Optional[Tuple[Restaurant, float]]:
        """
        指定座標に最も近いレストランを検索
        Returns: (Restaurant, distance) or None
        """
        # SQLAlchemyで距離計算（ユークリッド距離の近似）
        distance_query = func.sqrt(
            func.pow(Restaurant.lat - lat, 2) + 
            func.pow(Restaurant.lng - lng, 2)
        ).label('distance')
        
        result = (
            self.db.query(Restaurant, distance_query)
            .order_by(distance_query)
            .first()
        )
        
        if result:
            restaurant, distance = result
            return restaurant, float(distance)
        return None
    
    def find_restaurants_within_radius(self, lat: float, lng: float, radius_km: float = 1.0) -> List[Tuple[Restaurant, float]]:
        """
        指定座標から半径内のレストランを検索
        """
        # 1度の緯度経度は約111kmなので、km to degree conversion
        radius_deg = radius_km / 111.0
        
        distance_query = func.sqrt(
            func.pow(Restaurant.lat - lat, 2) + 
            func.pow(Restaurant.lng - lng, 2)
        ).label('distance')
        
        results = (
            self.db.query(Restaurant, distance_query)
            .filter(distance_query <= radius_deg)
            .order_by(distance_query)
            .all()
        )
        
        return [(restaurant, float(distance)) for restaurant, distance in results]
    
    def search_by_name(self, name: str) -> List[Restaurant]:
        """名前で部分一致検索"""
        return (
            self.db.query(Restaurant)
            .filter(Restaurant.name.contains(name))
            .order_by(Restaurant.rating.desc())
            .all()
        )


class OSMBuildingRepository:
    """
    OSM建物データアクセス用リポジトリ
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[OSMBuilding]:
        """全OSM建物を取得"""
        return self.db.query(OSMBuilding).all()
    
    def get_by_osm_id(self, osm_id: str) -> Optional[OSMBuilding]:
        """OSM IDで建物を取得"""
        return self.db.query(OSMBuilding).filter(OSMBuilding.osm_id == osm_id).first()
    
    def get_by_building_type(self, building_type: str) -> List[OSMBuilding]:
        """建物タイプで検索"""
        return (
            self.db.query(OSMBuilding)
            .filter(OSMBuilding.building_type == building_type)
            .all()
        )
    
    def get_commercial_buildings(self) -> List[OSMBuilding]:
        """商業建物を取得"""
        return (
            self.db.query(OSMBuilding)
            .filter(OSMBuilding.building_use == 'commercial')
            .all()
        )


class RestaurantSearchRepository:
    """
    レストラン検索用複合リポジトリ
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.restaurant_repo = RestaurantRepository(db)
        self.osm_building_repo = OSMBuildingRepository(db)
    
    def search_restaurant_with_building(self, lat: float, lng: float) -> Optional[Tuple[Restaurant, Optional[OSMBuilding], float]]:
        """
        レストラン検索 + 対応するOSM建物データを取得
        Returns: (Restaurant, OSMBuilding|None, distance)
        """
        result = self.restaurant_repo.find_nearest_restaurant(lat, lng)
        
        if not result:
            return None
        
        restaurant, distance = result
        osm_building = None
        
        if restaurant.osm_building_id:
            osm_building = self.osm_building_repo.get_by_osm_id(restaurant.osm_building_id)
        
        return restaurant, osm_building, distance
    
    def get_restaurant_with_building(self, restaurant_id: str) -> Optional[Tuple[Restaurant, Optional[OSMBuilding]]]:
        """
        特定レストラン + 対応するOSM建物データを取得
        """
        restaurant = self.restaurant_repo.get_by_id(restaurant_id)
        
        if not restaurant:
            return None
        
        osm_building = None
        if restaurant.osm_building_id:
            osm_building = self.osm_building_repo.get_by_osm_id(restaurant.osm_building_id)
        
        return restaurant, osm_building