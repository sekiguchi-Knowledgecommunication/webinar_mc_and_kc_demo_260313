"""
ユーティリティパッケージ
"""
from utils.config import (
    DashboardConfig,
    get_dashboard_config,
    get_app_title,
    is_debug_mode
)

__all__ = [
    "DashboardConfig",
    "get_dashboard_config",
    "get_app_title",
    "is_debug_mode"
]
