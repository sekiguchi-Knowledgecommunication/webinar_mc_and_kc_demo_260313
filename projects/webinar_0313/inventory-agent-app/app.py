"""
在庫分析エージェント — メインアプリケーション

MLflow ResponsesAgent を使用して FastAPI サーバーを起動。
ストリーミング対応のチャット UI 付き。
"""

import os
import json
import logging
import asyncio
from typing import Generator

import mlflow
from mlflow.pyfunc import ResponsesAgent
from mlflow.types.agent import (
    ChatAgentMessage,
    ChatAgentResponse,
    ChatAgentChunk,
)
from agents import Runner
from agents.stream_events import RunItemStreamEvent, RawResponsesStreamEvent

from agent import inventory_agent

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MLflow の Databricks 設定
mlflow.set_tracking_uri("databricks")

# OpenAI Agents SDK の MLflow 自動トレースを有効化
try:
    mlflow.openai.autolog()
except Exception:
    logger.info("MLflow OpenAI autolog は利用できません（ローカル実行時は無視）")


def _convert_messages_to_input(messages: list[ChatAgentMessage]) -> list[dict]:
    """ChatAgentMessage のリストを OpenAI Agents SDK の入力形式に変換"""
    converted = []
    for msg in messages:
        if msg.role in ("user", "assistant"):
            converted.append({
                "role": msg.role,
                "content": msg.content or "",
            })
    return converted


class InventoryAnalysisAgent(ResponsesAgent):
    """
    在庫分析エージェント — ResponsesAgent ラッパー

    OpenAI Agents SDK のエージェントを ResponsesAgent でラップし、
    MLflow AgentServer から呼び出し可能にする。
    マルチターン会話とストリーミング応答に対応。
    """

    def predict(self, messages: list[ChatAgentMessage], context=None) -> ChatAgentResponse:
        """同期の predict メソッド — マルチターン会話対応"""
        # 会話履歴全体を Agent に渡す
        input_messages = _convert_messages_to_input(messages)

        if not input_messages:
            return ChatAgentResponse(
                messages=[
                    ChatAgentMessage(
                        role="assistant",
                        content="ご質問をお聞かせください。在庫データの分析をお手伝いします。",
                    )
                ]
            )

        # エージェント実行（会話履歴全体を渡す）
        try:
            result = asyncio.run(
                Runner.run(inventory_agent, input=input_messages)
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
        """ストリーミングの predict メソッド — リアルタイムイベント配信"""
        # 会話履歴全体を Agent に渡す
        input_messages = _convert_messages_to_input(messages)

        if not input_messages:
            yield ChatAgentChunk(
                delta=ChatAgentMessage(
                    role="assistant",
                    content="ご質問をお聞かせください。在庫データの分析をお手伝いします。",
                )
            )
            return

        try:
            # Runner.run_streamed() で非同期ストリーミング実行
            # 同期コンテキストから非同期ストリームを消費するためにイベントループを使用
            loop = asyncio.new_event_loop()
            try:
                # 非同期ジェネレータから全イベントを収集
                events = loop.run_until_complete(
                    _collect_stream_events(input_messages)
                )
            finally:
                loop.close()

            # 収集したイベントを ChatAgentChunk として yield
            for event_data in events:
                yield ChatAgentChunk(
                    delta=ChatAgentMessage(
                        role="assistant",
                        content=event_data,
                    )
                )

        except Exception as e:
            logger.error(f"ストリーミングエラー: {e}")
            yield ChatAgentChunk(
                delta=ChatAgentMessage(
                    role="assistant",
                    content=f"分析中にエラーが発生しました: {str(e)}",
                )
            )


async def _collect_stream_events(input_messages: list[dict]) -> list[str]:
    """非同期ストリーミングイベントを収集"""
    events = []
    streamed_result = Runner.run_streamed(inventory_agent, input=input_messages)

    async for event in streamed_result.stream_events():
        if isinstance(event, RunItemStreamEvent):
            # ツール呼び出し完了時（report_step の結果を通知）
            item = event.item
            if hasattr(item, "type") and item.type == "tool_call_output_item":
                if hasattr(item, "output") and item.output:
                    output = item.output
                    # report_step の出力（✅ Step N: ...）のみを通知
                    if isinstance(output, str) and output.startswith("✅"):
                        events.append(output + "\n\n")

        elif isinstance(event, RawResponsesStreamEvent):
            # LLM のテキスト生成をトークン単位で収集
            data = event.data
            if hasattr(data, "delta") and data.delta:
                delta_text = ""
                if hasattr(data.delta, "content") and data.delta.content:
                    # Content delta からテキストを抽出
                    for part in data.delta.content:
                        if hasattr(part, "text") and part.text:
                            delta_text += part.text
                elif hasattr(data.delta, "text") and data.delta.text:
                    delta_text = data.delta.text

                if delta_text:
                    events.append(delta_text)

    return events


# エージェントのインスタンス
agent = InventoryAnalysisAgent()

# MLflow にモデルとして登録
mlflow.models.set_model(agent)


if __name__ == "__main__":
    port = int(os.environ.get("DATABRICKS_APP_PORT", os.environ.get("PORT", 7860)))

    logger.info(f"🤖 在庫分析エージェントを起動中...")
    logger.info(f"   ポート: {port}")
    logger.info(f"   チャット UI: http://localhost:{port}/")

    # AgentServer で起動を試みる
    try:
        from mlflow.server import get_app

        app = get_app()
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=port)
    except (ImportError, Exception) as e:
        # AgentServer が利用不可の場合は簡易サーバー + SSE ストリーミング
        logger.warning(f"MLflow AgentServer が利用できません（{e}）。簡易モードで起動します。")

        from fastapi import FastAPI, Request
        from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
        import uvicorn

        fast_app = FastAPI(title="在庫分析エージェント")

        @fast_app.get("/", response_class=HTMLResponse)
        async def chat_ui():
            return _get_chat_html()

        @fast_app.post("/invocations")
        async def invocations(request: Request):
            """同期レスポンス（互換性維持）"""
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

        @fast_app.post("/stream")
        async def stream_endpoint(request: Request):
            """SSE ストリーミングエンドポイント"""
            body = await request.json()
            messages = [
                ChatAgentMessage(role=m.get("role", "user"), content=m.get("content", ""))
                for m in body.get("messages", [])
            ]

            def generate():
                for chunk in agent.predict_stream(messages):
                    if chunk.delta and chunk.delta.content:
                        # SSE 形式でデータを送信
                        data = json.dumps({"content": chunk.delta.content}, ensure_ascii=False)
                        yield f"data: {data}\n\n"
                yield "data: [DONE]\n\n"

            return StreamingResponse(
                generate(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                },
            )

        uvicorn.run(fast_app, host="0.0.0.0", port=port)


def _get_chat_html() -> str:
    """ストリーミング対応のチャット UI HTML"""
    return """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>在庫分析アシスタント</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', 'Noto Sans JP', sans-serif;
            background: #0a0f1e; color: #e5e7eb;
            height: 100vh; display: flex; flex-direction: column;
        }
        /* ヘッダー */
        .header {
            padding: 16px 24px;
            background: linear-gradient(135deg, rgba(6,182,212,0.08), rgba(59,130,246,0.08));
            border-bottom: 1px solid rgba(6,182,212,0.15);
            display: flex; align-items: center; gap: 12px;
        }
        .header-icon {
            width: 36px; height: 36px; border-radius: 10px;
            background: linear-gradient(135deg, #06b6d4, #3b82f6);
            display: flex; align-items: center; justify-content: center;
            font-size: 1.1rem;
        }
        .header h1 {
            font-size: 1.05rem; font-weight: 700;
            background: linear-gradient(135deg, #06b6d4, #60a5fa);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .header .badge {
            font-size: 0.65rem; font-weight: 600; color: #06b6d4;
            background: rgba(6,182,212,0.12);
            padding: 3px 10px; border-radius: 20px;
            border: 1px solid rgba(6,182,212,0.2);
            letter-spacing: 0.05em;
        }

        /* チャットコンテナ */
        .chat-container {
            flex: 1; overflow-y: auto; padding: 24px;
            display: flex; flex-direction: column; gap: 16px;
            scroll-behavior: smooth;
        }
        .message {
            max-width: 85%; padding: 16px 20px; border-radius: 16px;
            line-height: 1.7; white-space: pre-wrap; font-size: 0.92rem;
            animation: fadeIn 0.3s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .message.user {
            align-self: flex-end;
            background: linear-gradient(135deg, #06b6d4, #3b82f6);
            color: white; border-bottom-right-radius: 4px;
            font-weight: 500;
        }
        .message.assistant {
            align-self: flex-start;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
            border-bottom-left-radius: 4px;
        }

        /* ステップバッジ */
        .step-badge {
            display: inline-flex; align-items: center; gap: 8px;
            padding: 8px 16px; border-radius: 24px;
            font-size: 0.82rem; font-weight: 600;
            background: rgba(6,182,212,0.1);
            border: 1px solid rgba(6,182,212,0.25);
            color: #22d3ee;
            animation: slideIn 0.4s ease-out;
            margin: 4px 0;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-16px); }
            to { opacity: 1; transform: translateX(0); }
        }
        .step-badge .step-icon {
            width: 20px; height: 20px; border-radius: 50%;
            background: rgba(6,182,212,0.2);
            display: flex; align-items: center; justify-content: center;
            font-size: 0.7rem;
        }

        /* ローディング */
        .loading-indicator {
            display: flex; align-items: center; gap: 12px;
            padding: 16px 20px; border-radius: 16px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
            border-bottom-left-radius: 4px;
            font-size: 0.88rem; color: #94a3b8;
            animation: fadeIn 0.3s ease-out;
        }
        .loading-dots {
            display: flex; gap: 4px;
        }
        .loading-dots span {
            width: 6px; height: 6px; border-radius: 50%;
            background: #06b6d4;
            animation: bounce 1.4s infinite ease-in-out both;
        }
        .loading-dots span:nth-child(1) { animation-delay: -0.32s; }
        .loading-dots span:nth-child(2) { animation-delay: -0.16s; }
        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }

        /* 入力エリア */
        .input-area {
            padding: 16px 24px;
            background: rgba(255,255,255,0.02);
            border-top: 1px solid rgba(255,255,255,0.06);
            display: flex; gap: 12px;
        }
        .input-area input {
            flex: 1; padding: 14px 18px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 14px; color: #e5e7eb;
            font-size: 0.92rem; font-family: inherit;
            outline: none; transition: border-color 0.2s;
        }
        .input-area input:focus {
            border-color: #06b6d4;
            box-shadow: 0 0 0 3px rgba(6,182,212,0.1);
        }
        .input-area input::placeholder { color: #64748b; }
        .input-area button {
            padding: 14px 28px;
            background: linear-gradient(135deg, #06b6d4, #3b82f6);
            color: white; border: none; border-radius: 14px;
            font-weight: 600; font-size: 0.9rem; font-family: inherit;
            cursor: pointer; transition: all 0.2s;
        }
        .input-area button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 16px rgba(6,182,212,0.3);
        }
        .input-area button:disabled {
            opacity: 0.4; cursor: not-allowed;
            transform: none; box-shadow: none;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-icon">📊</div>
        <h1>在庫分析アシスタント</h1>
        <span class="badge">AI AGENT</span>
    </div>
    <div class="chat-container" id="chat">
        <div class="message assistant">こんにちは！在庫分析アシスタントです。
在庫データについて何でもお聞きください。

例:
• 「在庫過多の要因を分析し、改善アクションを提案してください」
• 「カテゴリBの過剰在庫を減らすにはどうすべきですか？」
• 「需要予測の精度を教えてください」</div>
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
            loadingDiv.className = 'loading-indicator';
            loadingDiv.innerHTML = '<div class="loading-dots"><span></span><span></span><span></span></div> 分析中...';
            chat.appendChild(loadingDiv);
            chat.scrollTop = chat.scrollHeight;

            // アシスタント応答用の要素を事前作成
            const assistantDiv = document.createElement('div');
            assistantDiv.className = 'message assistant';
            assistantDiv.style.display = 'none';

            let fullContent = '';

            try {
                // SSE ストリーミングで受信
                const res = await fetch('/stream', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({messages: history})
                });

                const reader = res.body.getReader();
                const decoder = new TextDecoder();
                let buffer = '';

                // ローディングを消してアシスタント要素を表示
                chat.removeChild(loadingDiv);
                chat.appendChild(assistantDiv);
                assistantDiv.style.display = 'block';

                while (true) {
                    const {done, value} = await reader.read();
                    if (done) break;

                    buffer += decoder.decode(value, {stream: true});

                    // SSE メッセージをパース
                    const lines = buffer.split('\\n');
                    buffer = lines.pop() || '';

                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            const dataStr = line.slice(6).trim();
                            if (dataStr === '[DONE]') continue;

                            try {
                                const data = JSON.parse(dataStr);
                                if (data.content) {
                                    // ステップバッジかテキストかを判定
                                    if (data.content.startsWith('✅ Step')) {
                                        const badge = document.createElement('div');
                                        badge.className = 'step-badge';
                                        const stepMatch = data.content.match(/✅ Step (\\d+): (.+)/);
                                        if (stepMatch) {
                                            badge.innerHTML = '<span class="step-icon">' + stepMatch[1] + '</span>' + stepMatch[2];
                                        } else {
                                            badge.textContent = data.content;
                                        }
                                        chat.insertBefore(badge, assistantDiv);
                                    } else {
                                        fullContent += data.content;
                                        assistantDiv.textContent = fullContent;
                                    }
                                    chat.scrollTop = chat.scrollHeight;
                                }
                            } catch (e) {
                                // JSON パースエラーは無視
                            }
                        }
                    }
                }

                // 最終テキストが空の場合の処理
                if (!fullContent && assistantDiv.textContent === '') {
                    assistantDiv.textContent = '分析を完了しましたが、結果を表示できませんでした。';
                }

                history.push({role: 'assistant', content: fullContent});

            } catch (e) {
                // SSE が使えない場合は同期 API にフォールバック
                try {
                    const res = await fetch('/invocations', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({messages: history})
                    });
                    const data = await res.json();
                    if (loadingDiv.parentNode) chat.removeChild(loadingDiv);

                    if (data.messages && data.messages.length > 0) {
                        const msg = data.messages[data.messages.length - 1].content;
                        appendMessage('assistant', msg);
                        history.push({role: 'assistant', content: msg});
                    }
                } catch (e2) {
                    if (loadingDiv.parentNode) chat.removeChild(loadingDiv);
                    appendMessage('assistant', 'エラーが発生しました: ' + e2.message);
                }
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
