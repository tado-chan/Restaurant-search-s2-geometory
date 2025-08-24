# Heidi SQL でレストランデータベースを構築する手順

## 1. 必要なファイル
```
database/
├── restaurant_schema.sql     # テーブル作成用DDL
├── restaurant_data.sql       # レストランデータ投入
├── osm_buildings_data.sql    # OSM建物データ投入
└── README_HeidiSQL.md       # この手順書
```

## 2. Heidi SQL での実行手順

### Step 1: データベース作成・接続
1. **Heidi SQL** を起動
2. MySQL/MariaDB サーバーに接続
3. 新しいデータベースを作成:
   ```sql
   CREATE DATABASE restaurant_search_app;
   USE restaurant_search_app;
   ```

### Step 2: テーブル作成
1. **File** → **Load SQL file** で `restaurant_schema.sql` を開く
2. **F9** キーまたは **Query** → **Execute** で実行
3. 以下の2つのテーブルが作成されます:
   - `restaurants` - レストラン情報テーブル
   - `osm_buildings` - OSM建物データテーブル

### Step 3: レストランデータ投入
1. **File** → **Load SQL file** で `restaurant_data.sql` を開く
2. **F9** キーまたは **Query** → **Execute** で実行
3. 10件のレストランデータが投入されます

### Step 4: OSM建物データ投入
1. **File** → **Load SQL file** で `osm_buildings_data.sql` を開く
2. **F9** キーまたは **Query** → **Execute** で実行
3. 5件のOSM建物データが投入されます

## 3. データ確認用クエリ

### レストラン一覧表示
```sql
SELECT 
    id,
    name,
    address,
    rating,
    lat,
    lng,
    osm_building_id
FROM restaurants
ORDER BY rating DESC;
```

### 初台駅周辺レストラン検索 (1km圏内)
```sql
SELECT 
    name,
    address,
    rating,
    SQRT(POW(lat - 35.6833, 2) + POW(lng - 139.6867, 2)) * 111000 as distance_meters
FROM restaurants
WHERE SQRT(POW(lat - 35.6833, 2) + POW(lng - 139.6867, 2)) < 0.009 -- 約1km
ORDER BY distance_meters;
```

### レストランとOSM建物データの結合
```sql
SELECT 
    r.name as restaurant_name,
    r.address,
    r.rating,
    b.name as building_name,
    b.building_type,
    b.building_levels
FROM restaurants r
LEFT JOIN osm_buildings b ON r.osm_building_id = b.osm_id
ORDER BY r.rating DESC;
```

## 4. 投入されるデータ概要

### レストラン (10件)
- **アジアンパーム渋谷本町** - 実際のOSM ID使用
- **松阪牛 よし田** - 東京オペラシティ53F
- **叙々苑** - 東京オペラシティ53F
- **永楽** - 中華料理店
- **大戸屋ごはん処** - 東京オペラシティB1F
- **そじ坊** - そば専門店
- **田中そば店** - 東京オペラシティ
- **サブウェイ** - サンドイッチ店
- その他レガシーデータ2件

### OSM建物 (5件)
- **way/1081064846** - Asian Palm Building (実際のOSM ID)
- **way/234567890** - Tokyo Opera City Tower
- **way/345678901** - Eiraku Building
- その他レガシー建物データ2件

## 5. 注意事項

- **座標系**: WGS84 (GPS座標)
- **文字コード**: UTF-8
- **JSON データ**: MySQL 5.7以上またはMariaDB 10.2以上が必要
- **タイムスタンプ**: 自動的にJST時刻で記録

## 6. トラブルシューティング

### JSON関数エラーが出る場合
古いMySQL/MariaDBの場合、JSON関数が使えません:
```sql
-- JSON_ARRAYの代わりにTEXT型で格納
ALTER TABLE osm_buildings MODIFY geometry_coordinates TEXT;
```

### 文字化けする場合
```sql
-- 文字セットを確認
SHOW VARIABLES LIKE 'character_set%';

-- データベース文字セット変更
ALTER DATABASE restaurant_search_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```