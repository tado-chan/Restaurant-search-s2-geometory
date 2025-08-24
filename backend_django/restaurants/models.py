"""
SQLAlchemy models for Restaurant Search App
"""
from sqlalchemy import create_engine, Column, String, Numeric, Integer, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from django.conf import settings
import json
from typing import List, Dict, Any

# SQLAlchemy setup
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Restaurant(Base):
    """
    レストラン情報モデル
    """
    __tablename__ = "restaurants"
    
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    address = Column(Text, nullable=False)
    opening_hours = Column(String(100), nullable=False)
    rating = Column(Numeric(3, 1), nullable=False, index=True)
    lat = Column(Numeric(10, 7), nullable=False, index=True)
    lng = Column(Numeric(11, 7), nullable=False, index=True)
    osm_building_id = Column(String(50), index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'openingHours': self.opening_hours,
            'rating': float(self.rating),
            'lat': float(self.lat),
            'lng': float(self.lng),
            'osmBuildingId': self.osm_building_id
        }
    
    def __repr__(self):
        return f"<Restaurant(id='{self.id}', name='{self.name}', rating={self.rating})>"


class OSMBuilding(Base):
    """
    OpenStreetMap建物データモデル
    """
    __tablename__ = "osm_buildings"
    
    osm_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(200))
    building_type = Column(String(50), index=True)
    building_levels = Column(Integer)
    building_material = Column(String(50))
    building_use = Column(String(50), index=True)
    geometry_coordinates = Column(Text, nullable=False)  # JSON string
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """モデルを辞書形式に変換"""
        return {
            'osm_id': self.osm_id,
            'name': self.name,
            'building_type': self.building_type,
            'building_levels': self.building_levels,
            'building_material': self.building_material,
            'building_use': self.building_use,
            'geometry_coordinates': self.get_geometry_coordinates()
        }
    
    def get_geometry_coordinates(self) -> List[List[List[float]]]:
        """JSON形式の座標データをパース"""
        try:
            return json.loads(self.geometry_coordinates)
        except (json.JSONDecodeError, TypeError):
            return []
    
    def to_geojson_feature(self) -> Dict[str, Any]:
        """GeoJSON Feature形式に変換"""
        return {
            'type': 'Feature',
            'properties': {
                'building': self.building_type or 'yes',
                'osm_id': self.osm_id,
                'name': self.name,
                'building:levels': str(self.building_levels) if self.building_levels else None,
                'building:material': self.building_material,
                'building:use': self.building_use
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': self.get_geometry_coordinates()
            }
        }
    
    def __repr__(self):
        return f"<OSMBuilding(osm_id='{self.osm_id}', name='{self.name}')>"


# データベースセッション管理
def get_db_session():
    """データベースセッションを取得"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()