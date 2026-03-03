#!/bin/bash
# ダッシュボードを公開する
export PATH="$HOME/.local/bin:$PATH"

DASHBOARD_ID="01f116d5e20611fb9cb1f97f9d1aa817"

echo "📊 ダッシュボードを公開中..."
databricks api post /api/2.0/lakeview/dashboards/$DASHBOARD_ID/published \
  --json '{"embed_credentials": true, "warehouse_id": "863ce5ef78045c29"}'
