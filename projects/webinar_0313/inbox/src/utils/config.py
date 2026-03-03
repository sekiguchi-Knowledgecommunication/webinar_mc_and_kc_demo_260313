"""
設定管理モジュール
環境変数からダッシュボード設定を取得
"""
import os
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DashboardConfig:
    """ダッシュボード設定"""
    name: str
    display_name: str
    url: Optional[str]
    icon: str = "📊"


def get_dashboard_config() -> List[DashboardConfig]:
    """
    環境変数からダッシュボード設定を取得
    
    Returns:
        List[DashboardConfig]: ダッシュボード設定のリスト
    """
    return [
        DashboardConfig(
            name="sales",
            display_name="売上分析",
            url=os.environ.get("DASHBOARD_SALES_URL"),
            icon="💰"
        ),
        DashboardConfig(
            name="finance",
            display_name="財務分析",
            url=os.environ.get("DASHBOARD_FINANCE_URL"),
            icon="📈"
        ),
        DashboardConfig(
            name="kpi",
            display_name="KPI",
            url=os.environ.get("DASHBOARD_KPI_URL"),
            icon="🎯"
        ),
    ]


def get_app_title() -> str:
    """アプリタイトルを取得"""
    return os.environ.get("APP_TITLE", "経営ダッシュボードポータル")


def is_debug_mode() -> bool:
    """デバッグモードかどうか"""
    return os.environ.get("APP_DEBUG", "false").lower() == "true"
