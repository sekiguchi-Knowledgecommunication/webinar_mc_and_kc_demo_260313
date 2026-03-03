"""
在庫分析エージェント — メインアプリケーション

MLflow AgentServer を使用して FastAPI サーバーを起動。
組み込みチャット UI 付き。
"""

import os
import logging
import asyncio

import mlflow
from mlflow.pyfunc import ResponsesAgent
from mlflow.types.agent import (
    ChatAgentMessage,
    ChatAgentResponse,
    ChatAgentChunk,
)
from agents import Runner

from agent import inventory_agent

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MLflow の Databricks 設定
mlflow.set_tracking_uri("databricks")


class InventoryAnalysisAgent(ResponsesAgent):
    """
    在庫分析エージェント — ResponsesAgent ラッパー

    OpenAI Agents SDK のエージェントを ResponsesAgent でラップし、
    MLflow AgentServer から呼び出し可能にする。
    ストリーミング応答に対応。
    """

    def predict(self, messages: list[ChatAgentMessage], context=None) -> ChatAgentResponse:
        """同期の predict メソッド"""
        # メッセージからユーザーの質問を取得
        user_message = ""
        for msg in reversed(messages):
            if msg.role == "user":
                user_message = msg.content
                break

        if not user_message:
            return ChatAgentResponse(
                messages=[
                    ChatAgentMessage(
                        role="assistant",
                        content="ご質問をお聞かせください。在庫データの分析をお手伝いします。",
                    )
                ]
            )

        # エージェント実行
        try:
            result = asyncio.run(
                Runner.run(inventory_agent, input=user_message)
            )

            response_text = result.final_output if result.final_output else "分析を完了しましたが、結果を生成できませんでした。"

        except Exception as e:
            logger.error(f"エージェント実行エラー: {e}")
            response_text = f"分析中にエラーが発生しました: {str(e)}\n\nもう一度お試しください。"

        return ChatAgentResponse(
            messages=[
                ChatAgentMessage(
                    role="assistant",
                    content=response_text,
                )
            ]
        )

    def predict_stream(self, messages: list[ChatAgentMessage], context=None):
        """ストリーミングの predict メソッド"""
        # 同期版を呼び出してチャンクに分割
        response = self.predict(messages, context)

        if response.messages:
            content = response.messages[0].content
            # 文章を句読点で分割してストリーミング風に返す
            chunks = _split_to_chunks(content)
            for chunk in chunks:
                yield ChatAgentChunk(
                    delta=ChatAgentMessage(
                        role="assistant",
                        content=chunk,
                    )
                )


def _split_to_chunks(text: str, chunk_size: int = 50) -> list[str]:
    """テキストをチャンクに分割（ストリーミング用）"""
    chunks = []
    current = ""
    for char in text:
        current += char
        if len(current) >= chunk_size and char in ("。", "\n", "、", "）", "」"):
            chunks.append(current)
            current = ""
    if current:
        chunks.append(current)
    return chunks


# エージェントのインスタンス
agent = InventoryAnalysisAgent()

# MLflow にモデルとして登録
mlflow.models.set_model(agent)


if __name__ == "__main__":
    port = int(os.environ.get("DATABRICKS_APP_PORT", os.environ.get("PORT", 7860)))

    logger.info(f"🤖 在庫分析エージェントを起動中...")
    logger.info(f"   ポート: {port}")
    logger.info(f"   チャット UI: http://localhost:{port}/")

    # AgentServer で起動
    try:
        from mlflow.server import get_app

        app = get_app()
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=port)
    except ImportError:
        # AgentServer が利用不可の場合は簡易サーバー
        logger.warning("MLflow AgentServer が利用できません。簡易モードで起動します。")

        from fastapi import FastAPI, Request
        from fastapi.responses import HTMLResponse, JSONResponse
        import uvicorn

        fast_app = FastAPI(title="在庫分析エージェント")

        @fast_app.get("/", response_class=HTMLResponse)
        async def chat_ui():
            return _get_chat_html()

        @fast_app.post("/invocations")
        async def invocations(request: Request):
            body = await request.json()
            messages = [
                ChatAgentMessage(role=m.get("role", "user"), content=m.get("content", ""))
                for m in body.get("messages", [])
            ]
            response = agent.predict(messages)
            return JSONResponse({
                "messages": [
                    {"role": m.role, "content": m.content}
                    for m in response.messages
                ]
            })

        uvicorn.run(fast_app, host="0.0.0.0", port=port)


def _get_chat_html() -> str:
    """シンプルなチャット UI HTML"""
    return """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>在庫分析アシスタント</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', 'Noto Sans JP', sans-serif;
            background: #0f172a; color: #e5e7eb;
            height: 100vh; display: flex; flex-direction: column;
        }
        .header {
            padding: 16px 24px;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            display: flex; align-items: center; gap: 12px;
        }
        .header h1 { font-size: 1.1rem; font-weight: 700; }
        .header .badge {
            font-size: 0.7rem; font-weight: 600; color: #60a5fa;
            background: rgba(59,130,246,0.15);
            padding: 2px 8px; border-radius: 4px;
        }
        .chat-container {
            flex: 1; overflow-y: auto; padding: 24px;
            display: flex; flex-direction: column; gap: 16px;
        }
        .message {
            max-width: 80%; padding: 16px; border-radius: 16px;
            line-height: 1.6; white-space: pre-wrap;
        }
        .message.user {
            align-self: flex-end;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: white; border-bottom-right-radius: 4px;
        }
        .message.assistant {
            align-self: flex-start;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            border-bottom-left-radius: 4px;
        }
        .input-area {
            padding: 16px 24px;
            border-top: 1px solid rgba(255,255,255,0.08);
            display: flex; gap: 12px;
        }
        .input-area input {
            flex: 1; padding: 12px 16px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px; color: #e5e7eb; font-size: 0.95rem;
            outline: none;
        }
        .input-area input:focus { border-color: #3b82f6; }
        .input-area button {
            padding: 12px 24px; background: #3b82f6;
            color: white; border: none; border-radius: 12px;
            font-weight: 600; cursor: pointer;
        }
        .input-area button:hover { background: #2563eb; }
        .input-area button:disabled { opacity: 0.5; cursor: not-allowed; }
        .loading { display: inline-block; }
        .loading::after {
            content: ''; animation: dots 1.5s infinite;
        }
        @keyframes dots {
            0% { content: '.'; }
            33% { content: '..'; }
            66% { content: '...'; }
        }
    </style>
</head>
<body>
    <div class="header">
        <span style="font-size:1.5rem">🤖</span>
        <h1>在庫分析アシスタント</h1>
        <span class="badge">AI Agent</span>
    </div>
    <div class="chat-container" id="chat">
        <div class="message assistant">
            こんにちは！在庫分析アシスタントです。
在庫データについて何でもお聞きください。

例:
• 「在庫過多の要因を分析し、改善アクションを提案してください」
• 「カテゴリBの過剰在庫を減らすにはどうすべきですか？」
• 「需要予測の精度を教えてください」
        </div>
    </div>
    <div class="input-area">
        <input type="text" id="input" placeholder="質問を入力してください..."
               onkeypress="if(event.key==='Enter')sendMessage()">
        <button onclick="sendMessage()" id="sendBtn">送信</button>
    </div>
    <script>
        const chat = document.getElementById('chat');
        const input = document.getElementById('input');
        const sendBtn = document.getElementById('sendBtn');
        let history = [];

        async function sendMessage() {
            const text = input.value.trim();
            if (!text) return;

            // ユーザーメッセージを表示
            appendMessage('user', text);
            history.push({role: 'user', content: text});
            input.value = '';
            sendBtn.disabled = true;

            // ローディング表示
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message assistant';
            loadingDiv.innerHTML = '<span class="loading">分析中</span>';
            chat.appendChild(loadingDiv);
            chat.scrollTop = chat.scrollHeight;

            try {
                const res = await fetch('/invocations', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({messages: history})
                });
                const data = await res.json();
                chat.removeChild(loadingDiv);

                if (data.messages && data.messages.length > 0) {
                    const assistantMsg = data.messages[data.messages.length - 1].content;
                    appendMessage('assistant', assistantMsg);
                    history.push({role: 'assistant', content: assistantMsg});
                }
            } catch (e) {
                chat.removeChild(loadingDiv);
                appendMessage('assistant', 'エラーが発生しました: ' + e.message);
            }

            sendBtn.disabled = false;
            input.focus();
        }

        function appendMessage(role, content) {
            const div = document.createElement('div');
            div.className = 'message ' + role;
            div.textContent = content;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>"""
