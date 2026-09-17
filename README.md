# SQL SOC Investigation Lab

Loads synthetic authentication events into SQLite and runs a parameterized aggregation that identifies source IPs with repeated failures and multiple targeted users.

```bash
python main.py sample_events.json
python -m unittest -v
```

Demonstrates SQLite schema design, safe parameterized queries, aggregation, and evidence-driven SOC investigation.
