# Databricks AI/BI ダッシュボード構築ガイド

本ドキュメントは、Databricks AI/BI ダッシュボード（Lakeview Dashboard）の作成～デプロイまでの
知見を、今回のウェビナーデモ構築を通じて体系的にまとめたものです。

---

## 目次

1. [概要](#概要)
2. [アーキテクチャ](#アーキテクチャ)
3. [.lvdash.json の構造](#lvdashjson-の構造)
4. [デプロイ方法](#デプロイ方法)
5. [トラブルシューティング（実例付き）](#トラブルシューティング実例付き)
6. [ベストプラクティス](#ベストプラクティス)

---

## 概要

Databricks AI/BI ダッシュボード（Lakeview Dashboard）は、Unity Catalog のテーブルに対して
SQL ベースのデータセットを定義し、KPI カウンター・チャート・テーブルなどのウィジェットで
可視化するダッシュボード機能です。

### 特徴

- **Serverless 実行**: SQL ウェアハウスを自動でプロビジョニング
- **AI 支援**: 自然言語でのビジュアライゼーション生成提案
- **JSON 定義**: `.lvdash.json` ファイルでバージョン管理可能
- **REST API**: プログラマティカルなデプロイをサポート

---

## アーキテクチャ

```
┌─────────────────────────────────────────────────────────┐
│  Databricks Workspace                                    │
│                                                          │
│  ┌──────────────┐    ┌──────────────┐                    │
│  │ Unity Catalog │    │ Lakeview API │                    │
│  │ (テーブル)    │◄───│ /api/2.0/    │                    │
│  │              │    │ lakeview/    │                    │
│  │ Gold Tables: │    │ dashboards   │                    │
│  │ - inventory  │    └──────┬───────┘                    │
│  │   _summary   │           │                            │
│  │ - turnover   │    ┌──────▼───────┐                    │
│  │   _analysis  │    │  Dashboard   │                    │
│  │ - overstock  │    │  (Lakeview)  │                    │
│  │   _alert     │    │              │                    │
│  └──────────────┘    │ datasets[]   │                    │
│                      │ pages[]      │                    │
│  ローカル             │   widgets[]  │                    │
│  ┌──────────────┐    └──────────────┘                    │
│  │ .lvdash.json │──── serialized_dashboard として POST ──┘
│  │ (定義ファイル) │
│  └──────────────┘
```

---

## .lvdash.json の構造

### トップレベル

```json
{
  "pages": [],     // ページ定義（通常1ページ）
  "datasets": []   // SQL データセット定義
}
```

### データセットの設計

データセットは SQL クエリを定義する。**必ず三層名（catalog.schema.table）** を使う。

```json
{
  "name": "inventory_kpi",
  "displayName": "在庫KPI",
  "query": "SELECT SUM(avg_inventory_value) as total_value FROM catalog.schema.inventory_summary WHERE ..."
}
```

### ウィジェットの設計

ウィジェットは `widget` と `position` のペアで定義する。

**重要な紐付けルール:**

```
datasets[].name ←──── widget.queries[].query.datasetName   (★一致必要)
widget.queries[].query.fields[].name ←──── widget.spec.encodings.*.fieldName   (★一致必要)
```

### 6カラムグリッド

```
  x=0   x=1   x=2   x=3   x=4   x=5
 ┌─────┬─────┬─────┬─────┬─────┬─────┐
 │ KPI1 (w=2)│ KPI2 (w=2)│ KPI3 (w=2)│  y=0, h=2
 ├───────────┼───────────┼───────────┤
 │ Chart1    │           │ Chart2    │  y=2, h=4
 │  (w=3)    │           │  (w=3)    │
 ├───────────┴───────────┴───────────┤
 │         Table (w=6, 全幅)         │  y=6, h=4
 └───────────────────────────────────┘
```

---

## デプロイ方法

### ✅ Lakeview REST API（推奨）

```bash
# Python で .lvdash.json → 内部形式変換 + API ペイロード生成
python3 << 'PYEOF'
import json
with open("dashboard.lvdash.json") as f:
    dashboard = json.load(f)

# query → queryLines 変換（★必須）
for ds in dashboard.get("datasets", []):
    if "query" in ds:
        lines = ds["query"].split("\n")
        ds["queryLines"] = [line + "\n" for line in lines[:-1]] + [lines[-1]]
        del ds["query"]
for page in dashboard.get("pages", []):
    page["pageType"] = "PAGE_TYPE_CANVAS"
dashboard["uiSettings"] = {
    "theme": {"widgetHeaderAlignment": "ALIGNMENT_UNSPECIFIED"},
    "applyModeEnabled": False
}

payload = {
    "display_name": "ダッシュボード名",
    "serialized_dashboard": json.dumps(dashboard, ensure_ascii=False),
    "parent_path": "/Users/user@example.com"
}
with open("/tmp/payload.json", "w") as out:
    json.dump(payload, out, ensure_ascii=False)
PYEOF

# 作成
databricks api post /api/2.0/lakeview/dashboards --json @/tmp/payload.json

# 更新（既存ダッシュボード）
databricks api patch /api/2.0/lakeview/dashboards/$DASHBOARD_ID --json @/tmp/payload.json
```

### ❗ Visualization 反映の鋵（確定知見）

**API で Visualization は完全反映可能。** ただし、`fields[].name` と `encodings.fieldName` の命名規則が重要：

| `fields[].name` | `fields[].expression` | `encodings.fieldName` |
|:---|:---|:---|
| `category` | `` `category` `` | `category` |
| `sum(total_value)` | `SUM(\`total_value\`)` | `sum(total_value)` |
| `monthly(month)` | `DATE_TRUNC("MONTH", \`month\`)` | `monthly(month)` |

その他のルール：
- `queries[].name` → **`"main_query"` に統一**
- `disaggregated` → **`false`**（テーブルのみ `true`）
- `encodings` の `displayName` → **設定しない**（UI が自動付与）

---

## トラブルシューティング（実例付き）

### 1. UNRESOLVED_COLUMN エラー

**症状**: `A column, variable, or function parameter with name 'turnover_rate' cannot be resolved.`

**原因**: DLTパイプラインで `alias()` によりカラム名が変わっている。

```python
# DLT パイプライン側
spark_avg("turnover_rate").alias("avg_turnover_rate")  # ← 出力カラム名は avg_turnover_rate
```

```sql
-- Dashboard SQL（❌ 誤り）
SELECT AVG(turnover_rate) FROM turnover_analysis

-- Dashboard SQL（✅ 正しい）
SELECT AVG(avg_turnover_rate) FROM turnover_analysis
```

**対策**: `DESCRIBE TABLE catalog.schema.table` で実カラム名を確認してからSQLを書く。

### 2. 「Select fields to visualize」と表示される

**症状**: ウィジェットに「Select fields to visualize.」と表示され、チャートが描画されない。

**原因**: `fields[].name` の命名形式が間違っている。

**対策**:
- 集約フィールドの `name` に集約関数を含める（例: `sum(total_value)`）
- 時系列フィールドは `DATE_TRUNC` 形式を使用（例: `monthly(month)` + `DATE_TRUNC("MONTH", \`month\`)`）
- `encodings.fieldName` が `fields.name` と完全一致しているか確認
- `disaggregated: false`（テーブル以外）になっているか確認

### 3. テーブルエイリアスで UNRESOLVED_COLUMN

**症状**: `A column with name 'ta'.'item_id' cannot be resolved.`

**原因**: テーブルエイリアス付きのカラム参照が解決できない。

```sql
-- ❌ エイリアス参照でエラー
SELECT ta.item_id FROM catalog.schema.turnover_analysis ta

-- ✅ 直接参照で解決
SELECT item_id FROM catalog.schema.turnover_analysis
```

### 4. You must use serverless compute

**症状**: DLT パイプラインやダッシュボード作成時に `You must use serverless compute` エラー。

**対策**: パイプライン定義JSONに `"serverless": true` を追加。

### 5. Metastore storage root URL does not exist

**症状**: CLI からカタログを新規作成しようとするとエラー。

**原因**: Free Edition 等では CLI からのカタログ作成が制限されている。

**対策**: Databricks UI から手動でカタログ/スキーマ/Volumeを作成する。

---

## ベストプラクティス

### SQL 設計

1. **三層名を必ず使用**: `catalog.schema.table`（相対参照は環境依存）
2. **集約はSQL側で行う**: ウィジェットの`expression`はシンプルに保つ
3. **LIMIT を活用**: テーブルウィジェットは `LIMIT 20` 等で制限
4. **サブクエリで最新日付を動的取得**: `WHERE month = (SELECT MAX(month) FROM ...)`

### デプロイ

1. **Lakeview REST API を使用**: `query` → `queryLines` 変換 + `pageType`/`uiSettings` 追加
2. **ダッシュボード定義はGit管理**: `.lvdash.json` をリポジトリに入れる
3. **デプロイスクリプトを用意**: 繰り返し実行可能なシェルスクリプト化
4. **`fields.name` の命名規則を守る**: 集約関数を含む形式（`sum(col)`）で Visualization が API で完全反映される

### テーブル設計（DLT側）

1. **カラム名を明示的にする**: `alias()` で意味のある名前をつける
2. **ダッシュボードを意識した集約**: Gold テーブルはダッシュボードの要件に合わせて設計
3. **テーブルコメントを付ける**: Genie Space でも活用できる
