"""
在庫分析エージェント — 設定定数

Unity Catalog 登録先、Serving Endpoint 名などの定数を管理。
"""

# Unity Catalog のモデル登録先
UC_CATALOG = "prod_manufacturing"
UC_SCHEMA = "models"
UC_MODEL_NAME = f"{UC_CATALOG}.{UC_SCHEMA}.inventory_agent"

# Serving Endpoint 名
ENDPOINT_NAME = "inventory-agent-endpoint"

# エージェントのバージョン説明
AGENT_DESCRIPTION = "在庫分析 AI エージェント — Genie API × OpenAI Agents SDK"
