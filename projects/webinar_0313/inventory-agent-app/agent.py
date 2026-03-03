"""
在庫分析 AI エージェント — メインエージェント定義

OpenAI Agents SDK を使用し、Genie API ツールで
在庫データを自律的に探索・分析するエージェント。
"""

import os
import pathlib
import logging

from agents import Agent, function_tool
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
def get_inventory_overview(question: str = "今月の在庫金額の全体像を教えてください") -> str:
    """
    在庫の全体概要を取得する。在庫総額、カテゴリ別構成比、品目数などを確認する。
    """
    return query_genie(question)


@function_tool
def find_overstock_items(question: str = "過剰在庫品目の一覧を滞留日数の降順で教えてください") -> str:
    """
    過剰在庫品目（滞留日数が長い品目）を検索する。回転率や滞留日数でフィルタリング可能。
    """
    return query_genie(question)


@function_tool
def analyze_demand_gap(question: str = "需要予測と実績の乖離が大きい品目を教えてください") -> str:
    """
    需要予測と実績の乖離を分析する。予測精度やギャップ率でソート可能。
    """
    return query_genie(question)


@function_tool
def check_supplier_leadtime(question: str = "サプライヤー別の平均入荷リードタイムを教えてください") -> str:
    """
    サプライヤー別の入荷リードタイムを確認する。カテゴリ別の比較も可能。
    """
    return query_genie(question)


@function_tool
def custom_data_query(question: str) -> str:
    """
    在庫データに対する任意の分析クエリを実行する。
    自然言語で質問を指定すると、Genie が SQL を生成して実行する。
    """
    return query_genie(question)


# ====================
# エージェント定義
# ====================

# 使用するモデル（Databricks 上の Foundation Model）
MODEL_NAME = os.environ.get(
    "AGENT_MODEL",
    "databricks-meta-llama-3-1-70b-instruct"
)

# 在庫分析エージェント
inventory_agent = Agent(
    name="在庫分析アシスタント",
    instructions=SYSTEM_PROMPT,
    tools=[
        get_inventory_overview,
        find_overstock_items,
        analyze_demand_gap,
        check_supplier_leadtime,
        custom_data_query,
    ],
    model=MODEL_NAME,
)
