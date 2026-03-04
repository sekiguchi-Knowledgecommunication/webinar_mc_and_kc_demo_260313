"""
在庫分析 AI エージェント — メインエージェント定義

OpenAI Agents SDK を使用し、Genie API ツールで
在庫データを自律的に探索・分析するエージェント。
"""

import os
import pathlib
import logging

from agents import Agent, ModelSettings, function_tool
from tools.genie_tool import query_genie

logger = logging.getLogger(__name__)

# システムプロンプトをファイルから読み込み
PROMPT_PATH = pathlib.Path(__file__).parent / "prompts" / "system_prompt.md"
try:
    SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")
except FileNotFoundError:
    SYSTEM_PROMPT = "あなたは製造業の在庫管理に特化した分析エージェントです。日本語で応答してください。"


# ====================
# ツール定義
# ====================

@function_tool
def query_inventory_data(question: str) -> str:
    """
    在庫データに自然言語で問い合わせる汎用ツール。
    Genie が SQL を自動生成・実行し、結果をテーブル形式で返す。
    在庫サマリ、過剰在庫アラート、回転率分析、リードタイム、
    需要予測と実績の比較など、あらゆる在庫データの問い合わせに使用する。
    """
    return query_genie(question)


@function_tool
def report_step(step_number: int, step_title: str, step_detail: str) -> str:
    """
    分析の各ステップをユーザーに通知するためのツール。
    データ取得や分析を開始する前に必ずこのツールを呼び出して、
    今から何をするかをユーザーに伝えること。

    Args:
        step_number: ステップ番号（1〜5）
        step_title: ステップのタイトル（例: "在庫サマリを取得"）
        step_detail: ステップの詳細説明（例: "カテゴリ別の在庫金額を確認します"）
    """
    logger.info(f"📍 Step {step_number}: {step_title} — {step_detail}")
    return f"✅ Step {step_number}: {step_title}"


# ====================
# エージェント定義
# ====================

# 使用するモデル（Databricks AI Gateway 経由）
MODEL_NAME = os.environ.get(
    "AGENT_MODEL",
    "databricks-meta-llama-3-1-70b-instruct"
)

# 在庫分析エージェント
inventory_agent = Agent(
    name="在庫分析アシスタント",
    instructions=SYSTEM_PROMPT,
    tools=[
        query_inventory_data,
        report_step,
    ],
    model=MODEL_NAME,
    model_settings=ModelSettings(
        max_tokens=4096,
    ),
)
