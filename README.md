# Restaurant Search App

OpenStreetMapの建物ポリゴンを使用したレストラン検索アプリケーション

## 機能

- 地図タップによるレストラン検索
- OSM建物データによる正確な建物形状表示
- 最適化モード（OSM ID使用）による高速処理
- Angular + Ionic + Google Maps API構成

## セットアップ

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd restaurant-search-app
```

### 2. 依存関係のインストール

```bash
npm install
```

### 3. Google Maps API Keyの設定

1. [Google Cloud Console](https://console.cloud.google.com/)でGoogle Maps APIキーを取得
2. `src/environments/environment.ts`を編集：

```typescript
export const environment = {
  production: false,
  googleMapsApiKey: 'YOUR_ACTUAL_API_KEY_HERE', // ここに実際のAPIキーを入力
  apiBaseUrl: 'http://localhost:8000'
};
```

⚠️ **重要**: `environment.ts`は`.gitignore`で保護されているため、APIキーがGitにコミットされることはありません。

### 4. アプリケーションの起動

```bash
npm start
```

または

```bash
npm run dev
```

アプリケーションは `http://localhost:8100` で起動します。

### 5. バックエンド（オプション）

バックエンドは現在開発中です。現時点ではフロントエンドのモックデータで動作します。

## 使用方法

1. アプリを起動
2. 地図上をタップ
3. レストラン情報と建物ポリゴン（薄い青色）が表示
4. 画面右上の「OSM最適化」ボタンで処理モードを切り替え可能

## 技術スタック

- **フロントエンド**: Angular 17 + Ionic 7
- **地図**: Google Maps JavaScript API
- **データ**: OpenStreetMap (OSM)
- **状態管理**: Angular Signals
- **スタイル**: SCSS

## プロジェクト構成

```
src/
├── app/
│   └── map/           # 地図ページコンポーネント
├── services/
│   ├── api.service.ts # API通信サービス
│   └── map.service.ts # 地図操作サービス
├── store/
│   └── restaurant.store.ts # 状態管理
├── models/
│   └── restaurant.ts  # データ型定義
└── environments/
    └── environment.ts # 環境設定（Git管理外）
```

## 開発コマンド

```bash
# 開発サーバー起動
npm start

# ビルド
npm run build

# Angular CLI サーバー
npm run serve
```

## トラブルシューティング

### Google Maps が表示されない場合

1. APIキーが正しく設定されているか確認
2. Google Maps JavaScript APIが有効化されているか確認
3. ブラウザの開発者ツールでエラーをチェック

### 依存関係エラーの場合

```bash
rm -rf node_modules package-lock.json
npm install
```