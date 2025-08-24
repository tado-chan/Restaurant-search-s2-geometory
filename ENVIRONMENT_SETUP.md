# 環境設定ガイド

## Google Maps API Key の設定

セキュリティのため、Google Maps API Keyは環境設定ファイルで管理します。

### 1. ローカル開発環境の設定

1. `src/environments/environment.local.ts` ファイルを編集
2. `ENTER_YOUR_GOOGLE_MAPS_API_KEY_HERE` を実際のAPIキーに置換

```typescript
export const environment = {
  production: false,
  googleMapsApiKey: 'YOUR_ACTUAL_API_KEY_HERE',
  apiBaseUrl: 'http://localhost:8000'
};
```

### 2. 本番環境の設定

1. `src/environments/environment.prod.ts` ファイルを編集
2. `YOUR_GOOGLE_MAPS_API_KEY_HERE` を実際のAPIキーに置換

### ⚠️ セキュリティ注意事項

- **絶対にAPIキーをGitにコミットしないでください**
- `environment.local.ts` は `.gitignore` に追加済みです
- テスト用HTMLファイルにAPIキーを含めないでください
- 本番環境では環境変数を使用することを推奨します

### 3. Angular設定の更新（必要に応じて）

ローカル開発でlocal環境を使用する場合：

`angular.json` の `serve` 設定に追加：

```json
"serve": {
  "builder": "@angular-devkit/build-angular:dev-server",
  "configurations": {
    "local": {
      "fileReplacements": [
        {
          "replace": "src/environments/environment.ts",
          "with": "src/environments/environment.local.ts"
        }
      ]
    }
  }
}
```

使用方法：
```bash
ng serve --configuration=local
```