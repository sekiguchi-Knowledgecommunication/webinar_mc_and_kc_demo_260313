# 在庫管理 AI エージェントアプリケーション

マクニカ×KC 共催ウェビナー用 AI エージェントデモアプリ。
Databricks Agent Framework を使用し、Genie API をツールとして組み込んだマルチステップ推論エージェント。

## 技術スタック

- **フレームワーク**: OpenAI Agents SDK + MLflow ResponsesAgent
- **サーバー**: MLflow AgentServer（FastAPI）
- **ツール**: Genie API（自然言語 → SQL 実行）
- **デプロイ**: Databricks Apps

## ローカル実行

```bash
pip install -r requirements.txt
python app.py
# → http://localhost:7860/
```
