# レストラン検索アプリ - バックエンドAPI

## セットアップ手順

### 1. 依存関係インストール
```bash
cd backend
npm install
```

### 2. 環境設定
`.env` ファイルでデータベース接続情報を設定:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=restaurant_search_app
PORT=3000
```

### 3. データベース準備
Heidi SQLで以下を確認:
- `restaurant_search_app` データベースが存在
- `restaurants` テーブルにデータが投入済み
- `osm_buildings` テーブルにデータが投入済み

### 4. サーバー起動
```bash
npm start
```

または開発モード（自動再起動）:
```bash
npm run dev
```

## API エンドポイント

### POST `/api/search`
最寄りレストラン検索（建物ポリゴン付き）

**リクエスト:**
```json
{
  "lat": 35.682179,
  "lng": 139.68194
}
```

**レスポンス:**
```json
{
  "restaurant": {
    "id": "rest_001",
    "name": "アジアンパーム渋谷本町",
    "address": "東京都渋谷区本町2-14-4",
    "openingHours": "11:30 - 14:30, 17:00 - 23:00",
    "rating": 4.0,
    "lat": 35.682179,
    "lng": 139.68194,
    "osmBuildingId": "way/1081064846"
  },
  "buildingPolygon": { /* GeoJSON Feature */ },
  "message": "アジアンパーム渋谷本町が見つかりました"
}
```

### POST `/api/search/optimized`
最寄りレストラン検索（OSM ID のみ）

**リクエスト:**
```json
{
  "lat": 35.683600,
  "lng": 139.686500
}
```

### GET `/api/restaurants`
全レストラン一覧取得

### GET `/health`
ヘルスチェック

## データベーススキーマ

### restaurants テーブル
- `id`: VARCHAR(50) PRIMARY KEY
- `name`: VARCHAR(200) NOT NULL
- `address`: TEXT NOT NULL
- `opening_hours`: VARCHAR(100) NOT NULL
- `rating`: DECIMAL(3,1) NOT NULL
- `lat`: DECIMAL(10,7) NOT NULL
- `lng`: DECIMAL(11,7) NOT NULL
- `osm_building_id`: VARCHAR(50)
- `created_at`: TIMESTAMP
- `updated_at`: TIMESTAMP

### osm_buildings テーブル
- `osm_id`: VARCHAR(50) PRIMARY KEY
- `name`: VARCHAR(200)
- `building_type`: VARCHAR(50)
- `building_levels`: INT
- `building_material`: VARCHAR(50)
- `building_use`: VARCHAR(50)
- `geometry_coordinates`: TEXT (JSON形式)
- `created_at`: TIMESTAMP
- `updated_at`: TIMESTAMP