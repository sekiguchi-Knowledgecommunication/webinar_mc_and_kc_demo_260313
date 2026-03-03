import json

with open("/tmp/dashboard_actual.json") as f:
    d = json.load(f)

for page in d.get("pages", []):
    for item in page.get("layout", []):
        w = item.get("widget", {})
        spec = w.get("spec", {})
        wt = spec.get("widgetType", "?")
        name = w.get("name", "?")
        queries = w.get("queries", [])
        q = queries[0] if queries else {}
        qname = q.get("name", "?")
        qdata = q.get("query", {})
        fields = qdata.get("fields", [])
        disagg = qdata.get("disaggregated", "?")
        enc = spec.get("encodings", {})
        ver = spec.get("version", "?")

        print(f"=== {name} ({wt}, v{ver}) ===")
        print(f"  query.name: {qname}")
        print(f"  disaggregated: {disagg}")
        print(f"  fields:")
        for fd in fields:
            print(f"    - name: {fd.get('name')}  expression: {fd.get('expression')}")
        print(f"  encodings:")
        print(json.dumps(enc, indent=4, ensure_ascii=False))
        print()
