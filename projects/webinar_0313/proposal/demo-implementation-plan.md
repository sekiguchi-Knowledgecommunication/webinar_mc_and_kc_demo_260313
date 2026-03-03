# ウェビナーデモ実装方針 — Databricks Apps による在庫管理デモ

## 概要

マクニカ共催ウェビナー（2026.03.13）のデモシナリオ（5シーン・約18分）を **Databricks Apps** 上で実装する。App は「デモ操作のハブ（統合UI）」として Scene 1・2 をカバーし、**Scene 3（Genie）と Scene 4（Research Agent）は Databricks ネイティブ UI** を使用する。

---

## 1. フレームワーク選定

### 比較分析

| 評価軸 | Streamlit | **Dash + Mantine** | Gradio | React + Python |
|:---|:---|:---|:---|:---|
| **モダン UI** | ⭐⭐ 制約多い | ⭐⭐⭐⭐⭐ | ⭐⭐ AI特化 | ⭐⭐⭐⭐⭐ |
| **実装工数** | ⭐⭐⭐⭐⭐ 最小 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ 最大 |
| **レイアウト自由度** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Plotly 統合** | 別途 import | ネイティブ | 弱い | 別途実装 |
| **Databricks 対応** | テンプレあり | プリインストール済 | プリインストール済 | Node.js 別管理 |
| **カスタム CSS** | 制約あり | 完全自由 | 制約あり | 完全自由 |

### 推奨: **Dash + dash-mantine-components (DMC)**

**推奨理由**:
1. **モダン UI が標準搭載**: DMC (Mantine React) でグラスモーフィズム、カードUI、ダークモード等がコンポーネント1行で実現可能
2. **Plotly ネイティブ**: チャート描画が最も美しく、追加ライブラリ不要
3. **フル CSS 制御**: ウェビナーの「WOW」な第一印象を確実に実現
4. **プリインストール済み**: Databricks Apps に `dash 2.18.1` + `dash-mantine-components 0.14.4` + `plotly 5.24.1` が標準搭載 → 依存管理の手間がほぼゼロ
5. **Python のみ**: Node.js ビルドステップ不要、Databricks SDK/SQL Connector と直接連携
6. **Streamlit 比 +20% の工数でUI品質は 2倍以上**: デモの訴求力を考えると十分なROI

---

## 2. 技術構成の全体像

```
┌─────────────────────────────────────────────────────────────┐
│                   Databricks Workspace                       │
│                                                             │
│  ┌──────────────────┐   ┌──────────────┐  ┌──────────────┐ │
│  │ Databricks App   │   │ Genie Space  │  │ Research     │ │
│  │ (Dash + DMC)     │   │ 「在庫分析    │  │ Agent        │ │
│  │                  │   │ アシスタント」 │  │ (Notebook)   │ │
│  │ ■ Scene 1: 概要  │   │              │  │              │ │
│  │ ■ Scene 2: 可視化│   │ ■ Scene 3    │  │ ■ Scene 4    │ │
│  │ ■ Scene 5: CTA  │   │  ネイティブUI │  │  ネイティブUI │ │
│  └────────┬─────────┘   └──────┬───────┘  └──────┬───────┘ │
│           │                    │                  │         │
│           ▼                    ▼                  ▼         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Unity Catalog: prod_manufacturing                   │   │
│  │  ├── bronze/ (raw_orders, raw_inventory, ...)        │   │
│  │  ├── silver/ (orders, inventory, ...)                │   │
│  │  └── gold/   (inventory_summary, turnover, alert)    │   │
│  └──────────────────────────────────────────────────────┘   │
│           ▲                                                 │
│  ┌────────┴────────┐  ┌──────────────────┐                 │
│  │ DLT Pipeline    │  │ DBSQL Dashboard  │                 │
│  │ Bronze→Silver   │  │「在庫管理統合」   │                 │
│  │ →Gold           │  └──────────────────┘                 │
│  └─────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. シーン↔コンポーネント対応表

| Scene | 担当 | 技術要素 | 概要 |
|:---|:---|:---|:---|
| **Scene 1** (3min) | Databricks App | Dash + DMC + Plotly | パイプライン概要・Medallion図解・テーブル統計 |
| **Scene 2** (3min) | Databricks App | Dash + DMC + Plotly | 在庫ダッシュボード（5チャート）をApp内描画 |
| **Scene 3** (5min) | **ネイティブ UI** | Genie Space | 自然言語質問（Genie を直接操作） |
| **Scene 4** (5min) | **ネイティブ UI** | Notebook / Agent | リサーチエージェントの分析プロセスを実演 |
| **Scene 5** (2min) | Databricks App | Dash + DMC | まとめ・CTA・次のステップ |

---

## 4. ファイル構成

```
inventory-demo-app/
├── app.yaml                     # Databricks Apps 実行構成
├── requirements.txt             # 追加 Python 依存関係
├── app.py                       # メインエントリポイント（Dash）
├── pages/                       # マルチページ構成
│   ├── pipeline.py              # Scene 1: パイプライン概要
│   ├── dashboard.py             # Scene 2: 在庫ダッシュボード
│   └── summary.py               # Scene 5: まとめ + CTA
├── components/                  # 再利用可能 UI コンポーネント
│   ├── header.py                # ヘッダー・ナビゲーション
│   ├── kpi_card.py              # KPI メトリクスカード
│   ├── medallion_diagram.py     # Medallion Architecture 図解
│   └── chart_factory.py         # Plotly チャート生成
├── utils/
│   ├── db_connector.py          # Databricks SQL 接続
│   └── data_queries.py          # クエリ定義
├── assets/
│   ├── custom.css               # カスタム CSS（グラスモーフィズム等）
│   └── logo.png                 # ロゴ
└── data/
    └── generate_sample_data.py  # サンプルデータ生成スクリプト
```

---

## 5. 主要実装の詳細

### 5a. Dash アプリ（エントリポイント）

```python
import dash
from dash import Dash, html, dcc, page_container
import dash_mantine_components as dmc

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
)

# ダークモード対応のモダンレイアウト
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark", "primaryColor": "blue"},
    children=[
        dmc.AppShell(
            header=dmc.Header(height=60, children=[...]),  # ナビゲーション
            children=[page_container],
        )
    ],
)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("DATABRICKS_APP_PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)
```

### 5b. Scene 2 ダッシュボード（5パネル）

| # | パネル名 | 可視化タイプ | Plotly コンポーネント |
|:---|:---|:---|:---|
| 1 | 在庫総額推移 | 折れ線 | `go.Scatter` (area fill) |
| 2 | カテゴリ別構成 | ツリーマップ | `px.treemap` |
| 3 | 過剰在庫アラート | テーブル | DMC `Table` + 条件付きバッジ |
| 4 | 発注 vs 需要 | バブルチャート | `px.scatter` (size param) |
| 5 | リードタイム | 棒グラフ | `px.bar` (horizontal) |

### 5c. サンプルデータ（5テーブル）

| テーブル | 件数 | データ設計のポイント |
|:---|:---|:---|
| `raw_orders` | 10,000 | 過去12ヶ月の発注データ |
| `raw_inventory` | 50,000 | 品目×拠点×日のスナップショット |
| `raw_receipts` | 8,000 | 入荷実績データ |
| `raw_demand` | 5,000 | 予測 vs 実績（カテゴリBで乖離大） |
| `item_master` | 500 | 品目マスタ（カテゴリA〜D） |

**注意**: カテゴリB（電子部品）に過剰在庫を意図的に集中させ、デモストーリー（Scene 4 のエージェント分析結果）と整合させる。

### 5d. DLT パイプライン

Bronze（生取り込み）→ Silver（品質検証・正規化）→ Gold（ビジネス集約）の3段階。Expectations で品質チェックを実装。

### 5e. Genie Space（ネイティブ UI）

- 「在庫分析アシスタント」を Gold テーブルに接続
- 事前テスト済み質問4つを準備

---

## 6. 設定ファイル

### app.yaml
```yaml
command:
  - python
  - app.py
env:
  - name: DATABRICKS_WAREHOUSE_ID
    valueFrom: warehouse-id
  - name: CATALOG_NAME
    value: prod_manufacturing
```

### requirements.txt
```
# dash, plotly, dash-mantine-components はプリインストール済みのため不要
# 以下は追加で必要なもののみ
databricks-sql-connector>=3.0.0
pandas>=2.0.0
```

---

## 7. 実装の優先順位と工数

| 優先度 | コンポーネント | 工数 | 自動生成可能 |
|:---|:---|:---|:---|
| 🔴 P0 | サンプルデータ生成スクリプト | 1.5h | ✅ AI で生成 |
| 🔴 P0 | Unity Catalog + テーブル作成 | 1h | ✅ SQL スクリプト |
| 🔴 P0 | DLT パイプラインノートブック | 2h | ✅ テンプレート活用 |
| 🟡 P1 | Dash App — Scene 1 (パイプライン概要) | 2h | ✅ AI で生成 |
| 🟡 P1 | Dash App — Scene 2 (ダッシュボード) | 3h | ✅ AI で生成 |
| 🟡 P1 | Dash App — Scene 5 (まとめ+CTA) | 1h | ✅ AI で生成 |
| 🟡 P1 | Genie Space 設定 + 質問テスト | 1.5h | 手動設定 |
| 🟡 P1 | カスタム CSS / テーマ調整 | 1h | ✅ AI で生成 |
| 🟢 P2 | リサーチエージェント Notebook | 2h | ✅ AI で生成 |
| 🟢 P2 | デプロイ + リハーサル | 1.5h | 手動 |
| | **合計** | **約17h** | |

> 当初見積の26hから **約35%圧縮**。AI によるコード生成で Dash コンポーネント・データ生成・CSS を高速に実装。

---

## 8. リスク対策

| リスク | 対策 |
|:---|:---|
| Genie の回答不安定 | 事前テスト済み質問セット + 録画バックアップ |
| App 起動遅延 | デモ前にアプリ起動済みにしておく |
| DLT エラー | パイプライン事前実行完了状態を維持 |
| ネットワーク障害 | 全シーンのスクリーンショット/録画バックアップ |
| エージェント実行時間超過 | 事前実行済み結果を用意 |

---

## 9. デプロイ手順

```bash
# 1. ローカル開発・テスト
cd inventory-demo-app
pip install -r requirements.txt
python app.py   # → http://localhost:8050

# 2. Databricks CLI でデプロイ
databricks apps deploy inventory-demo --source-code-path ./inventory-demo-app

# 3. または Git リポジトリ経由デプロイ（推奨）
git push origin main
# → Databricks UI で Git ソースを指定してデプロイ
```

---

## 10. 検証計画

### 自動検証
- ローカルでの Dash アプリ起動確認（全ページ遷移テスト）
- サンプルデータ生成スクリプトの dry-run

### 手動検証（Databricks ワークスペース）
- Unity Catalog テーブル存在確認
- DLT パイプライン正常完了
- DBSQL 経由の Gold テーブルクエリ動作
- Genie 質問 4 つの回答品質確認
- Databricks App URL アクセス → 全ページ表示確認
- デモリハーサル 2 回以上
