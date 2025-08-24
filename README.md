# Restaurant Search App

**初台駅周辺1km圏内のレストラン検索アプリ**  
OpenStreetMap建物データとMySQLデータベースを連携した地図検索システム

![アプリケーション画面](images/app_screenshot.png)
*▲ 実際のアプリケーション動作画面 - 地図タップでレストラン検索・建物ポリゴン表示*

## 主な機能

- 🗺️ **リアルタイム地図検索** - 地図タップで最寄りレストランを自動検索
- 🏢 **OSM建物ポリゴン表示** - 実際の建物形状を薄い青色で表示
- 🍽️ **初台駅周辺レストランDB** - 8軒の実在レストランデータを収録
- ⚡ **2つの検索モード** - 従来モード vs OSM ID最適化モード
- 💾 **MySQL連携** - Heidi SQLで管理するリアルデータベース
- 📱 **レスポンシブ対応** - Angular + Ionic による現代的UI

## セットアップ手順

### 🗄️ 1. データベース構築（Heidi SQL）

#### データベース作成
```sql
CREATE DATABASE restaurant_search_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE restaurant_search_app;
```

#### テーブル作成 & データ投入
1. `database/restaurant_schema.sql` を実行（テーブル作成）
2. `database/restaurant_data.sql` を実行（レストランデータ投入）
3. `database/osm_buildings_data.sql` を実行（OSM建物データ投入）

**収録レストラン**:
- アジアンパーム渋谷本町（OSM ID: `way/1081064846`）
- 松阪牛 よし田（東京オペラシティ53F）
- 叙々苑（東京オペラシティ53店）
- 永楽（中華料理店）
- 大戸屋ごはん処、そじ坊、田中そば店、サブウェイ

### 💻 2. バックエンドAPI起動

```bash
cd backend_django

# 仮想環境作成・有効化
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install -r requirements.txt

# .env ファイル編集（MySQLパスワード設定）
# DB_PASSWORD=your_mysql_password

python manage.py runserver 8000  # http://localhost:8000
```

### 🌐 3. フロントエンド起動

```bash
# プロジェクトルートで
npm install
npm start  # http://localhost:4200
```

### 🗝️ 4. Google Maps API Key設定

`src/environments/environment.ts`:
```typescript
export const environment = {
  production: false,
  googleMapsApiKey: 'YOUR_GOOGLE_MAPS_API_KEY',
  apiBaseUrl: 'http://localhost:8000/api'
};
```

## 🎯 使用方法

### 基本操作
1. **地図をタップ** - 初台駅周辺の地図上任意の場所をクリック
2. **レストラン自動検索** - 最寄りのレストランが自動的に検索・表示
3. **建物ポリゴン表示** - 該当レストランの建物が薄い青色で描画
4. **詳細情報確認** - 店名、住所、営業時間、評価を確認

### 高度な機能
- **🔄 最適化モード切替** - 画面右上ボタンでOSM ID最適化モード on/off
- **📍 正確な建物形状** - OpenStreetMapの実際の建物座標を使用
- **🔍 最近接検索** - クリック地点から最も近いレストランを検索

## 🛠️ 技術スタック

### フロントエンド
- **Angular 17** - TypeScript ベースモダンフレームワーク
- **Ionic 7** - モバイルファーストUIコンポーネント
- **Google Maps JavaScript API** - 地図表示・操作
- **Angular Signals** - リアクティブ状態管理

### バックエンド
- **Django 4.2** - Python Webフレームワーク
- **SQLAlchemy 2.0** - ORM (Object-Relational Mapping)
- **Django REST Framework** - RESTful API構築
- **MySQL 8.0** - レストラン・OSM建物データ保存
- **PyMySQL** - MySQLドライバー

### データソース
- **OpenStreetMap (OSM)** - 建物形状・OSM ID
- **実地調査データ** - レストラン情報・座標

## 📁 プロジェクト構成

```
restaurant-search-app/
├── 📁 src/                          # フロントエンド
│   ├── 📁 app/map/                 # 地図ページコンポーネント
│   ├── 📁 services/
│   │   ├── api.service.ts         # データベースAPI通信
│   │   └── map.service.ts         # Google Maps操作・OSM描画
│   ├── 📁 store/
│   │   └── restaurant.store.ts    # Angular Signals 状態管理
│   ├── 📁 models/
│   │   └── restaurant.ts          # TypeScript型定義
│   └── 📁 environments/
│       └── environment.ts         # 環境設定（Git管理外）
├── 📁 backend_django/               # バックエンドAPI
│   ├── restaurant_search/         # Django プロジェクト
│   ├── restaurants/               # レストランアプリ
│   │   ├── models.py             # SQLAlchemyモデル
│   │   ├── repositories.py       # Repository層
│   │   ├── services.py           # Service層
│   │   ├── views.py              # Views層（API）
│   │   └── urls.py               # URL設定
│   ├── requirements.txt          # Python依存関係
│   └── .env                      # 環境変数
└── 📁 database/                     # SQL ファイル
    ├── restaurant_schema.sql      # テーブル作成DDL
    ├── restaurant_data.sql        # レストランデータ
    ├── osm_buildings_data.sql     # OSM建物データ
    └── README_HeidiSQL.md         # Heidi SQL手順書
```

## ⚙️ API エンドポイント

- **POST** `/api/search` - 最寄りレストラン検索（建物ポリゴン付き）
- **POST** `/api/search/optimized` - OSM ID最適化検索
- **GET** `/api/restaurants` - 全レストラン一覧
- **GET** `/health` - APIヘルスチェック

## 🔧 開発コマンド

### フロントエンド
```bash
npm start          # 開発サーバー起動 (http://localhost:4200)
npm run build      # プロダクションビルド
ng serve           # Angular CLI直接実行
```

### バックエンド
```bash
cd backend_django
python manage.py runserver 8000  # APIサーバー起動 (http://localhost:8000)
python manage.py runserver        # デフォルトポート使用
```

## 🚨 トラブルシューティング

### 地図が表示されない
1. **Google Maps API Key** が正しく設定されているか確認
2. **Maps JavaScript API** が有効化されているか確認
3. **CORS エラー** - バックエンドAPIが起動しているか確認

### データベース接続エラー
1. **MySQL** が起動しているか確認
2. **backend/.env** のDB設定を確認
3. **Heidi SQL** でテーブル・データが存在するか確認

### 建物ポリゴンが表示されない
1. **最適化モード** が有効になっているか確認
2. **OSM ID** が正しくデータベースに保存されているか確認
3. ブラウザのコンソールでエラーログを確認

### TypeScript コンパイルエラー
```bash
rm -rf node_modules package-lock.json
npm install
ng build --aot=false  # AoT無効でビルド
```