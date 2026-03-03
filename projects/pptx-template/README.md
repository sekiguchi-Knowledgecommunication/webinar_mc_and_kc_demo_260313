# 案件名（Project Name）

> この README は新規案件のテンプレートです。案件情報に合わせて更新してください。

## 基本情報

| 項目 | 内容 |
|:---|:---|
| **案件名** | （案件の正式名称） |
| **顧客名** | （顧客名） |
| **担当者** | （プロジェクト担当者） |
| **ステータス** | 準備中 / 進行中 / 提出済 / 完了 |
| **作成日** | YYYY-MM-DD |
| **提出期限** | YYYY-MM-DD |

## ディレクトリ構造

```
<案件名>/
├── inbox/          # 顧客から受領した議事録・RFP・資料（Markdown化済み）
├── notes/          # 構造化仕様・ドメインモデル・用語集（SSoT）
├── proposal/       # 提案書（章立て）
├── snapshots/      # DRM アジェンダ・台本（マイルストーン記録）
│   ├── DRM1-<案件名>.md   # Phase 1: Go/No-Go 判断
│   └── DRM2-<案件名>.md   # Phase 2: 提出前レビュー
├── decision_log/   # 設計判断ログ（ADR）・DRM 判定結果
└── references/     # 外部参照・URL・PDF
```

## ワークフロー

> 詳細は `.agent/workflows/proposal-lifecycle.md` を参照。

| Phase | 工程 | スキル | 成果物 |
|:---|:---|:---|:---|
| 1 | 資料収集 | `pdf-convert` | `inbox/*.md` |
| 2 | 要件蒸留 | `design` | `notes/*.md` |
| 3 | 提案書作成 | （手動 or AI） | `proposal/*.md` |
| **4** | **DRM レビュー** | **`drm`** | **`snapshots/DRM1-*.md`, `snapshots/DRM2-*.md`** |
| 5 | 品質検証 | `verify` | Review Report |
| 6 | 提出 | — | 顧客へ提出 |

### Phase 4: DRM レビュー（提案書作成後に必ず実施）

提案書の初版完成後、以下の2つの DRM アジェンダを `snapshots/` に生成する:

1. **DRM Phase 1（Go/No-Go）**: 提案を進めるべきか否かの判断
   ```
   「drm スキルで、<案件名> のフェーズ1アジェンダを snapshots/ に生成して」
   ```

2. **DRM Phase 2（提出前レビュー）**: 「このまま出して勝てるか？」の最終確認
   ```
   「drm スキルで、<案件名> のフェーズ2アジェンダを snapshots/ に生成して」
   ```

| DRM 判定結果 | 次のアクション |
|:---|:---|
| Go | Phase 5（verify）に進む |
| 修正Go | 指摘箇所を修正し、Phase 5 に進む |
| 差し戻し | 大幅修正後、Phase 4 を再実施 |
| No-Go | 案件中止。`decision_log/` に記録 |

## メモ

（案件に関する補足事項をここに記載）
