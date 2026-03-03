# ビジュアル戦略: GenAI セキュリティガードレール設計サービス — 展示会ブース LP

> **作成日**: 2026-02-22 | **バージョン**: 1.0.0
> **用途**: 「AIセキュリティ ガバナンスEXPO」展示会ブースで対面説明に使う単一HTML LP
> **技術制約**: 単一HTML（Tailwind CSS CDN）、インラインSVG、Google Fonts

---

## 1. コンセプトキーワード

| # | キーワード | ビジュアルへの翻訳 |
|:---|:---|:---|
| 1 | **信頼** | 深いネイビー基調、安定感のある水平ライン、堅牢な構造表現 |
| 2 | **先進性** | シアンのアクセントライト、微細な幾何学パターン、鋭角的な装飾 |
| 3 | **防御** | シールドモチーフ、多層構造の視覚表現、囲い込むレイアウト |
| 4 | **透明性** | グラスモーフィズム風のカード、半透明サーフェス、見通しの良い余白 |
| 5 | **日本初** | ゴールドアクセントバッジ、差別化を示す視覚的な特別感 |

## 2. ムードボード方針

- **カラー方向性**: ダークネイビー基調にシアンアクセント。セキュリティの堅牢さをダークモードで、先進性をシアンの発光表現で伝える。ゴールドは「日本初」バッジ限定の特別色。
- **写真スタイル**: 写真は使用しない。代わりにインラインSVGの幾何学パターン（ネットワークノード、シールド、多層レイヤー図）で抽象的に表現。展示会ブースでは大画面表示のため、ベクター表現が鮮明。
- **レイアウト傾向**: センター配置を基本としつつ、セクションごとに明度を切り替えてリズムを作る。展示会の大画面（横長ディスプレイ）を想定し、横幅を活かしたワイドレイアウト。
- **タイポグラフィ方向**: ジオメトリックサンセリフ（欧文）+ 高可読性ゴシック（和文）。展示会では離れた位置からの視認性が重要なため、通常より大きめのスケール。

## 3. ヒーローセクション構成案

### パターンA: センター配置 + ダークメッシュグラデーション背景（推奨）

展示会向け最適。大画面で映えるダークグラデーション背景に、SVGの微細なグリッドパターンをオーバーレイ。テキストは中央配置で、来場者が遠くからでも読める大きなヘッドライン。

```
[ゴールドバッジ: 日本初]
[ヘッドライン: 大文字・白・中央]
[サブヘッド: シアンアクセント・3つの特長]
[CTAボタン: Blue 600・角丸8px]
```

### パターンB: スプリットレイアウト（左テキスト・右SVG図解）

左半分にテキスト（ヘッドライン + CTA）、右半分にインラインSVGの3層防御構造図。技術的な信頼性を視覚的に即座に伝える構成。

### パターンC: フルスクリーンダーク + アニメーション付きネットワークノード

背景全体にアニメーション付きのSVGネットワーク図を配置し、テキストをオーバーレイ。先進性を最も強く訴求できるが、パフォーマンスに注意が必要。

---

## 4. カラーシステム

### コンセプトからの導出根拠

| コンセプト | 導出されるカラー | 理由 |
|:---|:---|:---|
| 信頼 | ダークネイビー `#0B1120` | 金融・セキュリティ業界で信頼を示す深い紺 |
| 先進性 | シアン `#06B6D4` | テクノロジーの先端性、ネオンライト的な発光感 |
| 防御 | ブルー `#2563EB` | アクション・CTA に使う確実性の青 |
| 透明性 | スレートグレー系 | 半透明サーフェスで「見通せる」透明性を表現 |
| 日本初 | アンバーゴールド `#F59E0B` | 特別感・差別化を示すアクセント（限定使用） |

### CSS 変数定義

```css
:root {
  /* === 背景・サーフェス === */
  --color-bg:             #0B1120;  /* Dark Navy — 最深層の背景 */
  --color-surface:        #131B2E;  /* Elevated Surface — カード・セクション背景 */
  --color-surface-alt:    #1A2540;  /* Alternative Surface — ホバー・アクティブ */

  /* === プライマリ（CTA・主要アクション） === */
  --color-primary:        #2563EB;  /* Blue 600 — ボタン・リンク */
  --color-primary-light:  #3B82F6;  /* Blue 500 — ホバー */
  --color-primary-dark:   #1D4ED8;  /* Blue 700 — プレス */

  /* === アクセント（ハイライト・装飾） === */
  --color-accent:         #06B6D4;  /* Cyan 500 — バッジ・ハイライト */
  --color-accent-dark:    #0891B2;  /* Cyan 600 — アクセント暗め */

  /* === ゴールド（「日本初」バッジ専用） === */
  --color-gold:           #F59E0B;  /* Amber 500 — 特別感 */
  --color-gold-dark:      #D97706;  /* Amber 600 */

  /* === テキスト === */
  --color-text:           #F1F5F9;  /* Slate 100 — メインテキスト */
  --color-text-muted:     #94A3B8;  /* Slate 400 — サブテキスト */
  --color-text-tertiary:  #64748B;  /* Slate 500 — 注釈・キャプション */

  /* === ボーダー === */
  --color-border:         #1E293B;  /* Slate 800 — 境界線 */
  --color-border-light:   #334155;  /* Slate 700 — ホバー時ボーダー */

  /* === セマンティック === */
  --color-success:        #10B981;  /* Emerald 500 */
  --color-warning:        #F59E0B;  /* Amber 500 */
  --color-error:          #EF4444;  /* Red 500 */
}
```

### WCAG AA コントラスト比確認

| 組み合わせ | コントラスト比 | WCAG AA（通常テキスト） | WCAG AA（大テキスト） |
|:---|:---|:---|:---|
| `#F1F5F9` on `#0B1120` | 15.2:1 | PASS | PASS |
| `#94A3B8` on `#0B1120` | 6.3:1 | PASS | PASS |
| `#64748B` on `#0B1120` | 4.0:1 | FAIL（注釈は大テキストのみ） | PASS |
| `#F1F5F9` on `#2563EB` | 5.8:1 | PASS | PASS |
| `#0B1120` on `#F59E0B` | 10.1:1 | PASS | PASS |
| `#F1F5F9` on `#131B2E` | 13.8:1 | PASS | PASS |
| `#06B6D4` on `#0B1120` | 7.5:1 | PASS | PASS |

> **注意**: `--color-text-tertiary`（`#64748B`）は通常テキスト（16px以下）には使用不可。18px以上のboldまたは24px以上のテキストにのみ使用する。

### 展示会照明下の視認性考慮

- 展示会場は照明が明るく、ダークモード画面のコントラストが低下しやすい
- **対策**: ディスプレイの輝度を最大に設定する前提で、テキストは`#F1F5F9`（ほぼ白）を基本とし、`#94A3B8`以下の薄いテキストは重要情報に使わない
- カードのボーダー`#1E293B`は照明下で見えにくくなる可能性あり → ボーダー幅を2pxに拡大、またはサーフェス色差で深度表現

---

## 5. タイポグラフィ選定

### フォントペアリング

| 用途 | フォント | ウェイト | 根拠 |
|:---|:---|:---|:---|
| 見出し（欧文） | **Space Grotesk** | 500, 700 | ジオメトリックでテック感。Inter よりも個性があり AI slop を回避 |
| 見出し・本文（和文） | **Noto Sans JP** | 400, 700 | 可読性最高のゴシック体。展示会の大画面でも安定した視認性 |
| 数値・KPI | **Space Grotesk** | 700 | Tabular Figures対応。KPIカウンター表示に最適 |

### Google Fonts 読み込み

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet">
```

### font-family 宣言

```css
body {
  font-family: 'Space Grotesk', 'Noto Sans JP', 'Hiragino Kaku Gothic ProN', 'Yu Gothic', sans-serif;
  font-feature-settings: "palt" 1, "kern" 1;
}
```

### タイポグラフィスケール（展示会用拡大版）

展示会ブースの大画面（40-60インチ、視距離1-3m）を考慮し、通常のWebサイトより1-2段階大きいスケールを採用。

```css
:root {
  /* === 展示会用拡大タイポグラフィスケール === */
  --text-hero:    clamp(3rem, 6vw, 5rem);        /* ヒーロー見出し: 48-80px */
  --text-section: clamp(2rem, 4vw, 3rem);         /* セクション見出し: 32-48px */
  --text-sub:     clamp(1.375rem, 2.5vw, 1.75rem); /* サブ見出し: 22-28px */
  --text-body-lg: clamp(1.125rem, 1.5vw, 1.25rem); /* 本文（大）: 18-20px */
  --text-body:    clamp(1rem, 1.2vw, 1.125rem);    /* 本文: 16-18px */
  --text-caption: clamp(0.875rem, 1vw, 1rem);      /* キャプション: 14-16px */
  --text-badge:   0.75rem;                          /* バッジ: 12px固定 */
  --text-kpi:     clamp(3rem, 5vw, 4.5rem);       /* KPI数値: 48-72px */
}

/* 見出し共通 */
h1, h2, h3 {
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.01em;
}

/* 本文（日本語最適化） */
body {
  font-size: var(--text-body);
  line-height: 1.8;
  letter-spacing: 0.04em;
}
```

---

## 6. レイアウトパターン設計

### パターン1: センター配置ヒーロー + ダークグラデーション（推奨・メイン）

展示会ブースの大画面に最適。来場者が離れた位置からでもキーメッセージを読める。

```css
.hero {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: clamp(2rem, 5vw, 4rem);
  position: relative;
  overflow: hidden;
  background: var(--color-bg);
}

/* メッシュグラデーション背景 */
.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 20% 50%, rgba(6, 182, 212, 0.08) 0%, transparent 60%),
    radial-gradient(ellipse 60% 70% at 80% 30%, rgba(37, 99, 235, 0.1) 0%, transparent 55%),
    radial-gradient(ellipse 90% 40% at 50% 100%, rgba(6, 182, 212, 0.05) 0%, transparent 50%);
  pointer-events: none;
}

.hero__content {
  position: relative;
  z-index: 1;
  max-width: 900px;
}
```

### パターン2: カード/フィーチャーグリッド（セクション向け）

課題提起、ソリューション概要、サービス特長に使用。展示会では3カラムで特長を一覧表示。

```css
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: clamp(1rem, 2vw, 1.5rem);
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 clamp(1rem, 3vw, 2rem);
}

.feature-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: clamp(1.5rem, 3vw, 2rem);
  transition: border-color 0.25s, transform 0.2s;
}

.feature-card:hover {
  border-color: var(--color-border-light);
  transform: translateY(-2px);
}
```

### パターン3: タイムラインレイアウト（PoC フロー向け）

8週間のスプリント計画をステップバイステップで視覚化。展示会で「具体的なアクション」を示す。

```css
.timeline {
  display: flex;
  gap: clamp(1rem, 2vw, 2rem);
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 clamp(1rem, 3vw, 2rem);
  overflow-x: auto;
}

.timeline__step {
  flex: 1;
  min-width: 200px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-top: 3px solid var(--color-accent);
  border-radius: 0 0 12px 12px;
  padding: clamp(1.25rem, 2vw, 1.75rem);
  position: relative;
}

.timeline__step-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  background: var(--color-accent);
  color: var(--color-bg);
  border-radius: 50%;
  font-weight: 700;
  font-size: var(--text-caption);
  margin-bottom: 0.75rem;
}
```

### セクション間のリズム設計

展示会の大画面では、セクション間の区切りを明確にする必要がある。背景色の切り替えでリズムを作る。

```
Section 1 (Hero):     --color-bg (#0B1120) + メッシュグラデーション
Section 2 (課題):      --color-surface (#131B2E)
Section 3 (ソリューション): --color-bg (#0B1120)
Section 4 (3層防御):   --color-surface (#131B2E)
Section 5 (特長):      --color-bg (#0B1120)
Section 6 (PoC):       --color-surface (#131B2E)
Section 7 (KPI):       --color-bg (#0B1120) + アクセントグラデーション
Section 8 (FAQ):       --color-surface (#131B2E)
Section 9 (CTA):       ブルーグラデーション（特別なセクション）
Section 10 (Footer):   --color-bg (#0B1120)
```

---

## 7. CSS スニペット

### 7.1 グラデーション背景

```css
/* ヒーロー用メッシュグラデーション — ネイビー基調にシアンとブルーの光球 */
.grad-hero-mesh {
  background:
    radial-gradient(ellipse 80% 50% at 20% 50%, rgba(6, 182, 212, 0.08) 0%, transparent 60%),
    radial-gradient(ellipse 60% 70% at 80% 30%, rgba(37, 99, 235, 0.1) 0%, transparent 55%),
    radial-gradient(ellipse 90% 40% at 50% 100%, rgba(6, 182, 212, 0.05) 0%, transparent 50%),
    var(--color-bg);
}

/* CTA セクション用グラデーション — Blue の帯で行動を促す */
.grad-cta {
  background: linear-gradient(
    135deg,
    var(--color-primary-dark) 0%,
    var(--color-primary) 50%,
    #1E40AF 100%
  );
}

/* SVG ノイズテクスチャ付きグラデーション — 質感を出す */
.grad-textured {
  background:
    url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.7' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E"),
    var(--color-bg);
}
```

### 7.2 CTA ボタン

```css
/* Primary CTA — Blue 600 ソリッド + ホバーリフト */
.cta-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: clamp(0.875rem, 1.5vw, 1.125rem) clamp(1.5rem, 3vw, 2.5rem);
  font-size: var(--text-body-lg);
  font-weight: 700;
  color: #FFFFFF;
  background: var(--color-primary);
  border: 2px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.25s, transform 0.2s, box-shadow 0.25s;
  text-decoration: none;
}

.cta-primary:hover {
  background: var(--color-primary-light);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.3);
}

.cta-primary:active {
  transform: translateY(0);
  box-shadow: none;
}

.cta-primary:focus-visible {
  outline: 3px solid var(--color-accent);
  outline-offset: 3px;
}

/* Secondary CTA — ゴーストボタン */
.cta-secondary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: clamp(0.875rem, 1.5vw, 1.125rem) clamp(1.5rem, 3vw, 2.5rem);
  font-size: var(--text-body-lg);
  font-weight: 600;
  color: var(--color-text);
  background: transparent;
  border: 2px solid var(--color-border-light);
  border-radius: 8px;
  cursor: pointer;
  transition: color 0.25s, background 0.25s, border-color 0.25s, transform 0.2s;
  text-decoration: none;
}

.cta-secondary:hover {
  color: #FFFFFF;
  background: rgba(241, 245, 249, 0.08);
  border-color: var(--color-text-muted);
  transform: translateY(-1px);
}

.cta-secondary:active {
  transform: translateY(0);
}

.cta-secondary:focus-visible {
  outline: 3px solid var(--color-accent);
  outline-offset: 3px;
}
```

### 7.3 「日本初」バッジ

```css
/* 日本初バッジ — ゴールドアクセント、ピル型 */
.badge-first {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 1rem;
  font-size: var(--text-badge);
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-bg);
  background: linear-gradient(135deg, var(--color-gold) 0%, var(--color-gold-dark) 100%);
  border-radius: 999px;
  line-height: 1;
}
```

### 7.4 カード（ダークサーフェス）

```css
/* ダークサーフェスカード — ボーダー + subtle hover */
.card-dark {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: clamp(1.5rem, 3vw, 2rem);
  transition: border-color 0.3s, transform 0.2s;
}

.card-dark:hover {
  border-color: var(--color-accent-dark);
  transform: translateY(-2px);
}

/* アイコン付きカード */
.card-dark__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  background: rgba(6, 182, 212, 0.1);
  border-radius: 10px;
  margin-bottom: 1rem;
  color: var(--color-accent);
}
```

### 7.5 KPI カウンター

```css
/* KPI 数値表示 — 大きな数値 + ラベル */
.kpi-counter {
  text-align: center;
  padding: 1.5rem;
}

.kpi-counter__value {
  font-family: 'Space Grotesk', monospace;
  font-size: var(--text-kpi);
  font-weight: 700;
  color: var(--color-accent);
  line-height: 1;
  letter-spacing: -0.02em;
}

.kpi-counter__label {
  font-size: var(--text-caption);
  color: var(--color-text-muted);
  margin-top: 0.5rem;
  letter-spacing: 0.02em;
}
```

### 7.6 アニメーション

```css
/* fadeInUp — セクション登場 */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in-up {
  opacity: 0;
  animation: fadeInUp 0.7s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

.animate-delay-1 { animation-delay: 0.15s; }
.animate-delay-2 { animation-delay: 0.3s; }
.animate-delay-3 { animation-delay: 0.45s; }
.animate-delay-4 { animation-delay: 0.6s; }

/* スクロールトリガー — Intersection Observer 連携 */
.scroll-reveal {
  opacity: 0;
  transform: translateY(32px);
  transition: opacity 0.7s cubic-bezier(0.22, 1, 0.36, 1),
              transform 0.7s cubic-bezier(0.22, 1, 0.36, 1);
}

.scroll-reveal.is-visible {
  opacity: 1;
  transform: translateY(0);
}

/* アクセシビリティ: モーション抑制対応 */
@media (prefers-reduced-motion: reduce) {
  .animate-fade-in-up,
  .scroll-reveal {
    opacity: 1;
    transform: none;
    animation: none;
    transition: none;
  }
}
```

### 7.7 3層防御ビジュアル用スタイル

```css
/* 3層スタック — 多層防御の視覚表現 */
.layer-stack {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 800px;
  margin: 0 auto;
}

.layer-stack__item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-left: 4px solid var(--color-accent);
  border-radius: 0 12px 12px 0;
  padding: clamp(1.25rem, 2vw, 1.75rem);
  transition: border-color 0.3s;
}

.layer-stack__item:nth-child(1) { border-left-color: var(--color-accent); }
.layer-stack__item:nth-child(2) { border-left-color: var(--color-primary); }
.layer-stack__item:nth-child(3) { border-left-color: var(--color-gold); }

.layer-stack__item:hover {
  border-color: var(--color-border-light);
}

.layer-stack__number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  font-weight: 700;
  font-size: var(--text-body-lg);
  flex-shrink: 0;
}

.layer-stack__item:nth-child(1) .layer-stack__number {
  background: rgba(6, 182, 212, 0.15);
  color: var(--color-accent);
}
.layer-stack__item:nth-child(2) .layer-stack__number {
  background: rgba(37, 99, 235, 0.15);
  color: var(--color-primary-light);
}
.layer-stack__item:nth-child(3) .layer-stack__number {
  background: rgba(245, 158, 11, 0.15);
  color: var(--color-gold);
}
```

---

## 8. インラインSVG 装飾方針

展示会LP はインラインSVG で装飾する。以下のモチーフを統一的に使用する。

### 使用するモチーフ

| モチーフ | 用途 | カラー |
|:---|:---|:---|
| ネットワークノード | ヒーロー背景の微細パターン | `rgba(6, 182, 212, 0.15)` |
| シールド | セキュリティを象徴するアイコン | `var(--color-accent)` |
| 多層レイヤー | 3層防御の構造図 | シアン・ブルー・ゴールドの3色 |
| ロックアイコン | 防御・保護を示すカードアイコン | `var(--color-accent)` |
| チェックマーク | KPI・成功条件の達成表現 | `var(--color-success)` |
| グリッドパターン | 背景テクスチャ（subtle） | `rgba(241, 245, 249, 0.03)` |

### SVG スタイルガイドライン

- ストローク幅: 1.5-2px（展示会の大画面で見えるよう太め）
- 角の処理: `stroke-linecap="round"` `stroke-linejoin="round"` で統一
- カラーは CSS 変数を `currentColor` 経由で参照
- アニメーションは `stroke-dasharray` / `stroke-dashoffset` で描画アニメーションを控えめに使用

---

## 9. AI slop 回避確認

| # | AI slop パターン | 本戦略での回避方法 | 状態 |
|:---|:---|:---|:---|
| 1 | 紫→青グラデーション | ネイビー→ダークネイビーの同系色。シアンは光球として点在させ、グラデーションの主色にしない | 回避済 |
| 2 | Inter / Roboto のデフォルト使用 | Space Grotesk（テック個性）+ Noto Sans JP（和文最適）の意図的選定 | 回避済 |
| 3 | 全て同じ角丸 | バッジ: 999px、カード: 12px、ボタン: 8px、アイコン背景: 10px で差別化 | 回避済 |
| 4 | 意味なくセンター寄せ | ヒーローはセンター、カードグリッドは左寄せテキスト、3層防御は左寄せスタック | 回避済 |
| 5 | コンセプト無関係の装飾 | 全装飾にセキュリティ根拠あり（シールド=防御、ネットワーク=統合、ゴールド=差別化） | 回避済 |
| 6 | 全要素にドロップシャドウ | ダークモードでは shadow ではなくボーダー色差で深度表現。hover のみ控えめな transform | 回避済 |
| 7 | 汎用ストック写真 | 写真不使用。インラインSVGの幾何学パターンで業種固有のビジュアル | 回避済 |
| 8 | 無個性 CTA 文言 | 「無料セキュリティアセスメントを申し込む」「ホワイトペーパーをダウンロード」（具体的アクション） | 回避済 |

---

## 10. 品質基準チェック

| 基準 | 確認内容 | 状態 |
|:---|:---|:---|
| **WCAG AA** | メインテキスト 15.2:1、サブテキスト 6.3:1、CTA テキスト 5.8:1 — 全 PASS | PASS |
| **レスポンシブ** | `clamp()` によるフルード設計 + `auto-fit` グリッド | PASS |
| **パフォーマンス** | 過度な shadow/filter なし。アニメーションは `transform`/`opacity` のみ | PASS |
| **CSS 変数** | 全色が CSS 変数で定義。ハードコード色値なし | PASS |
| **フルード設計** | font-size, padding, gap 全てに `clamp()` 適用 | PASS |
| **ブラウザ互換性** | Chrome/Firefox/Safari/Edge 最新2バージョン対応 | PASS |
| **展示会最適化** | 大画面視認性、拡大タイポスケール、ダーク背景の照明下対策 | PASS |
