-- PostGIS Migration SQL
-- PostgreSQL + PostGIS データベース作成・移行用スクリプト

-- 1. PostGIS拡張機能を有効化
CREATE EXTENSION IF NOT EXISTS postgis;

-- 2. レストランテーブル作成
CREATE TABLE IF NOT EXISTS restaurants (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    address TEXT NOT NULL,
    opening_hours VARCHAR(100) NOT NULL,
    rating DECIMAL(3,1) NOT NULL CHECK (rating >= 0 AND rating <= 5),
    lat DECIMAL(10,7) NOT NULL,
    lng DECIMAL(11,7) NOT NULL,
    osm_building_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- インデックス作成（位置情報検索用）
CREATE INDEX IF NOT EXISTS idx_restaurants_location ON restaurants (lat, lng);
CREATE INDEX IF NOT EXISTS idx_restaurants_osm_building ON restaurants (osm_building_id);
CREATE INDEX IF NOT EXISTS idx_restaurants_rating ON restaurants (rating);
CREATE INDEX IF NOT EXISTS idx_restaurants_name ON restaurants (name);

-- 3. OSM建物データテーブル作成（PostGIS対応）
CREATE TABLE IF NOT EXISTS osm_buildings (
    osm_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200),
    building_type VARCHAR(50),
    building_levels INTEGER,
    building_material VARCHAR(50),
    building_use VARCHAR(50),
    geometry GEOMETRY(POLYGON, 4326) NOT NULL,  -- PostGIS spatial column
    geometry_coordinates TEXT,  -- 後方互換性のためのJSON格納カラム
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- PostGIS空間インデックス（GIST）
CREATE INDEX IF NOT EXISTS idx_osm_buildings_geom ON osm_buildings USING GIST(geometry);
CREATE INDEX IF NOT EXISTS idx_osm_buildings_type ON osm_buildings (building_type);
CREATE INDEX IF NOT EXISTS idx_osm_buildings_use ON osm_buildings (building_use);

-- 4. 初期データ投入（PostGIS geometry使用）
INSERT INTO osm_buildings (osm_id, name, building_type, building_levels, building_material, building_use, geometry, geometry_coordinates) VALUES

-- アジアンパーム渋谷本町の建物 (実際のOSM ID)
('way/1081064846', 'Asian Palm Building', 'yes', 5, 'bricks', NULL,
 ST_GeomFromText('POLYGON((139.6819139 35.6821810, 139.6819745 35.6822094, 139.6820436 35.6821119, 139.6819829 35.6820835, 139.6819139 35.6821810))', 4326),
 JSON_BUILD_ARRAY(JSON_BUILD_ARRAY(
    JSON_BUILD_ARRAY(139.6819139, 35.6821810),
    JSON_BUILD_ARRAY(139.6819745, 35.6822094),
    JSON_BUILD_ARRAY(139.6820436, 35.6821119),
    JSON_BUILD_ARRAY(139.6819829, 35.6820835),
    JSON_BUILD_ARRAY(139.6819139, 35.6821810)
))),

-- 東京オペラシティタワー (複数レストラン入居)
('way/234567890', 'Tokyo Opera City Tower', 'commercial', 54, 'steel_concrete', 'commercial',
 ST_GeomFromText('POLYGON((139.6860 35.6830, 139.6870 35.6830, 139.6870 35.6842, 139.6860 35.6842, 139.6860 35.6830))', 4326),
 JSON_BUILD_ARRAY(JSON_BUILD_ARRAY(
    JSON_BUILD_ARRAY(139.6860, 35.6830),
    JSON_BUILD_ARRAY(139.6870, 35.6830),
    JSON_BUILD_ARRAY(139.6870, 35.6842),
    JSON_BUILD_ARRAY(139.6860, 35.6842),
    JSON_BUILD_ARRAY(139.6860, 35.6830)
))),

-- 永楽の建物
('way/345678901', 'Eiraku Building', 'commercial', 3, NULL, 'commercial',
 ST_GeomFromText('POLYGON((139.6870 35.6820, 139.6880 35.6820, 139.6880 35.6830, 139.6870 35.6830, 139.6870 35.6820))', 4326),
 JSON_BUILD_ARRAY(JSON_BUILD_ARRAY(
    JSON_BUILD_ARRAY(139.6870, 35.6820),
    JSON_BUILD_ARRAY(139.6880, 35.6820),
    JSON_BUILD_ARRAY(139.6880, 35.6830),
    JSON_BUILD_ARRAY(139.6870, 35.6830),
    JSON_BUILD_ARRAY(139.6870, 35.6820)
))),

-- テスト用建物データ
('way/123456', 'Tokyo Ramen Building', 'residential', NULL, NULL, NULL,
 ST_GeomFromText('POLYGON((139.6503 35.6762, 139.6505 35.6762, 139.6505 35.6764, 139.6503 35.6764, 139.6503 35.6762))', 4326),
 JSON_BUILD_ARRAY(JSON_BUILD_ARRAY(
    JSON_BUILD_ARRAY(139.6503, 35.6762),
    JSON_BUILD_ARRAY(139.6505, 35.6762),
    JSON_BUILD_ARRAY(139.6505, 35.6764),
    JSON_BUILD_ARRAY(139.6503, 35.6764),
    JSON_BUILD_ARRAY(139.6503, 35.6762)
))),

('way/789012', 'Sushi Zen Building', 'commercial', NULL, NULL, NULL,
 ST_GeomFromText('POLYGON((139.6510 35.6765, 139.6512 35.6765, 139.6512 35.6767, 139.6510 35.6767, 139.6510 35.6765))', 4326),
 JSON_BUILD_ARRAY(JSON_BUILD_ARRAY(
    JSON_BUILD_ARRAY(139.6510, 35.6765),
    JSON_BUILD_ARRAY(139.6512, 35.6765),
    JSON_BUILD_ARRAY(139.6512, 35.6767),
    JSON_BUILD_ARRAY(139.6510, 35.6767),
    JSON_BUILD_ARRAY(139.6510, 35.6765)
)))

ON CONFLICT (osm_id) DO UPDATE SET
    name = EXCLUDED.name,
    building_type = EXCLUDED.building_type,
    building_levels = EXCLUDED.building_levels,
    building_material = EXCLUDED.building_material,
    building_use = EXCLUDED.building_use,
    geometry = EXCLUDED.geometry,
    geometry_coordinates = EXCLUDED.geometry_coordinates,
    updated_at = NOW();

-- 5. 初期レストランデータ投入
INSERT INTO restaurants (id, name, address, opening_hours, rating, lat, lng, osm_building_id, created_at, updated_at) VALUES

('rest_001', 'アジアンパーム渋谷本町', '東京都渋谷区本町2-14-4', '11:30 - 14:30, 17:00 - 23:00', 4.0, 35.682179, 139.68194, 'way/1081064846', NOW(), NOW()),
('rest_002', '松阪牛 よし田', '東京都新宿区西新宿3-20-2 東京オペラシティ53F', '11:30 - 14:30, 17:30 - 21:30', 4.5, 35.6836, 139.6865, 'way/234567890', NOW(), NOW()),
('rest_003', '叙々苑 東京オペラシティ53店', '東京都新宿区西新宿3-20-2 東京オペラシティ53F', '11:30 - 22:00', 4.3, 35.6836, 139.6865, 'way/234567890', NOW(), NOW()),
('rest_004', '永楽', '東京都渋谷区本町2-47-2', '11:00 - 14:00, 17:00 - 21:00', 4.1, 35.6825, 139.6875, 'way/345678901', NOW(), NOW()),
('rest_005', '大戸屋ごはん処 東京オペラシティ店', '東京都新宿区西新宿3-20-2 東京オペラシティB1F', '11:00 - 22:00', 3.8, 35.6834, 139.6863, 'way/234567890', NOW(), NOW()),
('rest_006', 'そじ坊 東京オペラシティ店', '東京都新宿区西新宿3-20-2 東京オペラシティB1F', '11:00 - 22:00', 3.9, 35.6834, 139.6863, 'way/234567890', NOW(), NOW()),
('rest_007', '田中そば店 東京オペラシティ店', '東京都新宿区西新宿3-20-2 東京オペラシティ', '11:00 - 21:00', 4.2, 35.6835, 139.6864, 'way/234567890', NOW(), NOW()),
('rest_008', 'サブウェイ 東京オペラシティ店', '東京都新宿区西新宿3-20-2 東京オペラシティB1F', '7:00 - 21:00', 3.6, 35.6834, 139.6863, 'way/234567890', NOW(), NOW())

ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    address = EXCLUDED.address,
    opening_hours = EXCLUDED.opening_hours,
    rating = EXCLUDED.rating,
    lat = EXCLUDED.lat,
    lng = EXCLUDED.lng,
    osm_building_id = EXCLUDED.osm_building_id,
    updated_at = NOW();

-- 6. 空間検索のサンプルクエリ（テスト用）
-- 指定座標を含む建物を検索
-- SELECT osm_id, name, building_type FROM osm_buildings WHERE ST_Contains(geometry, ST_Point(139.6819, 35.6822));

-- 指定範囲内の建物を検索
-- SELECT osm_id, name, ST_Distance(geometry, ST_Point(139.6819, 35.6822)) as distance 
-- FROM osm_buildings 
-- WHERE ST_DWithin(geometry, ST_Point(139.6819, 35.6822), 0.001)
-- ORDER BY distance;