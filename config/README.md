# Config Files

`common.yaml` holds shared runtime defaults. The packaged version is reviewer-scale:
short duration, minimal logging, and conservative retry/concurrency settings.
Set `duration_seconds: 30` for the benchmark window.

`runs.yaml` is a minimal batch example using the local `random` baseline so it can
run without API keys. To evaluate a live model, replace `model_name` and
`thinking_mode` with a supported pair from `../llm/model_thinking.json`.

Run the bundled batch with:

```bash
python batch_run.py --common-config config/common.yaml --runs-config config/runs.yaml
```
