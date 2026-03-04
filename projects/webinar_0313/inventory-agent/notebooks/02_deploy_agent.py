# Databricks notebook source
# MAGIC %md
# MAGIC # 🚀 在庫分析エージェント — デプロイノートブック
# MAGIC
# MAGIC エージェントを MLflow にログ → Unity Catalog に登録 → Model Serving Endpoint にデプロイ。
# MAGIC
# MAGIC **手順:**
# MAGIC 1. エージェントを MLflow モデルとしてログ
# MAGIC 2. Unity Catalog にモデル登録
# MAGIC 3. Model Serving Endpoint を作成
# MAGIC 4. 動作確認

# COMMAND ----------

# 依存関係のインストール
%pip install openai-agents>=0.0.5 mlflow[databricks]>=2.20.0 databricks-sdk>=0.40.0
dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %md
# MAGIC ## ⚙️ 設定（ここだけ編集してください）

# COMMAND ----------

import os
import sys
import mlflow

# ============================================
# 🔧 ユーザー設定: ワークスペース上の絶対パスを指定
# ============================================
WORKSPACE_ROOT = "/Workspace/Users/s.sekiguchi7056@gmail.com/10.webinar/webinar_mc_and_kc_demo_260313"
AGENT_PATH = f"{WORKSPACE_ROOT}/projects/webinar_0313/inventory-agent"

# Unity Catalog の登録先（実在するカタログ・スキーマを指定）
UC_MODEL_NAME = "prod_manufacturing.gold.inventory_agent"

# Serving Endpoint 名
ENDPOINT_NAME = "inventory-agent-endpoint"

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

load_env_conf(ENV_CONF_PATH)

# Databricks AI Gateway 接続設定
host = spark.conf.get("spark.databricks.workspaceUrl", "")
if host and not host.startswith("https://"):
    host = f"https://{host}"
os.environ["DATABRICKS_HOST"] = host

token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().getOrElse(None)
if token:
    os.environ["DATABRICKS_TOKEN"] = token

# エージェントパスを追加
sys.path.insert(0, AGENT_PATH)

mlflow.set_tracking_uri("databricks")

print(f"✅ セットアップ完了")
print(f"   AGENT_PATH: {AGENT_PATH}")
print(f"   UC_MODEL_NAME: {UC_MODEL_NAME}")
print(f"   ENDPOINT_NAME: {ENDPOINT_NAME}")
print(f"   GENIE_SPACE_ID: {os.environ.get('GENIE_SPACE_ID', '(未設定)')}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 1: エージェントを MLflow モデルとしてログ

# COMMAND ----------

# 実験名を設定
experiment_name = "/tmp/inventory_agent_experiment"
try:
    mlflow.set_experiment(experiment_name)
except Exception:
    mlflow.set_experiment("/tmp/inventory_agent_experiment")

# エージェントのコードパス（agent.py がエントリポイント）
agent_code_path = os.path.join(AGENT_PATH, "agent.py")

# MLflow にエージェントをログ
with mlflow.start_run(run_name="inventory_agent_deploy") as run:
    # エージェントの依存関係を定義
    pip_requirements = [
        "openai-agents>=0.0.5",
        "mlflow[databricks]>=2.20.0",
        "databricks-sdk>=0.40.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
    ]

    # モデルログ
    model_info = mlflow.pyfunc.log_model(
        artifact_path="agent",
        python_model=agent_code_path,
        pip_requirements=pip_requirements,
        # 環境変数の設定
        model_config={
            "GENIE_SPACE_ID": os.environ.get("GENIE_SPACE_ID", ""),
            "AGENT_MODEL": os.environ.get("AGENT_MODEL", "databricks-meta-llama-3-3-70b-instruct"),
        },
    )

    run_id = run.info.run_id
    print(f"✅ モデルログ完了: run_id={run_id}")
    print(f"   artifact_uri: {model_info.model_uri}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2: Unity Catalog にモデル登録

# COMMAND ----------

# UC にモデルを登録
model_version = mlflow.register_model(
    model_uri=f"runs:/{run_id}/agent",
    name=UC_MODEL_NAME,
)

print(f"✅ UC 登録完了: {UC_MODEL_NAME}")
print(f"   バージョン: {model_version.version}")

# バージョンの説明を追加
from mlflow import MlflowClient
client = MlflowClient()
client.update_model_version(
    name=UC_MODEL_NAME,
    version=model_version.version,
    description="在庫分析 AI エージェント — Genie API × OpenAI Agents SDK",
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3: Model Serving Endpoint 作成

# COMMAND ----------

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import (
    EndpointCoreConfigInput,
    ServedEntityInput,
    AutoCaptureConfigInput,
)

w = WorkspaceClient()

# エンドポイント設定
serving_config = EndpointCoreConfigInput(
    served_entities=[
        ServedEntityInput(
            entity_name=UC_MODEL_NAME,
            entity_version=str(model_version.version),
            workload_type="CPU",
            workload_size="Small",
            scale_to_zero_enabled=True,
        )
    ],
    auto_capture_config=AutoCaptureConfigInput(
        catalog_name=UC_MODEL_NAME.split(".")[0],
        schema_name=UC_MODEL_NAME.split(".")[1],
        enabled=True,
    ),
)

# エンドポイント作成 or 更新
try:
    w.serving_endpoints.update_config(
        name=ENDPOINT_NAME,
        served_entities=serving_config.served_entities,
        auto_capture_config=serving_config.auto_capture_config,
    )
    print(f"✅ Endpoint 更新完了: {ENDPOINT_NAME}")
except Exception:
    w.serving_endpoints.create(
        name=ENDPOINT_NAME,
        config=serving_config,
    )
    print(f"✅ Endpoint 作成完了: {ENDPOINT_NAME}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 4: Endpoint の稼働確認

# COMMAND ----------

import time
import json

print("⏳ Endpoint がアクティブになるまで待機中...")
for i in range(60):
    endpoint = w.serving_endpoints.get(ENDPOINT_NAME)
    state = endpoint.state
    if state and state.ready == "READY":
        print(f"✅ Endpoint がアクティブになりました！")
        break
    elif state and state.config_update == "UPDATE_FAILED":
        print(f"❌ Endpoint の作成に失敗しました: {state}")
        break
    print(f"  ... 待機中 ({(i+1)*10}秒経過) — 状態: {state}")
    time.sleep(10)
else:
    print("⚠️ タイムアウト: Databricks UI で確認してください。")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 5: 動作確認テスト

# COMMAND ----------

response = w.serving_endpoints.query(
    name=ENDPOINT_NAME,
    dataframe_records=[{
        "messages": [
            {"role": "user", "content": "在庫総額の概要を教えてください"}
        ]
    }],
)

print("✅ テストリクエスト成功:")
print(json.dumps(response.as_dict(), indent=2, ensure_ascii=False))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 完了
# MAGIC
# MAGIC `inventory-demo-app` の環境変数に以下を設定してください:
# MAGIC ```
# MAGIC SERVING_ENDPOINT=inventory-agent-endpoint
# MAGIC ```
