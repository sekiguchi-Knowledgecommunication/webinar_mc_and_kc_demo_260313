# Databricks notebook source
# MAGIC %md
# MAGIC # 🧪 在庫分析エージェント — テストノートブック
# MAGIC
# MAGIC このノートブックでは、Databricks Apps にデプロイする前にエージェントの動作を直接テストします。
# MAGIC
# MAGIC **前提条件:**
# MAGIC - `inventory-agent-app/` が Repos に配置済み
# MAGIC - Genie Space が作成済み（`GENIE_SPACE_ID` を下記セルで設定）
# MAGIC - クラスターに `openai-agents>=0.0.5` がインストール済み

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. セットアップ

# COMMAND ----------

# 依存関係のインストール（クラスターに未インストールの場合）
%pip install openai-agents>=0.0.5 mlflow[databricks]>=2.20.0 databricks-sdk>=0.40.0
dbutils.library.restartPython()

# COMMAND ----------

import os
import sys
import asyncio
import logging

# ログ設定（ツール呼び出しが見えるようにINFOレベル）
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")

# inventory-agent-app のパスを追加（Repos 配下のパスに合わせて変更）
AGENT_APP_PATH = "/Workspace/Repos/{your_username}/webinar_mc_and_kc_demo_260313/inventory-agent-app"

# ↓ 実際のパスに変更してください
# AGENT_APP_PATH = "/Workspace/Repos/sekiguchi/webinar_mc_and_kc_demo_260313/inventory-agent-app"

sys.path.insert(0, AGENT_APP_PATH)

# Genie Space ID を設定（Workspace で作成した Genie Space の ID）
os.environ["GENIE_SPACE_ID"] = ""  # ← ここに Genie Space ID を入力

# LLM モデル名（Databricks AI Gateway で利用可能なモデル）
os.environ["AGENT_MODEL"] = "databricks-meta-llama-3-1-70b-instruct"

print("✅ セットアップ完了")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. エージェントの読み込み

# COMMAND ----------

from agent import inventory_agent
from agents import Runner

print(f"✅ エージェント読み込み完了: {inventory_agent.name}")
print(f"   モデル: {inventory_agent.model}")
print(f"   ツール数: {len(inventory_agent.tools)}")
for tool in inventory_agent.tools:
    print(f"   - {tool.name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. テスト実行

# COMMAND ----------

# MAGIC %md
# MAGIC ### テスト 1: メインデモ質問（5ステップ分析）
# MAGIC デモシナリオで使用する主要質問。5つの分析ステップが順番に実行されるかを確認。

# COMMAND ----------

# メインデモ質問
result = asyncio.run(
    Runner.run(
        inventory_agent,
        input="在庫過多の要因を分析し、改善アクションを提案してください"
    )
)

print("=" * 60)
print("📊 最終出力:")
print("=" * 60)
print(result.final_output)

# COMMAND ----------

# ツール呼び出し履歴の確認
print("=" * 60)
print("🔧 ツール呼び出し履歴:")
print("=" * 60)
for i, item in enumerate(result.new_items):
    item_type = type(item).__name__
    print(f"\n--- Item {i+1}: {item_type} ---")
    if hasattr(item, "raw_item"):
        raw = item.raw_item
        if hasattr(raw, "name"):
            print(f"  ツール名: {raw.name}")
        if hasattr(raw, "arguments"):
            print(f"  引数: {raw.arguments[:200]}...")
    if hasattr(item, "output"):
        output = str(item.output)[:300]
        print(f"  出力: {output}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### テスト 2: フォローアップ質問（マルチターン）
# MAGIC 前の分析結果を踏まえたフォローアップ質問。会話コンテキストが維持されるかを確認。

# COMMAND ----------

# フォローアップ質問（マルチターン）
followup_result = asyncio.run(
    Runner.run(
        inventory_agent,
        input=[
            {"role": "user", "content": "在庫過多の要因を分析し、改善アクションを提案してください"},
            {"role": "assistant", "content": result.final_output},
            {"role": "user", "content": "カテゴリBの過剰在庫を減らすために、どのサプライヤーとの発注条件を見直すべきですか？"},
        ]
    )
)

print("=" * 60)
print("📊 フォローアップ応答:")
print("=" * 60)
print(followup_result.final_output)

# COMMAND ----------

# MAGIC %md
# MAGIC ### テスト 3: ストリーミング動作確認
# MAGIC `Runner.run_streamed()` でステップ通知がリアルタイムに流れるかを確認。

# COMMAND ----------

from agents.stream_events import RunItemStreamEvent, RawResponsesStreamEvent

async def test_streaming():
    """ストリーミングモードのテスト"""
    streamed = Runner.run_streamed(
        inventory_agent,
        input="カテゴリ別の在庫金額を教えてください"
    )

    print("🔄 ストリーミングイベント:")
    print("-" * 40)

    text_buffer = ""
    async for event in streamed.stream_events():
        if isinstance(event, RunItemStreamEvent):
            item = event.item
            if hasattr(item, "type"):
                if item.type == "tool_call_item":
                    tool_name = item.raw_item.name if hasattr(item.raw_item, "name") else "unknown"
                    print(f"  🔧 ツール呼び出し: {tool_name}")
                elif item.type == "tool_call_output_item":
                    output = str(item.output)[:100] if hasattr(item, "output") else ""
                    print(f"  📤 ツール出力: {output}")
        elif isinstance(event, RawResponsesStreamEvent):
            data = event.data
            if hasattr(data, "delta") and data.delta:
                if hasattr(data.delta, "content") and data.delta.content:
                    for part in data.delta.content:
                        if hasattr(part, "text") and part.text:
                            text_buffer += part.text
                            print(part.text, end="", flush=True)

    print("\n" + "-" * 40)
    print("✅ ストリーミング完了")
    return streamed

streamed_result = asyncio.run(test_streaming())

# COMMAND ----------

# MAGIC %md
# MAGIC ### テスト 4: シンプルな質問（report_step を使わないケース）

# COMMAND ----------

simple_result = asyncio.run(
    Runner.run(
        inventory_agent,
        input="こんにちは、何ができますか？"
    )
)

print("📊 シンプルな応答:")
print(simple_result.final_output)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. MLflow トレースの確認
# MAGIC
# MAGIC 上のテストを実行した後、MLflow UI でトレースを確認できます:
# MAGIC - 左メニュー → **Experiments** → 該当 experiment を選択
# MAGIC - **Traces** タブで各ツール呼び出しの詳細を確認

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. チェックリスト
# MAGIC
# MAGIC | # | 確認事項 | 状態 |
# MAGIC |:---|:---|:---|
# MAGIC | 1 | メインデモ質問で `report_step` が 5 回呼ばれるか | |
# MAGIC | 2 | `query_inventory_data` でデータが返るか（Genie or フォールバック） | |
# MAGIC | 3 | 最終レポートに「■ 主要な発見」「■ 推奨アクション」があるか | |
# MAGIC | 4 | フォローアップ質問で前の分析コンテキストが維持されるか | |
# MAGIC | 5 | ストリーミングでイベントがリアルタイムに流れるか | |
# MAGIC | 6 | シンプルな質問で `report_step` が呼ばれないか | |
