# pptx-gen スキル — できること・品質監査レポート

**日付**: 2026-02-24
**ステータス**: v1.0.0 実装完了 / SKILL.md ドキュメント改善余地あり（19/28）

---

## pptx-gen でできること

### 基本機能

Markdown の提案書・報告書を、**ネイティブ編集可能な PowerPoint ファイル**に変換する。
テーブル・テキストボックス・図形がすべて PowerPoint オブジェクトとして生成されるため、
納品後にクライアントが直接編集できる。

### 対応レイアウト（全40パターン）

#### 特殊スライド（3種）
| ID | パターン名 | 用途 |
|:---|:---|:---|
| L-01 | Cover | 表紙（クライアント名・タイトル・日付） |
| L-02 | Closing | クロージング（会社情報・ロゴ） |
| L-21 | Section Divider | セクション区切り（紺背景・番号付き） |

#### テーブル系（6種）
| ID | パターン名 | 用途 |
|:---|:---|:---|
| L-03 | Flex Table | 汎用比較テーブル（観点×現状×課題×提案） |
| L-04 | Evaluation Table | 順位付き評価表（点線ハイライト） |
| L-05 | Detail Analysis | 検討軸×取組/リスク/軽減策 |
| L-10 | Summary Table | キーバリュー型サマリー表 |
| L-11 | Team Structure | 体制表（チーム・役職・人数） |
| L-22 | Appendix Table | 付録テーブル |

#### ビジュアル系（10種）
| ID | パターン名 | 用途 |
|:---|:---|:---|
| L-06 | Two Column | 2カラム（左カテゴリ＋右ハイライト） |
| L-07 | Comparison | Before/After 比較 |
| L-08 | Card List | 強み・特徴カード |
| L-09 | Gantt | スケジュール（ガントチャート） |
| L-13 | Agenda | 目次・アジェンダ |
| L-14 | KPI Dashboard | 2x2 KPI メトリクス |
| L-15 | Process Flow | ステップ・フェーズ横フロー |
| L-17 | Full Text | エグゼクティブサマリー |
| L-24 | Big Number | ヒーロー数値統計 |
| L-12 | Dark Reference | ダーク背景参考事例 |

#### 拡張レイアウト（21種）
| ID | パターン名 | ID | パターン名 |
|:---|:---|:---|:---|
| L-16 | Quote（引用） | L-25 | Concept Diagram（コンセプト図） |
| L-18 | Matrix 2x2 | L-26 | Before/After KPI |
| L-19 | Image + Text | L-27 | Case Study |
| L-20 | Stacked Bars | L-28 | Pricing（価格表） |
| L-23 | Pain Points（課題） | L-29 | FAQ |
| L-30 | CTA | L-31 | Logic Tree |
| L-32 | Mission/Vision | L-33 | Key Value |
| L-34 | Team Profiles | L-35 | Grid Cards |
| L-36 | Exec Summary | L-37 | KPI Achievement |
| L-38 | Strategy/Policy | L-39 | Priority Issue |
| L-40 | Roadmap | | |

### ワークフロー

```
Markdown 提案書
  ↓
Claude（分析・構成設計・メッセージライン抽出・レイアウト選定）
  ↓
slide_plan.json（中間フォーマット）
  ↓
generate_pptx.py（Python スクリプト）
  ↓
ネイティブ PPTX（全オブジェクト編集可能）
```

### 技術的特徴

| 特徴 | 詳細 |
|:---|:---|
| **ネイティブオブジェクト** | 全テキスト・テーブル・図形が PowerPoint オブジェクト。画像貼り付けではない |
| **日本語フォント** | メイリオを Latin + East Asian の両方に XML レベルで設定 |
| **KC ブランド準拠** | Navy #17406D / Blue #0F6FC6 / Sky #009DD9 のカラーシステム |
| **16:9 スライド** | 13.333" x 7.5" の標準ワイドスクリーン |
| **Layout Registry** | 新レイアウト追加が容易（1ファイル追加 + registry 登録） |
| **中間フォーマット** | slide_plan.json で Claude と Python の責務を分離 |
| **エラー耐性** | 部分失敗時も処理継続。exit code で結果を通知 |
| **ポータブル** | リポジトリ固有パスなし。スキルフォルダのコピーだけで他プロジェクトに導入可能 |

### 依存関係

```
python >= 3.10
python-pptx >= 0.6.23
lxml >= 4.9.0
```

### 他プロジェクトへの導入

```bash
# 1. スキルフォルダごとコピー
cp -r .agent/skills/pptx-gen ~/other-project/.agent/skills/

# 2. Python 依存のインストール（未導入なら）
pip install python-pptx lxml

# 3. Claude に「提案書を PPTX にして」等で発動
```

`projects/pptx-template/` は開発時の作業場（設計資料・HTML プロトタイプ等）であり、
スキルの実行には不要。

---

## できるようになったこと（Phase 0 → v1.0.0 の変遷）

### Phase 0（2026-02-20）: HTML アプローチの限界発見

- 外部スキル（slidekit-create + /pptx）を試用
- HTML → スクリーンショット → PPTX の方式では**全スライドが画像**になり編集不可
- コンサルティング納品物としては致命的と判断

### v1.0.0（2026-02-23）: python-pptx ネイティブ方式の完成

- **アーキテクチャ転換**: HTML ベース → python-pptx ネイティブ生成
- **Hybrid 方式の確立**: Claude（創造的判断）+ Python（機械的生成）の役割分担
- **40 レイアウト完全実装**: 提案書に必要なパターンを網羅
- **ブランドシステムのコード化**: brand.py に色・フォント・スペーシングを集約
- **共通部品ライブラリ**: slide_builder.py でヘッダー・フッター・罫線操作を統一
- **E2E 検証**: 9枚構成のサンプル提案書で全スライド OK 確認

### 実装規模

| カテゴリ | ファイル数 | 概算行数 |
|:---|:---|:---|
| SKILL.md | 1 | 420 |
| コアスクリプト | 3 | 650 |
| レイアウトモジュール | 40 | 3,500+ |
| **合計** | **44** | **4,570+** |

---

## skill-forge 品質監査結果（28項目チェック）

### スコアサマリー

```
A-1 ~ A-8 (Anthropic ガイド):  6/8
R-1 ~ R-6 (リポジトリ規約):    6/6
M-1 ~ M-6 (金型メトリクス):    2/6
C-1 ~ C-8 (コンテンツ品質):    5/8
合計: 19/28
```

### 不合格項目と改善方針

| # | 項目 | 現状 | 基準 | 改善方針 |
|:---|:---|:---|:---|:---|
| A-6 | Examples | 3個 | 6+ | KPI系/エラー復旧/テーブル分割 等のシナリオを追加 |
| A-7 | Troubleshooting | 6項目 | 10+ | JSON構文エラー/巨大テーブル/OS別フォント/slide_plan不整合 等を追加 |
| M-1 | 総行数 | 420行 | 450-600 | Examples/Troubleshooting 追加で自然に達成 |
| M-3 | Examples | 3個 | 6+ | A-6 と同じ |
| M-4 | Troubleshooting | 6項目 | 10-12 | A-7 と同じ |
| M-5 | references/ | 1 (画像のみ) | 3-7 | スキル内にドキュメント reference を追加 |
| C-4 | Examples 多様性 | 限定的 | 多様なシナリオ | A-6 と同じ |
| C-6 | references/ 整合 | 壊れリンクあり | 完全一致 | `brand-design-system.md` をスキル内に配置。外部参照を解消 |

### 評価

- **実装コード（scripts/）は Gold Standard** — 40レイアウト完全実装、エラーハンドリング完備、ポータブル設計
- **SKILL.md のドキュメント面に改善余地** — Examples, Troubleshooting, references/ の充実が必要
- **リポジトリ規約は完全準拠** — R 領域 6/6

### v1.1.0 で Gold Standard（28/28）に到達するための作業

1. **references/ の自己完結化**: `brand-design-system.md`（要約版）、`layout-fields-reference.md`（各レイアウトの fields 一覧）、`message-line-patterns.md`（要約版）をスキル内に作成
2. **Examples を 6+ に拡充**: 既存3 + KPI Dashboard 活用 / 大規模提案書（20枚+） / slide_plan.json の手動修正と再生成
3. **Troubleshooting を 10+ に拡充**: 既存6 + JSON パースエラー / テーブル行数超過 / macOS でのフォント代替 / slide_plan.json の fields 不足
4. 上記で総行数 450-600 行に到達

---

## 関連ファイル

| ファイル | 説明 |
|:---|:---|
| `.agent/skills/pptx-gen/SKILL.md` | スキル定義本体 |
| `.agent/skills/pptx-gen/scripts/` | Python 実行スクリプト群 |
| `.agent/skills/pptx-gen/references/KC_logo.png` | ブランドロゴ |
| `projects/pptx-template/` | 開発時の作業場（スキル実行には不要） |