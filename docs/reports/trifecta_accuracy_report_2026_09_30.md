# ⚠️ INVALID — DO NOT TRUST

This file was produced by `compare_results.py` on 2026-10-01, which contained a
**hard-coded placeholder** instead of the model's real picks:

```python
pred_mock = [str(rnum), str(rnum+1), str(rnum+2)]  # algorithmic placeholder
```

Every "Predicted Pick" column in this report is therefore just the race number
and the two numbers after it — it is **not** the trifecta model output. The
"0.0% hit rate" is an artifact of comparing real results against that
placeholder, and carries no information about model accuracy.

The picks themselves in `trifecta_picks` / `TRIFECTA_2026-09-30.csv` are real
and unaffected.

Superseded by the verified scorecard:
- `fair-dinkum-publishing-agent-workflowz/score_trifecta.py` → real picks vs
  real Racing Australia results (36/36 races, name+number cross-checked)
- `outputs/trifecta_scorecard_2026-09-30.json`
- `outputs/trifecta_market_2026-09-30.json`