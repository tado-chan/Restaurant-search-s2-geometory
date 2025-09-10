"""
Repository layer for data access operations with PostGIS Support
"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from geoalchemy2.functions import ST_Contains, ST_Point, ST_Distance, ST_DWithin
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
    OSM建物データアクセス用リポジトリ with PostGIS Spatial Queries
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
    
    def find_building_by_point(self, lat: float, lng: float) -> Optional[OSMBuilding]:
        """
        指定座標を含む建物をPostGISで検索（新機能）
        Returns: OSMBuilding or None
        """
        point = ST_Point(lng, lat)  # PostGIS Point (lng, lat order)
        
        return (
            self.db.query(OSMBuilding)
            .filter(ST_Contains(OSMBuilding.geometry, point))
            .first()
        )
    
    def find_buildings_near_point(self, lat: float, lng: float, distance_meters: float = 100) -> List[Tuple[OSMBuilding, float]]:
        """
        指定座標周辺の建物を距離付きで検索
        Returns: List[(OSMBuilding, distance_meters)]
        """
        point = ST_Point(lng, lat)
        
        # PostGISのST_DWithinで範囲内検索 + ST_Distanceで距離計算
        results = (
            self.db.query(
                OSMBuilding,
                ST_Distance(OSMBuilding.geometry, point).label('distance')
            )
            .filter(ST_DWithin(OSMBuilding.geometry, point, distance_meters))
            .order_by('distance')
            .all()
        )
        
        return [(building, float(distance)) for building, distance in results]


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