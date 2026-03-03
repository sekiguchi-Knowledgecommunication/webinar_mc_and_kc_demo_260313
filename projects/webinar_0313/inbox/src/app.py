"""
経営ダッシュボードポータル - メインアプリケーション

Databricks AI/BI ダッシュボードを埋め込み、
Genie による自然言語クエリを可能にするポータルアプリケーション
"""
import os
import sys

# src ディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from components.header import create_header
from components.dashboard_tabs import create_dashboard_tabs
from utils.config import get_dashboard_config, get_app_title, is_debug_mode

# アプリケーション初期化
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP  # Bootstrap Icons
    ],
    suppress_callback_exceptions=True,
    title=get_app_title(),
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

# サーバー（Gunicorn 用）
server = app.server

# ダッシュボード設定を取得
dashboard_config = get_dashboard_config()

# カスタムスタイル
custom_styles = {
    "container": {
        "backgroundColor": "#f8f9fa",
        "minHeight": "100vh"
    },
    "footer": {
        "textAlign": "center",
        "padding": "1rem",
        "color": "#6c757d",
        "fontSize": "0.85rem"
    }
}

# レイアウト定義
app.layout = dbc.Container([
    # ヘッダー
    create_header(),
    
    # メインコンテンツ
    dbc.Row([
        dbc.Col([
            # ダッシュボードタブ
            create_dashboard_tabs(dashboard_config),
            
            # ローディング表示（グローバル）
            dcc.Loading(
                id="loading-indicator",
                type="circle",
                children=html.Div(id="loading-output"),
                color="#0d6efd"
            )
        ], width=12)
    ]),
    
    # フッター
    html.Hr(className="my-4"),
    html.Footer([
        html.P([
            "© 2026 経営ダッシュボードポータル | ",
            html.A(
                "Powered by Databricks",
                href="https://databricks.com",
                target="_blank",
                style={"color": "#6c757d", "textDecoration": "none"}
            )
        ], style=custom_styles["footer"])
    ])
], fluid=True, className="py-3", style=custom_styles["container"])


if __name__ == "__main__":
    debug = is_debug_mode()
    port = int(os.environ.get("PORT", 8080))
    
    print(f"🚀 経営ダッシュボードポータルを起動しています...")
    print(f"   デバッグモード: {debug}")
    print(f"   ポート: {port}")
    print(f"   URL: http://localhost:{port}")
    
    app.run(
        debug=debug,
        host="0.0.0.0",
        port=port
    )
