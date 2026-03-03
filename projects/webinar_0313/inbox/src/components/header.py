"""
ヘッダーコンポーネント
アプリケーションのヘッダー部分を表示
"""
from dash import html
import dash_bootstrap_components as dbc

from utils.config import get_app_title


def create_header() -> dbc.Row:
    """
    ヘッダーを生成
    
    Returns:
        dbc.Row: ヘッダーコンポーネント
    """
    title = get_app_title()
    
    return dbc.Row([
        dbc.Col([
            html.H1([
                html.Span("📊 ", style={"marginRight": "10px"}),
                title
            ], className="mb-0", style={"fontSize": "1.75rem"}),
            html.P(
                "経営数値をリアルタイムで分析 | Genie で自然言語クエリ",
                className="text-muted mb-0",
                style={"fontSize": "0.9rem"}
            )
        ], width=12)
    ], className="align-items-center py-3 px-3 bg-light rounded mb-3")
