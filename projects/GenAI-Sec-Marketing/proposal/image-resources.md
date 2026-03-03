# 画像リソースガイド: GenAI セキュリティガードレール設計サービス — 展示会ブース LP

> **コンセプトキーワード**: 信頼, 先進性, 防御, 透明性, 日本初
> **カラーパレット**: ダークネイビー(`#0B1120`) + シアン(`#06B6D4`) + ブルー(`#2563EB`) + ゴールド(`#F59E0B`)
> **生成日**: 2026-02-22

---

## 注: 展示会LP での画像利用方針

本LPは **単一HTML + Tailwind CSS CDN + インラインSVG** の技術制約がある。写真やラスター画像は外部依存を増やすため、**主にインラインSVGとCSSグラデーションで視覚表現する方針**を推奨する。

ただし、以下の用途では写真・AI生成画像が効果的:
- OGP/SNSシェア画像（HTML外部の静的アセット）
- 会場配布資料・パネル用ビジュアル
- 将来のWebサイト展開用アセットの事前準備
- ヒーロー背景の代替案（SVGでは表現しきれない質感が必要な場合）

---

## 1. ストックフォト検索キーワード

### 検索先

| サービス | URL テンプレート | 特徴 |
|:---|:---|:---|
| Unsplash | `https://unsplash.com/s/photos/{keyword}` | 高品質、無料、商用利用可 |
| Pexels | `https://www.pexels.com/search/{keyword}/` | 動画もあり、無料、商用利用可 |

### セクション別キーワード

#### ヒーロー背景（展示会パネル・OGP 向け）

| 検索キーワード（英語） | 検索キーワード（日本語） | 推奨サイズ | フィルター |
|:---|:---|:---|:---|
| `"dark server room blue light neon"` | `"サーバールーム 青い光"` | 1920x1080以上 | Landscape, Dark |
| `"cybersecurity network dark abstract"` | `"サイバーセキュリティ ネットワーク 暗い"` | 1920x1080以上 | Landscape, Dark |
| `"abstract dark navy geometric grid technology"` | `"幾何学模様 テクノロジー 暗い"` | 1920x1080以上 | Landscape, Dark |
| `"digital shield protection dark background"` | `"デジタル シールド 防御"` | 1920x1080以上 | Landscape, Dark |

#### セクション背景（3層防御図解・ソリューション概要）

| 検索キーワード（英語） | 検索キーワード（日本語） | 推奨サイズ | フィルター |
|:---|:---|:---|:---|
| `"layers stacked transparent dark"` | `"レイヤー 多層 透明"` | 1920x800以上 | Landscape |
| `"abstract circuit board dark blue close up"` | `"基板 回路 暗い青"` | 1920x800以上 | Landscape, Dark |
| `"data center corridor dark blue led"` | `"データセンター 通路 青い LED"` | 1920x800以上 | Landscape, Dark |

#### 特徴カード（アイコン代替・雰囲気素材）

| 検索キーワード（英語） | 検索キーワード（日本語） | 推奨サイズ | フィルター |
|:---|:---|:---|:---|
| `"lock padlock digital dark navy"` | `"錠前 デジタル ダーク"` | 800x600 | — |
| `"audit document checklist dark"` | `"監査 書類 チェックリスト"` | 800x600 | — |
| `"radar scan dark blue"` | `"レーダー スキャン 暗い青"` | 800x600 | — |
| `"shield hologram dark technology"` | `"シールド ホログラム テクノロジー"` | 800x600 | — |

#### CTA 背景

| 検索キーワード（英語） | 検索キーワード（日本語） | 推奨サイズ | フィルター |
|:---|:---|:---|:---|
| `"abstract blue gradient dark minimal"` | `"抽象 青 グラデーション ダーク"` | 1920x600以上 | Landscape, Dark |
| `"night sky deep blue dark horizon"` | `"夜空 深い青 暗い 地平線"` | 1920x600以上 | Landscape, Dark |

#### OGP / SNS シェア画像用

| 検索キーワード（英語） | 検索キーワード（日本語） | 推奨サイズ | フィルター |
|:---|:---|:---|:---|
| `"cybersecurity ai dark navy abstract"` | `"サイバーセキュリティ AI ダーク"` | 1200x630 | Landscape, Dark |
| `"digital fortress dark blue technology abstract"` | `"デジタル 要塞 テクノロジー"` | 1200x630 | Landscape, Dark |

### 検索の組み合わせ Tips

検索結果が不十分な場合、以下の修飾語を追加する:

- **スタイル修飾**: `dark`, `minimal`, `abstract`, `neon`, `futuristic`, `low key`, `moody`
- **セキュリティ業種修飾**: `cybersecurity`, `encryption`, `firewall`, `defense`, `protection`, `shield`, `audit`, `compliance`
- **テクノロジー修飾**: `AI`, `machine learning`, `neural network`, `data flow`, `cloud computing`
- **除外キーワード**: 検索結果にノイズが多い場合
  - `-person`（人物写真を除外、汎用感を避ける）
  - `-office`（オフィス写真を除外）
  - `-handshake`（握手写真を除外、AI slop 回避）

---

## 2. AI 画像生成プロンプト

### 共通スタイル指示

以下のスタイル指示を全プロンプト末尾に付加し、LP全体の統一感を保つ:

```
Style: Technical cybersecurity visualization with clean geometric forms,
precise lines and angular shapes suggesting engineered defense systems.
Color palette: Deep navy (#0B1120) as dominant background, cyan (#06B6D4)
for energy and highlight accents, blue (#2563EB) for structural elements,
muted slate gray for depth. No purple, no magenta, no warm tones except
for sparse gold (#F59E0B) accents indicating distinction.
Mood: Authoritative trust, technological sophistication, multi-layered defense.
Lighting: Low ambient with focused cyan and blue directional light sources
creating depth through illumination rather than shadow.
```

### ネガティブプロンプト共通

```
--no people, faces, hands, text, letters, watermark, logo, bright colors,
purple gradient, warm lighting, organic shapes, bokeh, lens flare, stock photo look
```

---

### 2.1 ヒーロービジュアル

**用途**: ファーストビュー背景 / 展示会パネル / OGP 画像のベース
**推奨サイズ**: 1920x1080 / 16:9

#### Midjourney

```
Isometric dark navy environment showing a three-layered hexagonal shield structure
protecting a central AI processing core, each defense layer rendered as translucent
cyan geometric mesh with data streams flowing between layers, the outermost layer
glowing with cyan (#06B6D4) edge light, middle layer pulsing with blue (#2563EB)
structural nodes, innermost layer featuring a gold (#F59E0B) lock icon,
background is deep dark navy (#0B1120) with subtle grid pattern fading into
darkness, photorealistic 3D render with clean hard edges
--ar 16:9 --s 250 --q 2 --no people, faces, text, purple, warm colors, organic shapes
```

```
Top-down view of an abstract dark navy circuit board landscape where data pathways
glow in cyan (#06B6D4), forming a network topology of interconnected shield nodes,
each node is a hexagonal structure with blue (#2563EB) borders, three distinct
elevation layers visible through transparency, sparse gold (#F59E0B) indicator
lights at critical junctions, ultra-clean technical visualization,
matte dark navy (#0B1120) background
--ar 16:9 --s 250 --q 2 --no people, text, purple gradient, warm lighting, bokeh
```

#### DALL-E / GPT-4o

```
Create a wide-format digital illustration (1792x1024) of a cybersecurity defense
system visualization. The scene shows three concentric translucent hexagonal shield
layers floating in a deep dark navy (#0B1120) void. The outer shield layer has
glowing cyan (#06B6D4) edges with flowing data particles. The middle layer shows
blue (#2563EB) geometric nodes connected by thin lines. The inner layer contains
a small gold (#F59E0B) lock symbol. Thin cyan grid lines extend into the background.
The style is clean, technical, and precise — no organic shapes, no people, no text.
The mood is authoritative and sophisticated. Lighting comes from the cyan and blue
elements themselves, casting subtle reflections on the shield surfaces.
```

```
Generate a wide-format image (1792x1024) depicting an abstract aerial view of a
dark navy (#0B1120) digital landscape. Geometric pathways glow in cyan (#06B6D4)
forming a network of connected defense nodes. The nodes are hexagonal with
blue (#2563EB) outlines. Three visual depth layers are visible — the closest layer
is brightest, middle is semi-transparent, furthest is faint. A few gold (#F59E0B)
accent points mark critical intersections. Style: technical schematic rendered
in 3D with clean lines. No people, no text, no purple, no warm colors.
```

---

### 2.2 セクションイラスト / 概念図

**用途**: 3層防御図解、ソリューション概要セクションの装飾
**推奨サイズ**: 800x600 / 4:3

#### Midjourney

```
Technical cutaway diagram of a three-layer AI security system, side view,
Layer 1 (bottom): real-time inference guard shown as a horizontal cyan (#06B6D4)
barrier with scanning beams, Layer 2 (middle): red teaming layer shown as
blue (#2563EB) probing arrows testing the defenses from outside,
Layer 3 (top): audit trail layer shown as gold (#F59E0B) document icons
with connecting lines to a central log, dark navy (#0B1120) background,
clean technical illustration style with labeled markers
--ar 4:3 --s 200 --no people, text, purple, warm tones, realistic photo
```

```
Abstract representation of four platform logos merging into a unified security
mesh, four distinct geometric shapes (hexagon, octagon, diamond, circle) connected
by cyan (#06B6D4) data streams converging at a central blue (#2563EB) shield node,
dark navy (#0B1120) background with subtle grid, clean vector-style 3D rendering,
precision engineering aesthetic
--ar 4:3 --s 200 --no people, text, purple, warm colors
```

#### DALL-E / GPT-4o

```
Create a technical illustration (1024x1024) showing a cross-section of a
three-layer AI security defense system against a dark navy (#0B1120) background.
Bottom layer: a horizontal cyan (#06B6D4) barrier labeled "Real-time Defense"
with small scanning beam icons. Middle layer: blue (#2563EB) arrows representing
automated red teaming, pointing inward to test the barrier. Top layer: gold
(#F59E0B) document/audit icons connected by thin lines to a central log symbol.
Each layer is separated by subtle horizontal lines. Style: clean technical diagram
with geometric shapes, no organic forms. No people, no text within the image.
```

---

### 2.3 カード / アイキャッチ画像

**用途**: 特徴カード背景、課題セクションのアイコン代替
**推奨サイズ**: 800x600 / 4:3

#### Midjourney — 課題カード用（4枚セット）

```
Minimal icon illustration: a rapidly spinning technology gear with trailing
motion lines, surrounded by fragmented code symbols falling apart,
dark navy (#0B1120) background, single cyan (#06B6D4) accent color,
clean geometric style, represents "rapid technology evolution challenge"
--ar 4:3 --s 150 --no people, text, purple, warm colors
```

```
Minimal icon illustration: four disconnected geometric nodes (hexagon, circle,
triangle, square) with broken connection lines between them,
dark navy (#0B1120) background, blue (#2563EB) and muted gray colors,
clean geometric style, represents "team coordination gap"
--ar 4:3 --s 150 --no people, text, purple, warm colors
```

```
Minimal icon illustration: upward-pointing cost arrow piercing through
stacked currency layers, each layer cracking under pressure,
dark navy (#0B1120) background, red (#EF4444) arrow with blue (#2563EB) layers,
clean geometric style, represents "escalating security costs"
--ar 4:3 --s 150 --no people, text, purple, warm colors
```

```
Minimal icon illustration: an empty chair behind a desk with a floating
shield outline that has a question mark in the center,
dark navy (#0B1120) background, cyan (#06B6D4) shield outline,
clean geometric style, represents "AI security talent shortage"
--ar 4:3 --s 150 --no people, text, purple, warm colors
```

#### Midjourney — 特長カード用（3枚セット）

```
Minimal icon illustration: a golden (#F59E0B) badge with "1st" engraved,
surrounded by four interconnected platform icons forming a unified ring,
dark navy (#0B1120) background, cyan (#06B6D4) connection lines,
clean geometric style, represents "Japan's first integrated AI security consulting"
--ar 4:3 --s 150 --no people, text, purple, warm colors
```

```
Minimal icon illustration: a scientific beaker with measurement marks
connected to a checkmark flag at the finish line of a timeline arrow,
dark navy (#0B1120) background, blue (#2563EB) beaker with cyan (#06B6D4) flag,
clean geometric style, represents "PoC-driven verification approach"
--ar 4:3 --s 150 --no people, text, purple, warm colors
```

```
Minimal icon illustration: a document stack with an audit stamp seal on top,
connected by a single continuous line to a shield icon below,
dark navy (#0B1120) background, gold (#F59E0B) audit stamp with blue (#2563EB) shield,
clean geometric style, represents "one-stop audit compliance support"
--ar 4:3 --s 150 --no people, text, purple, warm colors
```

#### DALL-E / GPT-4o — カード用

```
Create a set of 4 minimal icon illustrations (1024x1024 each) on dark navy
(#0B1120) backgrounds, using only cyan (#06B6D4), blue (#2563EB), and white as
accent colors. Clean geometric vector style, no organic shapes, no text.
Icon 1: A rapidly spinning gear with trailing motion arcs, surrounded by
fragmenting code brackets — representing rapid technology change.
Icon 2: Four disconnected geometric nodes with broken link lines —
representing team coordination gaps.
Icon 3: An upward cost arrow piercing through cracking horizontal layers —
representing escalating costs.
Icon 4: An empty shield outline with a question mark inside —
representing talent shortage.
```

---

### 2.4 OGP / SNS シェア画像

**用途**: SNS シェア時のプレビュー画像、展示会告知用
**推奨サイズ**: 1200x630

#### Midjourney

```
Social media preview card design: three-layered translucent hexagonal shield
floating over a dark navy (#0B1120) field with subtle cyan (#06B6D4) grid lines,
a single gold (#F59E0B) badge element in the upper left corner suggesting
"first in Japan", clean negative space on the right side for text overlay,
the shield structure glows with blue (#2563EB) and cyan edges,
professional technical visualization
--ar 1200:630 --s 200 --no people, text, purple, warm colors, organic shapes
```

#### DALL-E / GPT-4o

```
Create a landscape image (1792x1024) designed for social media sharing.
Left two-thirds: a three-layered translucent hexagonal shield structure
glowing with cyan (#06B6D4) edges and blue (#2563EB) structural nodes,
floating above a dark navy (#0B1120) surface with faint grid lines.
Right one-third: clean dark navy space (for text overlay in post-production).
A small gold (#F59E0B) hexagonal badge element in the upper left corner.
Style: clean technical 3D visualization. No text, no people, no purple.
```

---

### 2.5 展示会ブースパネル用

**用途**: 展示会ブースの背面パネル、のぼり、配布物の背景
**推奨サイズ**: 2400x3600（縦長A1相当）/ 2:3

#### Midjourney

```
Vertical format abstract cybersecurity visualization: a towering hexagonal
shield structure viewed from below looking up, multiple defense layers stacked
vertically with cyan (#06B6D4) energy flowing between them, data streams
ascending through the layers, each layer increasingly transparent toward the top,
dark navy (#0B1120) background deepening at the edges, blue (#2563EB) structural
framework, sparse gold (#F59E0B) indicator nodes, dramatic upward perspective
creating a sense of protection and scale, clean 3D technical rendering
--ar 2:3 --s 250 --q 2 --no people, text, purple, warm colors
```

---

## 3. 画像利用ガイドライン

### ライセンス確認チェックリスト

- [ ] **Unsplash**: Unsplash License 確認（商用利用可、クレジット不要だが推奨）
- [ ] **Pexels**: Pexels License 確認（商用利用可、クレジット不要）
- [ ] **Midjourney**: 有料プラン加入確認（商用利用は有料プランが必須）
- [ ] **DALL-E / GPT-4o**: OpenAI 利用規約確認（生成画像の商用利用条件）
- [ ] 展示会配布物に使用する場合、印刷品質（300dpi以上）の確保
- [ ] クライアント（ナレコム）へのライセンス情報の共有を準備した
- [ ] AI生成画像を使用する場合、社内ポリシーに準拠しているか確認

### 画像最適化

| 形式 | 用途 | 目安サイズ | 備考 |
|:---|:---|:---|:---|
| **SVG** | インラインアイコン・装飾・背景パターン | N/A | LP内のメイン視覚要素。ベクターのため拡大しても鮮明 |
| **WebP** | ヒーロー背景（写真使用時）・カード画像 | 100-300KB | `<picture>` タグで AVIF フォールバック |
| **AVIF** | モダンブラウザ向け最適化 | 50-200KB | Chrome 85+, Firefox 93+, Safari 16.1+ |
| **PNG** | OGP 画像・ロゴ（透過あり） | 200-500KB | SNSプラットフォーム互換性のため PNG を使用 |
| **JPEG** | 展示会印刷物用 | — | 300dpi以上、CMYK変換が必要な場合あり |

### HTML 内での画像読み込み最適化

```html
<!-- 写真を使用する場合の推奨実装 -->
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" alt="" loading="lazy"
       width="1920" height="1080"
       decoding="async">
</picture>
```

### 展示会LP固有の注意事項

1. **単一HTML制約**: 画像はBase64エンコードでインライン化するか、外部URLから読み込む。ファイルサイズが大きくなるため、可能な限りインラインSVGを優先する
2. **展示会Wi-Fi**: 会場のネットワークが不安定な場合を考慮し、重要な視覚要素はインラインSVGまたはCSSで実現する。外部画像への依存を最小限にする
3. **大画面表示**: 展示会ディスプレイ（40-60インチ、1080p-4K）でラスター画像を使用する場合、解像度不足に注意。SVGまたは2x解像度の画像を用意する

---

## 4. インラインSVGテンプレート（LP用推奨アプローチ）

展示会LPでは外部画像依存を避けるため、以下のインラインSVGパターンを活用する。

### 4.1 ヒーロー背景グリッドパターン

```svg
<svg class="absolute inset-0 w-full h-full" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none"
            stroke="rgba(241,245,249,0.03)" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#grid)"/>
</svg>
```

### 4.2 シールドアイコン（セクション用）

```svg
<svg width="48" height="48" viewBox="0 0 48 48" fill="none"
     xmlns="http://www.w3.org/2000/svg">
  <path d="M24 4L6 12v12c0 11.1 7.7 21.5 18 24
           10.3-2.5 18-12.9 18-24V12L24 4z"
        stroke="currentColor" stroke-width="2"
        stroke-linecap="round" stroke-linejoin="round"
        fill="none" opacity="0.9"/>
  <path d="M16 24l5 5 11-11"
        stroke="currentColor" stroke-width="2.5"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

### 4.3 ネットワークノード装飾（ヒーロー背景用）

```svg
<svg class="absolute inset-0 w-full h-full opacity-20"
     viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <!-- ノード -->
  <circle cx="200" cy="150" r="4" fill="#06B6D4"/>
  <circle cx="400" cy="100" r="3" fill="#06B6D4"/>
  <circle cx="600" cy="200" r="5" fill="#2563EB"/>
  <circle cx="300" cy="350" r="4" fill="#06B6D4"/>
  <circle cx="500" cy="400" r="3" fill="#2563EB"/>
  <circle cx="150" cy="450" r="4" fill="#06B6D4"/>
  <circle cx="650" cy="350" r="3" fill="#06B6D4"/>
  <!-- コネクションライン -->
  <line x1="200" y1="150" x2="400" y2="100"
        stroke="#06B6D4" stroke-width="0.5" opacity="0.3"/>
  <line x1="400" y1="100" x2="600" y2="200"
        stroke="#06B6D4" stroke-width="0.5" opacity="0.3"/>
  <line x1="200" y1="150" x2="300" y2="350"
        stroke="#2563EB" stroke-width="0.5" opacity="0.2"/>
  <line x1="300" y1="350" x2="500" y2="400"
        stroke="#2563EB" stroke-width="0.5" opacity="0.2"/>
  <line x1="600" y1="200" x2="650" y2="350"
        stroke="#06B6D4" stroke-width="0.5" opacity="0.3"/>
  <line x1="150" y1="450" x2="300" y2="350"
        stroke="#06B6D4" stroke-width="0.5" opacity="0.2"/>
</svg>
```

---

## 5. プロンプトとパレットの整合性確認

| プロンプト用途 | 使用カラー | パレット整合 | ネガティブ制約 |
|:---|:---|:---|:---|
| ヒーロー | ダークネイビー + シアン + ブルー + ゴールド | 全色一致 | 紫・暖色・人物を除外 |
| セクション | ダークネイビー + シアン + ブルー | 3色一致 | 紫・暖色を除外 |
| カード（課題） | ダークネイビー + シアン or ブルー（単色アクセント） | 2色一致 | 紫・暖色を除外 |
| カード（特長） | ダークネイビー + シアン + ブルー + ゴールド | 全色一致 | 紫・暖色を除外 |
| OGP | ダークネイビー + シアン + ブルー + ゴールド | 全色一致 | 紫・暖色を除外 |
| 展示会パネル | ダークネイビー + シアン + ブルー + ゴールド | 全色一致 | 紫・暖色を除外 |

> 全プロンプトで共通スタイル指示を末尾に付加し、紫(`purple`)を明示的にネガティブ指定。AI slop 的な紫→青グラデーションを確実に回避。
