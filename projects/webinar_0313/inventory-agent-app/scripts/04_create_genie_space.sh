#!/bin/bash
# ============================================================
# Genie Space 作成スクリプト（内部形式準拠版）
# ============================================================
export PATH="$HOME/.local/bin:$PATH"

CATALOG="apps_demo_catalog"
SCHEMA="webinar_demo_0313"
WAREHOUSE_ID="863ce5ef78045c29"

echo "========================================================"
echo " Genie Space 作成（内部形式準拠版）"
echo "========================================================"

python3 << PYEOF
import json, uuid

catalog = "$CATALOG"
schema = "$SCHEMA"

def gen_id():
    return uuid.uuid4().hex[:32]

# serialized_space の内部形式（Bakehouse Space から逆引き）
serialized = {
    "version": 2,
    "config": {
        "sample_questions": [
            {
                "id": gen_id(),
                "question": ["今月の在庫総額をカテゴリ別に教えてください"]
            },
            {
                "id": gen_id(),
                "question": ["過剰在庫品目の一覧を滞留日数の降順で表示してください"]
            },
            {
                "id": gen_id(),
                "question": ["カテゴリ別の在庫回転率の推移を教えてください"]
            },
            {
                "id": gen_id(),
                "question": ["サプライヤー別の平均リードタイムを教えてください"]
            },
            {
                "id": gen_id(),
                "question": ["在庫金額が最も大きい品目トップ10を教えてください"]
            }
        ]
    },
    "data_sources": {
        "tables": [
            {"identifier": f"{catalog}.{schema}.inventory_summary"},
            {"identifier": f"{catalog}.{schema}.turnover_analysis"},
            {"identifier": f"{catalog}.{schema}.overstock_alert"},
            {"identifier": f"{catalog}.{schema}.receipts"}
        ]
    },
    "instructions": {
        "text_instructions": [
            {
                "id": gen_id(),
                "content": [
                    "あなたは製造業の在庫管理を支援する分析アシスタントです。\\n",
                    "\\n",
                    "テーブル情報:\\n",
                    "- inventory_summary: 品目×月の在庫サマリ。カラム: month, item_id, item_name, category, avg_inventory_value, avg_inventory_qty\\n",
                    "- turnover_analysis: カテゴリ×月の在庫回転率分析。カラム: month, category, avg_turnover_rate\\n",
                    "- overstock_alert: 過剰在庫アラート。カラム: item_id, item_name, category, turnover_rate, days_on_hand, avg_inventory_value\\n",
                    "- receipts: 入荷データ。カラム: supplier_id, item_id, lead_time_actual_days, receipt_date\\n",
                    "\\n",
                    "回答は常に日本語で行ってください。\\n",
                    "金額は日本円で表示し、カンマ区切りで読みやすくしてください。\\n",
                    "パーセンテージは小数点1桁まで表示してください。"
                ]
            }
        ]
    }
}

payload = {
    "title": "在庫分析アシスタント",
    "description": "在庫データに自然言語で質問できる分析スペースです。在庫総額、回転率、過剰在庫、サプライヤーリードタイムなどを分析できます。",
    "warehouse_id": "$WAREHOUSE_ID",
    "serialized_space": json.dumps(serialized, ensure_ascii=False)
}

with open("/tmp/genie_payload.json", "w") as f:
    json.dump(payload, f, ensure_ascii=False)

print("OK: ペイロード保存完了")
print(f"  テーブル: {len(serialized['data_sources']['tables'])} 個")
print(f"  サンプル質問: {len(serialized['config']['sample_questions'])} 個")
print(f"  serialized_space サイズ: {len(payload['serialized_space'])} 文字")
PYEOF

echo ""
echo "📊 Genie Space を作成中 (POST)..."
databricks api post /api/2.0/genie/spaces --json @/tmp/genie_payload.json

echo ""
echo "========================================================"
echo "完了！"
echo "========================================================"
