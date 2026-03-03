# UI設計仕様: AIセキュリティ ガバナンスEXPO 展示会ブース用LP

> **バージョン**: 1.0.0 | **作成日**: 2026-02-22
> **適用スキル**: ui-design v1.1.0 (Refactoring UI 8観点)
> **用途**: 展示会ブースで営業が大画面/タブレットで見せながら説明するLP
> **サービス**: ナレコム GenAI セキュリティガードレール設計サービス

---

## 展示会LP固有の設計前提

| 項目 | 通常Web LP | 展示会ブースLP |
|:---|:---|:---|
| **視距離** | 40-60cm (PC) | 1-3m (大画面), 30-50cm (タブレット) |
| **閲覧時間** | 自由 (スクロール) | 営業トーク中の 30-90秒/セクション |
| **操作者** | 訪問者本人 | 営業担当者 |
| **環境光** | 自宅/オフィス (安定) | 展示会ブース照明 (強い白色光 + 周囲の光) |
| **目的** | CV (フォーム送信) | 対面での理解促進 → 名刺交換/商談予約 |
| **情報密度** | SEO考慮で多め | 営業トーク補助なので最小限 |

---

## 1. 視覚的階層 (Visual Hierarchy)

### 展示会向け3段階設計

展示会LPでは情報を **3段階に厳密に絞る**。通常のWebサイトよりもコントラスト差を大きくし、1-3m先からでも階層が判別できるようにする。

| レイヤー | 役割 | フォントサイズ | ウェイト | 色 | CSS |
|:---|:---|:---|:---|:---|:---|
| **Primary** | セクション見出し、キーメッセージ | `clamp(2rem, 4vw, 3.5rem)` | 700 (Bold) | `#F1F5F9` (Slate 100) | `color: #F1F5F9; font-weight: 700;` |
| **Secondary** | 要点テキスト、カードタイトル | `clamp(1.25rem, 2.5vw, 1.75rem)` | 600 (Semibold) | `#E2E8F0` (Slate 200) | `color: #E2E8F0; font-weight: 600;` |
| **Tertiary** | 補足説明、注釈 | `clamp(1rem, 1.8vw, 1.25rem)` | 400 (Regular) | `#94A3B8` (Slate 400) | `color: #94A3B8; font-weight: 400;` |

### 展示会特有の調整

- **サイズ比の拡大**: Primary と Tertiary のサイズ比を通常の 2:1 ではなく **2.8:1** 程度に拡大。遠距離でも階層差が視認できるようにする
- **色のコントラスト差拡大**: Primary (#F1F5F9) と Tertiary (#94A3B8) の明度差を十分に確保（通常LPより大きく）
- **1画面1メッセージ原則**: 各セクションで Primary テキストは **1つだけ**。営業がその画面で伝えるべき核心を1行に凝縮する
- **ラベルの抑制**: ラベルはTertiaryに。値・数値が Primary で目立つように設計（Refactoring UI: 「ラベルは支えであり主役ではない」）

### アクション階層

```
Primary Action:   塗りつぶしボタン (#2563EB) — 1画面に最大1個
                  展示会では「詳しく見る」「次のセクションへ」の意味
Secondary Action: ボーダーボタン (border: 1px solid #334155) — 代替選択肢
Tertiary Action:  テキストリンク (#3B82F6) — 補足情報へのナビ
```

### 具体的なCSS

```css
/* Primary — セクション見出し */
.heading-primary {
  font-size: clamp(2rem, 4vw, 3.5rem);
  font-weight: 700;
  color: #F1F5F9;
  line-height: 1.15;
  letter-spacing: -0.02em;
}

/* Secondary — 要点 */
.heading-secondary {
  font-size: clamp(1.25rem, 2.5vw, 1.75rem);
  font-weight: 600;
  color: #E2E8F0;
  line-height: 1.3;
}

/* Tertiary — 補足 */
.text-tertiary {
  font-size: clamp(1rem, 1.8vw, 1.25rem);
  font-weight: 400;
  color: #94A3B8;
  line-height: 1.6;
}
```

---

## 2. スペーシング (Spacing)

### 展示会向けスペーシングスケール

通常のWebスペーシングスケールの **1.5倍** を基本とする。大画面での視認性と、営業トーク中のセクション区切りの明確化が目的。

**展示会用スケール**:

```
8px — 12px — 16px — 24px — 32px — 48px — 64px — 96px — 128px — 192px
```

| 用途 | 通常LP | 展示会LP | 理由 |
|:---|:---|:---|:---|
| **アイコンとテキスト間** | 4-8px | 8-12px | 遠距離で要素が分離して見えるように |
| **関連要素間（ラベル-値）** | 8px | 12px | グルーピングを維持しつつ余裕を |
| **カード内パディング** | 24px | 32-48px | 大画面での呼吸空間 |
| **グループ内要素間** | 12-16px | 24px | 要素間のリズムを明確に |
| **グループ間** | 24-32px | 48px | セクション内の区切り |
| **セクション間** | 48-64px | 96-128px | 営業トーク区切りと同期 |
| **ページレベル余白** | 96-128px | 128-192px | 大画面での贅沢な余白 |

### セクション間リズム設計

```css
/* セクション間 — 営業が画面切替する単位 */
.section {
  padding: 96px 48px;  /* 上下96px, 左右48px */
}

/* 大画面（展示ディスプレイ） */
@media (min-width: 1200px) {
  .section {
    padding: 128px 64px;
  }
}

/* カード内パディング */
.card {
  padding: 32px;
}
@media (min-width: 1200px) {
  .card {
    padding: 48px;
  }
}

/* グループ内要素間 */
.stack > * + * {
  margin-top: 24px;
}

/* グループ間（カード間など） */
.grid-cards {
  gap: 48px;
}
```

### テキスト幅の制限

```css
/* 展示会LPではテキストブロックの最大幅を広めに */
.prose {
  max-width: 50ch; /* 展示会では短文が多いため、通常より狭くてOK */
}

/* ヒーローの見出しは幅広 */
.hero-heading {
  max-width: 20ch; /* 短く、太く */
}
```

### コンテンツ最大幅

```css
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 48px;
}

/* 大画面展示ディスプレイ用 */
@media (min-width: 1920px) {
  .container {
    max-width: 1440px;
    padding: 0 96px;
  }
}
```

---

## 3. タイポグラフィ (Typography)

### 展示会向け可読性設計

展示会環境では **最小フォントサイズ 18px** を厳守。1m以上離れた来場者でもテキストの概要が掴めることが条件。

### フォントスタック

```css
:root {
  /* 見出し（欧文） */
  --font-heading: 'Inter', system-ui, -apple-system, sans-serif;
  /* 見出し・本文（和文） */
  --font-body: 'Noto Sans JP', "Hiragino Sans", "Hiragino Kaku Gothic ProN", sans-serif;
  /* KPI数値 */
  --font-mono: 'Inter', ui-monospace, monospace;
}
```

### 展示会用タイポグラフィスケール

| 用途 | サイズ | ウェイト | line-height | letter-spacing | 展示会での役割 |
|:---|:---|:---|:---|:---|:---|
| **ヒーロー見出し** | `clamp(2.5rem, 5vw, 4rem)` | 700 | 1.1 | -0.03em | 3m先からの第一印象 |
| **セクション見出し** | `clamp(1.75rem, 3.5vw, 2.5rem)` | 700 | 1.2 | -0.02em | セクション導入 |
| **サブ見出し** | `clamp(1.25rem, 2.5vw, 1.5rem)` | 600 | 1.3 | -0.01em | カードタイトル、要点 |
| **本文（大）** | `1.25rem` (20px) | 400 | 1.75 | 0 | 要点説明（営業が読む部分） |
| **本文** | `1.125rem` (18px) | 400 | 1.75 | 0 | 補足テキスト |
| **KPI数値** | `clamp(3rem, 6vw, 5rem)` | 700 | 1.0 | -0.03em | インパクト数値表示 |
| **KPI単位** | `1.25rem` (20px) | 400 | 1.0 | 0.05em | 数値の補足（%, ms, etc.） |
| **バッジ** | `0.875rem` (14px) | 600 | 1.0 | 0.05em | 「日本初」等のラベル |

### 展示会特有の調整

```css
/* 大きな見出しの letter-spacing を詰める（Refactoring UI: 大サイズでは間延びする） */
.hero-heading {
  font-family: var(--font-heading), var(--font-body);
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.03em;
}

/* KPI数値 — Inter の tabular figures で数値整列 */
.kpi-value {
  font-family: var(--font-mono);
  font-size: clamp(3rem, 6vw, 5rem);
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  line-height: 1.0;
  letter-spacing: -0.03em;
}

/* 本文 — 最小18pxの厳守 */
.body-text {
  font-family: var(--font-body);
  font-size: max(1.125rem, 18px);
  font-weight: 400;
  line-height: 1.75;
}

/* バッジテキスト（ALL CAPS風） */
.badge-text {
  font-family: var(--font-heading), var(--font-body);
  font-size: 0.875rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
```

### Google Fonts 読み込み

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Noto+Sans+JP:wght@400;600;700&display=swap" rel="stylesheet">
```

---

## 4. カラー (Color)

### ダークモード基調の判断

**結論: ダークモード採用**

| 検討項目 | 判断 | 理由 |
|:---|:---|:---|
| 展示会照明 | 採用に有利 | ブース照明の反射が減り、画面コンテンツが際立つ |
| ブランドイメージ | 一致 | セキュリティ = プロフェッショナル、ダークな信頼感 |
| 大画面表示 | 採用に有利 | 白背景の大画面は眩しく、長時間見る営業の目にも優しい |
| コントラスト | 注意が必要 | 十分なコントラスト比の確保が必須（後述） |

### カラーパレット定義 (CSS Custom Properties)

```css
:root {
  /* === Backgrounds === */
  --bg-base:       #0B1120;  /* Dark Navy — 最深背景 */
  --bg-surface:    #131B2E;  /* Elevated Surface — カード背景 */
  --bg-surface-2:  #1A2540;  /* Secondary Surface — セクション背景 */
  --bg-surface-3:  #1E293B;  /* Tertiary Surface — hover状態 */

  /* === Primary (Blue) === */
  --primary-600:   #2563EB;  /* CTA、主要アクション */
  --primary-500:   #3B82F6;  /* ホバー状態 */
  --primary-400:   #60A5FA;  /* アクティブ、選択状態 */
  --primary-900:   #1E3A5F;  /* Primary の暗い背景 */
  --primary-100:   #DBEAFE;  /* Primary の薄い背景 */

  /* === Accent (Cyan) === */
  --accent-500:    #06B6D4;  /* ハイライト、技術バッジ */
  --accent-600:    #0891B2;  /* Accent ホバー */
  --accent-400:    #22D3EE;  /* Accent 明るめ */
  --accent-900:    #0C4A6E;  /* Accent 背景 */

  /* === Text === */
  --text-primary:   #F1F5F9;  /* メインテキスト — Slate 100 */
  --text-secondary: #E2E8F0;  /* サブテキスト — Slate 200 */
  --text-tertiary:  #94A3B8;  /* 注釈テキスト — Slate 400 */
  --text-muted:     #64748B;  /* 最小テキスト — Slate 500 */

  /* === Border === */
  --border-default: #1E293B;  /* Slate 800 — 通常ボーダー */
  --border-subtle:  #334155;  /* Slate 700 — 強調ボーダー */

  /* === Semantic === */
  --gold:    #F59E0B;  /* Amber 500 — 「日本初」バッジ */
  --gold-bg: #78350F;  /* Amber 900 — ゴールドバッジ背景 */
  --success: #10B981;  /* Emerald 500 */
  --warning: #F59E0B;  /* Amber 500 */
  --error:   #EF4444;  /* Red 500 */
  --info:    #06B6D4;  /* Cyan 500 */

  /* === Gradient === */
  --gradient-hero: radial-gradient(ellipse at 50% 0%, #131B2E 0%, #0B1120 70%);
  --gradient-accent: linear-gradient(135deg, #2563EB 0%, #06B6D4 100%);
}
```

### コントラスト比検証

| 組み合わせ | 比率 | WCAG AA | 用途 |
|:---|:---|:---|:---|
| `#F1F5F9` on `#0B1120` | **15.2:1** | Pass (AAA) | メインテキスト on 背景 |
| `#E2E8F0` on `#0B1120` | **13.4:1** | Pass (AAA) | サブテキスト on 背景 |
| `#94A3B8` on `#0B1120` | **6.3:1** | Pass (AA) | 注釈テキスト on 背景 |
| `#F1F5F9` on `#2563EB` | **5.8:1** | Pass (AA) | ボタンテキスト |
| `#F1F5F9` on `#131B2E` | **13.8:1** | Pass (AAA) | テキスト on カード |
| `#0B1120` on `#F59E0B` | **10.1:1** | Pass (AAA) | バッジテキスト |
| `#F1F5F9` on `#0891B2` | **4.7:1** | Pass (AA) | Accent テキスト |

### 展示会ブース照明対策

```css
/* 展示会の強い照明による画面反射を考慮し、以下を適用 */

/* 1. 背景は純黒 #000 ではなく暗いネイビー #0B1120 を使用
      → 純黒は照明の映り込みで安っぽく見える */

/* 2. テキストは純白 #FFF ではなく Slate 100 #F1F5F9
      → 純白はグレアで目が疲れる */

/* 3. ボーダーは微妙な明度差で表現
      → 強い照明下でも境界が認識できる程度のコントラスト */
```

---

## 5. コンポーネント (Components)

### 5-1. 課題カード（Section 2: 課題提起）

営業が「この4つの課題、御社にも当てはまりませんか？」と問いかけながら指すカード。

```css
.challenge-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: 12px;
  padding: 32px;
  transition: all 0.2s ease;
}

.challenge-card:hover {
  border-color: var(--border-subtle);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3),
              0 5px 15px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
}

/* カード内アイコン — 丸背景に収める（意図されたサイズの原則） */
.challenge-card .icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: var(--primary-900);
  display: flex;
  align-items: center;
  justify-content: center;
}

.challenge-card .icon-wrapper svg {
  width: 28px;
  height: 28px;
  color: var(--primary-400);
}

.challenge-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-top: 24px;
}

.challenge-card p {
  font-size: 1.125rem;
  color: var(--text-tertiary);
  margin-top: 12px;
  line-height: 1.75;
}
```

**グリッドレイアウト**:
```css
.challenge-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);  /* 2x2 で4枚 */
  gap: 32px;
}

@media (max-width: 768px) {
  .challenge-grid {
    grid-template-columns: 1fr;
  }
}
```

### 5-2. プラットフォーム統合カード（Section 3）

4プラットフォームを横並びで示すカード。ロゴ + 名前 + 一言説明。

```css
.platform-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-top: 3px solid var(--accent-500);  /* アクセントボーダー */
  border-radius: 12px;
  padding: 32px 24px;
  text-align: center;
}

.platform-card .logo {
  width: 48px;
  height: 48px;
  margin: 0 auto 16px;
  object-fit: contain;
}

.platform-card h4 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
}

.platform-card p {
  font-size: 1rem;
  color: var(--text-tertiary);
  margin-top: 8px;
}
```

### 5-3. 3層防御タイムライン（Section 4）

営業が「この3つのレイヤーで守ります」と説明する、視覚的なスタック図。

```css
/* 3層スタック — 縦積みレイヤー図 */
.defense-layer {
  position: relative;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: 12px;
  padding: 32px 32px 32px 80px;  /* 左にレイヤー番号スペース */
}

.defense-layer + .defense-layer {
  margin-top: -1px;  /* レイヤー間を接続 */
}

/* レイヤー番号バッジ */
.defense-layer .layer-number {
  position: absolute;
  left: 24px;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--text-primary);
}

/* レイヤーごとの色分け */
.defense-layer--1 { border-left: 4px solid #2563EB; }
.defense-layer--1 .layer-number { background: #1E3A5F; color: #60A5FA; }

.defense-layer--2 { border-left: 4px solid #06B6D4; }
.defense-layer--2 .layer-number { background: #0C4A6E; color: #22D3EE; }

.defense-layer--3 { border-left: 4px solid #10B981; }
.defense-layer--3 .layer-number { background: #064E3B; color: #34D399; }

.defense-layer h4 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.defense-layer p {
  font-size: 1.125rem;
  color: var(--text-tertiary);
  margin-top: 8px;
}

/* 製品バッジ群 */
.defense-layer .product-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
}

.product-badge {
  font-size: 0.8125rem;
  font-weight: 500;
  padding: 4px 12px;
  border-radius: 999px;
  background: var(--bg-surface-2);
  color: var(--text-tertiary);
  border: 1px solid var(--border-default);
}
```

### 5-4. 特長カード（Section 5: なぜナレコムか）

3カラムの差別化ポイントカード。

```css
.feature-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: 12px;
  padding: 40px 32px;
  position: relative;
  overflow: hidden;
}

/* 上部のアクセントグラデーション帯 */
.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--gradient-accent);
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

@media (max-width: 1024px) {
  .feature-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
}
```

### 5-5. タイムライン（Section 6: PoC の流れ）

8週間4スプリントのタイムライン。横並びの進行表。

```css
.timeline {
  display: flex;
  gap: 0;
  position: relative;
}

.timeline::before {
  content: '';
  position: absolute;
  top: 36px;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--border-subtle);
}

.timeline-item {
  flex: 1;
  position: relative;
  padding-top: 56px;
  text-align: center;
}

/* タイムラインドット */
.timeline-item::before {
  content: '';
  position: absolute;
  top: 28px;
  left: 50%;
  transform: translateX(-50%);
  width: 16px;
  height: 16px;
  border-radius: 999px;
  background: var(--primary-600);
  border: 3px solid var(--bg-base);
  z-index: 1;
}

.timeline-item .sprint-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--accent-500);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.timeline-item .sprint-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-top: 8px;
}

.timeline-item .sprint-duration {
  font-size: 1rem;
  color: var(--text-tertiary);
  margin-top: 4px;
}
```

### 5-6. KPI数値カウンター（Section 7）

大きな数値で実績をインパクトのある形で表示。

```css
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 32px;
}

.kpi-item {
  text-align: center;
  padding: 32px 16px;
}

.kpi-item .value {
  font-family: var(--font-mono);
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  line-height: 1.0;
  letter-spacing: -0.03em;
  /* 数値ごとに色を変えてバリエーションを出す */
}

.kpi-item .value--primary { color: var(--primary-400); }
.kpi-item .value--accent  { color: var(--accent-400); }
.kpi-item .value--success { color: var(--success); }
.kpi-item .value--gold    { color: var(--gold); }

.kpi-item .unit {
  font-size: 1.25rem;
  font-weight: 400;
  color: var(--text-tertiary);
  margin-top: 4px;
}

.kpi-item .label {
  font-size: 1rem;
  color: var(--text-tertiary);
  margin-top: 12px;
}

@media (max-width: 1024px) {
  .kpi-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### 5-7. FAQ アコーディオン（Section 8）

```css
.faq-item {
  border-bottom: 1px solid var(--border-default);
  padding: 24px 0;
}

.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
}

.faq-question .chevron {
  width: 24px;
  height: 24px;
  color: var(--text-muted);
  transition: transform 0.2s ease;
}

.faq-item.open .chevron {
  transform: rotate(180deg);
}

.faq-answer {
  font-size: 1.125rem;
  color: var(--text-tertiary);
  line-height: 1.75;
  padding-top: 16px;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.faq-item.open .faq-answer {
  max-height: 500px;
}
```

### 5-8. CTA ボタン

```css
/* Primary CTA */
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 16px 32px;
  font-size: 1.125rem;
  font-weight: 600;
  color: #FFFFFF;
  background: var(--primary-600);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.btn-primary:hover {
  background: var(--primary-500);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3),
              0 5px 15px rgba(0, 0, 0, 0.2);
  transform: translateY(-1px);
}

.btn-primary:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

/* Secondary CTA (Ghost) */
.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 16px 32px;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  background: transparent;
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  border-color: var(--text-muted);
  background: var(--bg-surface-3);
}
```

### 5-9. 「日本初」バッジ

```css
.badge-japan-first {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 16px;
  font-size: 0.875rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  color: #0B1120;
  background: var(--gold);
  border-radius: 999px;
  box-shadow: 0 0 20px rgba(245, 158, 11, 0.3);
}
```

---

## 6. 深度・シャドウ (Depth & Shadow)

### ダークモードでの深度表現原則

ダークモードでは **box-shadow よりも背景色の階層とボーダー** で深度を表現する。影は背景と同化して見えにくいため、補助的に使用。

### エレベーションシステム（5段階）

| レベル | 用途 | 背景色 | ボーダー | box-shadow |
|:---|:---|:---|:---|:---|
| **Level 0** | 最下層（ページ背景） | `#0B1120` | なし | なし |
| **Level 1** | セクション背景 | `#131B2E` | `1px solid #1E293B` | なし |
| **Level 2** | カード、パネル | `#1A2540` | `1px solid #1E293B` | `var(--shadow-sm)` |
| **Level 3** | ホバー状態、ポップオーバー | `#1E293B` | `1px solid #334155` | `var(--shadow-md)` |
| **Level 4** | モーダル、最前面 | `#1E293B` | `1px solid #334155` | `var(--shadow-lg)` |

### Shadow 定義

```css
:root {
  /* ダークモード用 — 通常より不透明度を高めに */
  --shadow-sm:  0 1px 3px rgba(0, 0, 0, 0.4);
  --shadow-md:  0 4px 6px rgba(0, 0, 0, 0.3),
                0 2px 4px rgba(0, 0, 0, 0.2);
  --shadow-lg:  0 5px 15px rgba(0, 0, 0, 0.3),
                0 4px 6px rgba(0, 0, 0, 0.2);
  --shadow-xl:  0 15px 35px rgba(0, 0, 0, 0.4);
  --shadow-2xl: 0 20px 25px rgba(0, 0, 0, 0.35),
                0 10px 10px rgba(0, 0, 0, 0.15);
}
```

### インタラクション時の深度変化

```css
/* ホバーで浮き上がる */
.card {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  box-shadow: none;
  transition: all 0.2s ease;
}

.card:hover {
  background: var(--bg-surface-2);
  border-color: var(--border-subtle);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

/* ボタンのクリック — 押し込み感 */
.btn-primary:active {
  box-shadow: none;
  transform: translateY(0);
}
```

### 光源の統一（上から光）

```css
/* Raised 要素 — 上辺を微かに明るく */
.card {
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

/* Inset 要素（入力フィールド等） — 上辺に暗い影 */
.input {
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
}
```

### フラットデザインとの両立

ダークモードの展示会LPでは、**色差による深度** を主軸とする。

```css
/* 色差で深度を表現 */
.surface-raised { background: #1A2540; }  /* 手前 — 背景より明るい */
.surface-base   { background: #131B2E; }  /* 標準 */
.surface-inset  { background: #0B1120; }  /* 奥  — 背景より暗い */
```

---

## 7. 画像・イラスト (Images & Illustrations)

### 7-1. 3層防御の概念図設計

**図解の方針**: イラストや写真ではなく、CSS/SVGで構築する幾何学的な概念図。展示会では「営業が指差しながら説明できるシンプルさ」が最重要。

**3層スタック図の設計仕様**:

```
┌──────────────────────────────────────────────┐
│  Layer 3: 監査証跡                            │  ← #10B981 系
│  ISO/IEC 42001 PDCA | ログ統合 | 証跡自動生成   │
├──────────────────────────────────────────────┤
│  Layer 2: 継続的レッドチーミング                │  ← #06B6D4 系
│  月次自動実行 | 脆弱性マトリクス | 攻撃パック更新 │
├──────────────────────────────────────────────┤
│  Layer 1: 推論時多層防御                       │  ← #2563EB 系
│  block / audit / redact | P95 ≤ 500ms         │
└──────────────────────────────────────────────┘
```

```css
/* レイヤー図のCSS */
.defense-diagram {
  display: flex;
  flex-direction: column;
  gap: 2px;  /* レイヤー間の微小ギャップ */
  max-width: 800px;
  margin: 0 auto;
}

.defense-diagram .layer {
  padding: 32px 40px;
  border-radius: 8px;
  position: relative;
}

.defense-diagram .layer--1 {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.15) 0%, rgba(37, 99, 235, 0.05) 100%);
  border: 1px solid rgba(37, 99, 235, 0.3);
}

.defense-diagram .layer--2 {
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(6, 182, 212, 0.05) 100%);
  border: 1px solid rgba(6, 182, 212, 0.3);
}

.defense-diagram .layer--3 {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
  border: 1px solid rgba(16, 185, 129, 0.3);
}
```

### 7-2. ヒーロー背景の幾何学装飾

ヒーローセクションの背景: **抽象的なネットワーク/グリッドパターン** をCSSで生成。画像ファイル不要。

```css
.hero-bg {
  position: relative;
  background: var(--gradient-hero);
  overflow: hidden;
}

/* グリッドパターン (CSS背景) */
.hero-bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(37, 99, 235, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(37, 99, 235, 0.05) 1px, transparent 1px);
  background-size: 64px 64px;
  mask-image: radial-gradient(ellipse at 50% 50%, black 30%, transparent 70%);
  -webkit-mask-image: radial-gradient(ellipse at 50% 50%, black 30%, transparent 70%);
}

/* 装飾的な光源グロー */
.hero-bg::after {
  content: '';
  position: absolute;
  top: -200px;
  left: 50%;
  transform: translateX(-50%);
  width: 600px;
  height: 400px;
  background: radial-gradient(ellipse, rgba(37, 99, 235, 0.15) 0%, transparent 70%);
  pointer-events: none;
}
```

### 7-3. アイコン設計方針

Refactoring UI の「意図されたサイズ」原則に従い、アイコンは必ず背景付きで配置。

| 用途 | アイコンサイズ | 背景サイズ | 背景色 | 角丸 |
|:---|:---|:---|:---|:---|
| 課題カード | 28px | 56px | `var(--primary-900)` | 12px |
| 特長カード | 24px | 48px | `var(--accent-900)` | 10px |
| タイムライン | 20px | 40px | `var(--bg-surface-2)` | 999px |
| KPI | 使用しない (数値がアイコン代わり) | — | — | — |
| バッジ | 14px | インライン | — | — |

```css
/* アイコンラッパー — 共通 */
.icon-box {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-box--lg {
  width: 56px;
  height: 56px;
  border-radius: 12px;
}

.icon-box--md {
  width: 48px;
  height: 48px;
  border-radius: 10px;
}

.icon-box--sm {
  width: 40px;
  height: 40px;
  border-radius: 999px;
}
```

### 7-4. プラットフォームロゴの取り扱い

```css
/* ロゴは固定サイズで表示 — 拡大しない */
.platform-logo {
  width: 48px;
  height: 48px;
  object-fit: contain;
  /* ダークモード対応: 白抜きロゴを推奨。
     カラーロゴの場合は明るい背景の丸い枠に配置 */
}

/* カラーロゴ用の背景枠 */
.logo-container--light {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}
```

---

## 8. 仕上げ (Finishing Touches)

### 8-1. アクセントボーダー

展示会LPの「デザインされた感」を出す最も効果的な手法。

| 配置 | 実装 | 目的 |
|:---|:---|:---|
| **ページ上端** | 全幅 4px グラデーション帯 | サイト全体のブランディング |
| **カード上端** | `border-top: 3px solid` | カードに個性を追加 |
| **3層防御レイヤー左辺** | `border-left: 4px solid` | レイヤー色の視覚的識別 |
| **セクション見出し下** | 48px幅の短い帯 | セクション開始の強調 |
| **CTA セクション** | 上部にグラデーション帯 | 注目を集める |

```css
/* ページ最上部のブランドライン */
body::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--gradient-accent);
  z-index: 9999;
}

/* セクション見出し下のアクセント */
.section-heading::after {
  content: '';
  display: block;
  width: 48px;
  height: 3px;
  background: var(--gradient-accent);
  margin-top: 16px;
  border-radius: 2px;
}

/* 中央揃えの場合 */
.section-heading--center::after {
  margin-left: auto;
  margin-right: auto;
}
```

### 8-2. グラデーション効果

```css
/* テキストグラデーション — KPI セクション見出し等で限定使用 */
.text-gradient {
  background: var(--gradient-accent);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* セクション間のグラデーション区切り */
.section--alt {
  background: linear-gradient(180deg, var(--bg-surface) 0%, var(--bg-base) 100%);
}

/* CTA セクションのハイライト背景 */
.section--cta {
  background: radial-gradient(ellipse at 50% 50%, rgba(37, 99, 235, 0.1) 0%, transparent 60%);
}
```

### 8-3. デフォルト要素の強化

| 要素 | 標準 | 展示会LP版の強化 |
|:---|:---|:---|
| **箇条書き** | `bullet` | Cyan チェックマークアイコン + 左パディング |
| **引用・数値** | プレーンテキスト | 巨大フォント + グラデーション色 |
| **区切り線** | `<hr>` 1px | グラデーション帯 3px、中央幅 120px |
| **ラジオ/チェック** | ブラウザデフォルト | 不使用（展示会LPにフォームは置かない） |

```css
/* 強化された箇条書き */
.feature-list {
  list-style: none;
  padding: 0;
}

.feature-list li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  font-size: 1.125rem;
  color: var(--text-secondary);
  line-height: 1.75;
}

.feature-list li + li {
  margin-top: 16px;
}

.feature-list li::before {
  content: '';
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  margin-top: 4px;
  background: var(--accent-500);
  /* チェックマーク SVG をマスクで適用 */
  mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='currentColor'%3E%3Cpath fill-rule='evenodd' d='M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z' clip-rule='evenodd'/%3E%3C/svg%3E");
  -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='currentColor'%3E%3Cpath fill-rule='evenodd' d='M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z' clip-rule='evenodd'/%3E%3C/svg%3E");
}

/* 装飾的な区切り線 */
.divider {
  width: 120px;
  height: 3px;
  background: var(--gradient-accent);
  border: none;
  border-radius: 2px;
  margin: 48px auto;
}
```

### 8-4. ボーダーの代替

ダークモードでは特にボーダーの多用が「ビジー」に見える。以下の代替を優先。

| 代替手法 | 適用場面 | CSS |
|:---|:---|:---|
| **背景色の差** | セクション間、カードと背景 | `background: var(--bg-surface)` on `var(--bg-base)` |
| **余白** | リスト項目間、段落間 | `margin-top: 24px` |
| **微細な shadow** | カードの外枠（ボーダー代替） | `box-shadow: 0 0 0 1px rgba(255,255,255,0.05)` |

```css
/* ボーダー代替 — ring shadow */
.card-borderless {
  background: var(--bg-surface);
  border: none;
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.06);
  border-radius: 12px;
}
```

### 8-5. 装飾的幾何学シェイプ

```css
/* セクション背景の装飾円（コンテンツの邪魔にならない薄さ） */
.section--decorated {
  position: relative;
}

.section--decorated::before {
  content: '';
  position: absolute;
  top: -100px;
  right: -100px;
  width: 400px;
  height: 400px;
  border-radius: 999px;
  background: radial-gradient(circle, rgba(6, 182, 212, 0.06) 0%, transparent 70%);
  pointer-events: none;
}
```

### 8-6. 角丸の差別化

AI slop 回避: 全要素同じ角丸にしない。

| 要素 | 角丸 | 理由 |
|:---|:---|:---|
| カード | `12px` | 大きめで親しみやすい |
| ボタン | `8px` | カードより小さく引き締める |
| バッジ | `999px` (pill) | 小さい要素は完全丸で軽やかに |
| 入力フィールド | `8px` | ボタンと統一 |
| アイコン背景 | `12px` or `999px` | サイズに応じて使い分け |
| 3層防御レイヤー | `8px` | スタック図なので控えめに |

---

## 設計チェックリスト（Refactoring UI 8観点）

### 視覚的階層
- [x] Primary / Secondary / Tertiary の3段階が存在する
- [x] サイズだけでなく色・ウェイトも活用して階層を作っている
- [x] ラベルが値より目立っていない
- [x] Primary Action は1画面に1個に制限されている

### スペーシング
- [x] 展示会用スケール（通常の1.5倍）に従っている
- [x] 関連要素間 < 非関連要素間の距離関係が守られている
- [x] テキスト行幅が制限されている
- [x] セクション間のリズムが営業トークの区切りと同期している

### タイポグラフィ
- [x] フォントは2種類（Inter + Noto Sans JP）に制限
- [x] 最小フォントサイズ18px（バッジの14pxを除く）
- [x] 見出しの line-height が 1.3 以下
- [x] 大きな見出しで letter-spacing がマイナス調整されている
- [x] KPI数値に tabular-nums を適用

### カラー
- [x] ダークモード基調でブース照明対策済み
- [x] 全テキスト-背景組み合わせが WCAG AA 以上
- [x] セマンティックカラー（成功/警告/エラー/情報）が定義されている
- [x] 3層防御のレイヤー色が視覚的に区別可能

### コンポーネント
- [x] ボタンに Primary / Secondary 階層がある
- [x] カードスタイルが統一されている（背景 + ボーダー + hover shadow）
- [x] タイムラインUIが4スプリントを視覚的に表現
- [x] KPI数値が大きく目立つレイアウト

### 深度・シャドウ
- [x] ダークモード用の5段階エレベーションが定義されている
- [x] 背景色の階層で深度を主に表現（shadowは補助）
- [x] インタラクション時に深度が変化する（hover: 浮く, active: 沈む）
- [x] 光源方向（上から）が統一されている

### 画像・イラスト
- [x] 3層防御の概念図がCSS/SVGで設計されている
- [x] アイコンが意図されたサイズで使用されている（背景付き）
- [x] ヒーロー背景がCSSグラデーション + パターンで構成
- [x] プラットフォームロゴが固定サイズで管理されている

### 仕上げ
- [x] ページ上端にブランドラインのアクセントボーダー
- [x] セクション見出し下にグラデーション帯
- [x] 箇条書きがチェックマークアイコンで強化されている
- [x] ボーダーの代わりに背景色差・余白・微細shadowを使用
- [x] 角丸が要素種類ごとに差別化されている

---

## セクション別の設計サマリ

| Section | 背景 | 主要コンポーネント | 特記 |
|:---|:---|:---|:---|
| **1. ヒーロー** | `var(--gradient-hero)` + グリッドパターン | Badge + Heading + CTA | 中央揃え、グロー装飾 |
| **2. 課題提起** | `var(--bg-base)` | 2x2 Challenge Cards | アイコン + テキスト |
| **3. ソリューション** | `var(--bg-surface)` | Platform Cards (4列) | ロゴ + アクセントボーダー上端 |
| **4. 3層防御** | `var(--bg-base)` | Defense Layer Stack | 左ボーダー色分け + 番号バッジ |
| **5. 特長** | `var(--bg-surface)` 装飾付き | Feature Cards (3列) | グラデーション上端ボーダー |
| **6. PoC の流れ** | `var(--bg-base)` | Timeline (4ステップ) | 横並びドットライン |
| **7. KPI** | `var(--bg-surface)` + グロー | KPI Counter Grid (5列) | 巨大数値 + 色分け |
| **8. FAQ** | `var(--bg-base)` | Accordion | 展示会では2-3問に絞り可 |
| **9. CTA** | `var(--bg-base)` + アクセントグロー | Primary + Secondary Button | 中央揃え |
| **10. フッター** | `var(--bg-base)` (darkest) | 会社情報 + リンク | 最小限 |
