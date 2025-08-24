-- OSM建物データ投入用 SQL
-- Heidi SQL で実行してください

-- OSM建物データ投入
INSERT INTO osm_buildings (osm_id, name, building_type, building_levels, building_material, building_use, geometry_coordinates) VALUES

-- アジアンパーム渋谷本町の建物 (実際のOSM ID)
('way/1081064846', 'Asian Palm Building', 'yes', 5, 'bricks', NULL, 
JSON_ARRAY(JSON_ARRAY(
    JSON_ARRAY(139.6819139, 35.6821810),
    JSON_ARRAY(139.6819745, 35.6822094),
    JSON_ARRAY(139.6820436, 35.6821119),
    JSON_ARRAY(139.6819829, 35.6820835),
    JSON_ARRAY(139.6819139, 35.6821810)
))),

-- 東京オペラシティタワー (複数レストラン入居)
('way/234567890', 'Tokyo Opera City Tower', 'commercial', 54, 'steel_concrete', 'commercial',
JSON_ARRAY(JSON_ARRAY(
    JSON_ARRAY(139.6860, 35.6830),
    JSON_ARRAY(139.6870, 35.6830),
    JSON_ARRAY(139.6870, 35.6842),
    JSON_ARRAY(139.6860, 35.6842),
    JSON_ARRAY(139.6860, 35.6830)
))),

-- 永楽の建物
('way/345678901', 'Eiraku Building', 'commercial', 3, NULL, 'commercial',
JSON_ARRAY(JSON_ARRAY(
    JSON_ARRAY(139.6870, 35.6820),
    JSON_ARRAY(139.6880, 35.6820),
    JSON_ARRAY(139.6880, 35.6830),
    JSON_ARRAY(139.6870, 35.6830),
    JSON_ARRAY(139.6870, 35.6820)
))),

-- 従来のモックデータ（後方互換性のため保持）
('way/123456', 'Tokyo Ramen Building', 'residential', NULL, NULL, NULL,
JSON_ARRAY(JSON_ARRAY(
    JSON_ARRAY(139.6503, 35.6762),
    JSON_ARRAY(139.6505, 35.6762),
    JSON_ARRAY(139.6505, 35.6764),
    JSON_ARRAY(139.6503, 35.6764),
    JSON_ARRAY(139.6503, 35.6762)
))),

('way/789012', 'Sushi Zen Building', 'commercial', NULL, NULL, NULL,
JSON_ARRAY(JSON_ARRAY(
    JSON_ARRAY(139.6510, 35.6765),
    JSON_ARRAY(139.6512, 35.6765),
    JSON_ARRAY(139.6512, 35.6767),
    JSON_ARRAY(139.6510, 35.6767),
    JSON_ARRAY(139.6510, 35.6765)
)));