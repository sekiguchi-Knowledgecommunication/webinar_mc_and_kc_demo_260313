"""
ダッシュボードタブコンポーネント
複数ダッシュボードのタブ切り替えを実現
"""
from dash import html
import dash_bootstrap_components as dbc
from typing import List

from utils.config import DashboardConfig
from components.error_display import create_error_message


def create_dashboard_iframe(url: str) -> html.Iframe:
    """
    ダッシュボード表示用 iframe を生成
    
    Args:
        url: ダッシュボード埋め込み URL
    
    Returns:
        html.Iframe: iframe コンポーネント
    """
    return html.Iframe(
        src=url,
        style={
            "width": "100%",
            "height": "calc(100vh - 250px)",
            "border": "none",
            "borderRadius": "8px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
        },
        allow="fullscreen"
    )


def create_dashboard_tabs(configs: List[DashboardConfig]) -> dbc.Tabs:
    """
    ダッシュボードタブを生成
    
    Args:
        configs: ダッシュボード設定リスト
    
    Returns:
        dbc.Tabs: タブコンポーネント
    """
    tabs = []
    first_active_tab = None
    
    for config in configs:
        # URLがある場合は iframe、ない場合はエラーメッセージ
        content = (
            create_dashboard_iframe(config.url) 
            if config.url 
            else create_error_message(config.display_name)
        )
        
        tab_id = f"tab-{config.name}"
        
        # 最初に有効な（URLが設定された）タブを記憶
        if config.url and first_active_tab is None:
            first_active_tab = tab_id
        
        tabs.append(
            dbc.Tab(
                content,
                label=f"{config.icon} {config.display_name}",
                tab_id=tab_id,
                className="p-0",
                label_style={"fontSize": "1rem", "fontWeight": "500"}
            )
        )
    
    # デフォルトで最初のタブをアクティブに
    active_tab = first_active_tab or "tab-sales"
    
    return dbc.Tabs(
        tabs,
        id="dashboard-tabs",
        active_tab=active_tab,
        className="mb-3"
    )
