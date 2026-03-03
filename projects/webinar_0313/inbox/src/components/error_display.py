"""
エラー表示コンポーネント
URL未設定時などのエラーメッセージを表示
"""
from dash import html
import dash_bootstrap_components as dbc


def create_error_message(dashboard_name: str) -> html.Div:
    """
    エラーメッセージを生成
    
    Args:
        dashboard_name: ダッシュボード名
    
    Returns:
        html.Div: エラーメッセージコンポーネント
    """
    return html.Div([
        html.Div([
            html.I(className="bi bi-exclamation-triangle-fill", 
                   style={"fontSize": "3rem", "color": "#ffc107"}),
        ], className="mb-3"),
        html.H4("ダッシュボードが設定されていません", className="text-warning"),
        html.P(
            f"「{dashboard_name}」ダッシュボードの URL が設定されていません。",
            className="text-muted"
        ),
        html.Hr(),
        html.P("app.yaml の環境変数を設定してください:", className="mb-2"),
        dbc.Card([
            dbc.CardBody([
                html.Code(
                    "DASHBOARD_XXX_URL=https://workspace.cloud.databricks.com/embed/dashboardsv3/xxx",
                    style={"fontSize": "0.85rem"}
                )
            ])
        ], className="bg-dark text-light"),
    ], className="p-5 text-center bg-light rounded", 
       style={"minHeight": "400px", "display": "flex", "flexDirection": "column", 
              "justifyContent": "center", "alignItems": "center"})


def create_loading_placeholder() -> html.Div:
    """
    ローディングプレースホルダーを生成
    
    Returns:
        html.Div: ローディングプレースホルダー
    """
    return html.Div([
        dbc.Spinner(color="primary", size="lg"),
        html.P("ダッシュボードを読み込んでいます...", className="mt-3 text-muted")
    ], className="p-5 text-center", style={"minHeight": "400px"})
