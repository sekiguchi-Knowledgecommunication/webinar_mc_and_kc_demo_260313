# Databricks notebook source
# MAGIC %md
# MAGIC # 🧪 在庫分析エージェント — テストノートブック
# MAGIC
# MAGIC エージェント単体の動作テスト。Serving Endpoint デプロイ前の品質確認に使用。
# MAGIC
# MAGIC **前提**: クラスターに `openai-agents>=0.0.5` インストール済

# COMMAND ----------

# 依存関係のインストール
%pip install openai-agents>=0.0.5 mlflow[databricks]>=2.20.0 databricks-sdk>=0.40.0 nest_asyncio
dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %md
# MAGIC ## ⚙️ 設定（ここだけ編集してください）

# COMMAND ----------

import os
import sys
import logging
import nest_asyncio

nest_asyncio.apply()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")

# ============================================
# 🔧 ユーザー設定: ワークスペース上の絶対パスを指定
# ============================================
WORKSPACE_ROOT = "/Workspace/Users/s.sekiguchi7056@gmail.com/10.webinar/webinar_mc_and_kc_demo_260313"
AGENT_PATH = f"{WORKSPACE_ROOT}/projects/webinar_0313/inventory-agent"

# ============================================
# 📄 env.conf から設定を読み込み
# ============================================
ENV_CONF_PATH = f"{WORKSPACE_ROOT}/projects/webinar_0313/env.conf"

def load_env_conf(path):
    """env.conf ファイルから KEY=VALUE を読み込んで環境変数に設定"""
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()
        print(f"✅ env.conf 読み込み完了: {path}")
    except FileNotFoundError:
        print(f"⚠️ env.conf が見つかりません: {path}")
        print("   GENIE_SPACE_ID, AGENT_MODEL を手動で設定してください")

load_env_conf(ENV_CONF_PATH)

# エージェントのパスを追加
sys.path.insert(0, AGENT_PATH)

# Databricks AI Gateway 接続設定
host = spark.conf.get("spark.databricks.workspaceUrl", "")
if host and not host.startswith("https://"):
    host = f"https://{host}"
os.environ["DATABRICKS_HOST"] = host

token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().getOrElse(None)
if token:
    os.environ["DATABRICKS_TOKEN"] = token

print(f"✅ セットアップ完了")
print(f"   AGENT_PATH: {AGENT_PATH}")
print(f"   GENIE_SPACE_ID: {os.environ.get('GENIE_SPACE_ID', '(未設定)')}")
print(f"   AGENT_MODEL: {os.environ.get('AGENT_MODEL', '(未設定)')}")
print(f"   DATABRICKS_HOST: {os.environ.get('DATABRICKS_HOST', '(未設定)')}")
print(f"   DATABRICKS_TOKEN: {'***設定済み' if os.environ.get('DATABRICKS_TOKEN') else '(未設定)'}")

# COMMAND ----------

from agent import inventory_agent
from agents import Runner

print(f"✅ エージェント: {inventory_agent.name}")
print(f"   モデル: {inventory_agent.model}")
print(f"   ツール: {[t.name for t in inventory_agent.tools]}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## テスト 1: メインデモ質問（5ステップ分析）

# COMMAND ----------

import asyncio

result = asyncio.run(
    Runner.run(inventory_agent, input="在庫過多の要因を分析し、改善アクションを提案してください")
)
print("=" * 60)
print("📊 最終出力:")
print("=" * 60)
print(result.final_output)

# COMMAND ----------

# ツール呼び出し履歴
print("🔧 ツール呼び出し履歴:")
for i, item in enumerate(result.new_items):
    item_type = type(item).__name__
    if hasattr(item, "raw_item") and hasattr(item.raw_item, "name"):
        print(f"  {i+1}. {item.raw_item.name}")
    elif hasattr(item, "output"):
        print(f"  {i+1}. output: {str(item.output)[:100]}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## テスト 2: フォローアップ質問（マルチターン）

# COMMAND ----------

followup = asyncio.run(
    Runner.run(inventory_agent, input=[
        {"role": "user", "content": "在庫過多の要因を分析し、改善アクションを提案してください"},
        {"role": "assistant", "content": result.final_output},
        {"role": "user", "content": "カテゴリBの過剰在庫を減らすために、どのサプライヤーとの発注条件を見直すべきですか？"},
    ])
)
print("📊 フォローアップ応答:")
print(followup.final_output)

# COMMAND ----------

# MAGIC %md
# MAGIC ## テスト 3: シンプルな質問

# COMMAND ----------

simple = asyncio.run(
    Runner.run(inventory_agent, input="あなたは何ができるエージェントですか？在庫分析の機能を教えてください。")
)
print("📊 シンプルな応答:")
print(simple.final_output)

# COMMAND ----------

# MAGIC %md
# MAGIC ## チェックリスト
# MAGIC | # | 確認事項 | 状態 |
# MAGIC |:---|:---|:---|
# MAGIC | 1 | メインデモ質問で `report_step` が呼ばれるか | |
# MAGIC | 2 | `query_inventory_data` でデータが返るか | |
# MAGIC | 3 | 最終レポートに「■ 主要な発見」「■ 推奨アクション」があるか | |
# MAGIC | 4 | フォローアップで前のコンテキストが維持されるか | |
# MAGIC | 5 | シンプルな質問で `report_step` が呼ばれないか | |
