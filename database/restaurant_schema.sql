-- レストランデータベース作成用 SQL
-- Heidi SQL で実行してください

-- データベース作成 (必要に応じて)
-- CREATE DATABASE restaurant_search_app;
-- USE restaurant_search_app;

-- レストランテーブル作成
CREATE TABLE restaurants (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    address TEXT NOT NULL,
    opening_hours VARCHAR(100) NOT NULL,
    rating DECIMAL(3,1) NOT NULL CHECK (rating >= 0 AND rating <= 5),
    lat DECIMAL(10,7) NOT NULL,
    lng DECIMAL(11,7) NOT NULL,
    osm_building_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- インデックス作成（位置情報検索用）
    INDEX idx_location (lat, lng),
    INDEX idx_osm_building (osm_building_id),
    INDEX idx_rating (rating),
    INDEX idx_name (name)
);

-- OSM建物データテーブル作成
CREATE TABLE osm_buildings (
    osm_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200),
    building_type VARCHAR(50),
    building_levels INT,
    building_material VARCHAR(50),
    building_use VARCHAR(50),
    geometry_coordinates JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- インデックス作成
    INDEX idx_building_type (building_type),
    INDEX idx_building_use (building_use)
);