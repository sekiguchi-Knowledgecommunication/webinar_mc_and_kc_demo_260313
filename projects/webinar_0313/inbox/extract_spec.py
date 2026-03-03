import json

# サンプルダッシュボードからチャートウィジェットのspec構造を抽出
with open('/home/ubuntu/work/03.databricks/00.macnica_webinar/00.260313_webinar/projects/webinar_0313/inbox/Workspace Usage Dashboard.lvdash.json') as f:
    d = json.load(f)

for page in d.get('pages', []):
    for item in page.get('layout', []):
        w = item.get('widget', {})
        spec = w.get('spec', {})
        wt = spec.get('widgetType', '')
        if wt in ('bar', 'line', 'area', 'table', 'counter'):
            print(f"=== {w.get('name','?')} ({wt}) ===")
            print(json.dumps(spec, indent=2, ensure_ascii=False))
            print()
