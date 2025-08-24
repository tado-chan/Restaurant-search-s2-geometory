# Django + SQLAlchemy レストラン検索API

## アーキテクチャ

```
backend_django/
├── restaurant_search/          # Django プロジェクト設定
│   ├── settings.py            # Django設定
│   ├── urls.py               # メインURL設定
│   └── wsgi.py              # WSGI設定
├── restaurants/               # レストランアプリ
│   ├── models.py             # SQLAlchemyモデル層
│   ├── repositories.py       # Repository層 (データアクセス)
│   ├── services.py           # Service層 (ビジネスロジック)
│   ├── views.py              # Views層 (API エンドポイント)
│   └── urls.py               # アプリURL設定
├── requirements.txt           # Python依存関係
├── manage.py                 # Django管理コマンド
└── .env                      # 環境変数
```

## セットアップ

### 1. 仮想環境作成・有効化
```bash
cd backend_django
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. 依存関係インストール
```bash
pip install -r requirements.txt
```

### 3. 環境変数設定
`.env` ファイルを編集:
```env
DB_PASSWORD=your_mysql_password
```

### 4. サーバー起動
```bash
python manage.py runserver 8000
```

## API エンドポイント

### 🔍 レストラン検索
- **POST** `/api/search/` - 最寄りレストラン検索（建物ポリゴン付き）
- **POST** `/api/search/optimized/` - OSM ID最適化検索
- **POST** `/api/search/location/` - 範囲指定検索

### 📋 レストラン情報
- **GET** `/api/restaurants/` - 全レストラン一覧
- **GET** `/api/restaurants/{id}/` - レストラン詳細

### 🏢 OSM建物データ
- **GET** `/api/buildings/` - 全建物一覧
- **GET** `/api/buildings/{osm_id}/` - 建物詳細

### ⚕️ システム
- **GET** `/api/health/` - ヘルスチェック

## レイヤー構成

### 1. Models層 (`models.py`)
- **Restaurant**: レストランデータモデル
- **OSMBuilding**: OSM建物データモデル  
- SQLAlchemy ORM使用

### 2. Repository層 (`repositories.py`)
- **RestaurantRepository**: レストランデータアクセス
- **OSMBuildingRepository**: OSM建物データアクセス
- **RestaurantSearchRepository**: 複合検索用

### 3. Service層 (`services.py`)
- **RestaurantSearchService**: 検索ビジネスロジック
- **OSMBuildingService**: 建物データロジック
- **ValidationService**: 入力値検証

### 4. Views層 (`views.py`)
- Django REST Framework使用
- エラーハンドリング
- レスポンス統一

## 技術スタック

- **Django 4.2** - Webフレームワーク
- **SQLAlchemy 2.0** - ORM
- **PyMySQL** - MySQLドライバー
- **Django REST Framework** - API構築
- **django-cors-headers** - CORS対応

## データベース

既存のHeidi SQLデータベースを使用:
- `restaurants` テーブル - レストラン情報
- `osm_buildings` テーブル - OSM建物データ

## ログ・エラーハンドリング

- **バリデーション**: 座標・半径の妥当性チェック
- **ログ出力**: エラー詳細をログに記録
- **統一レスポンス**: 成功/エラー共に統一形式