# AtariBench

AtariBench is a compact runner for evaluating vision-language model agents on
Atari games. At each turn, the runner builds a multimodal prompt from recent game
frames, asks a model for a short action plan, executes the parsed actions in ALE,
and writes a reproducible trajectory with prompts, responses, frames, summaries,
and an optional video.

This repository contains only the core runtime code needed to run experiments.
Generated runs, auxiliary analysis utilities, and local credentials are
intentionally excluded.

## Repository Layout

- `main.py`: run one game/model setting.
- `batch_run.py`: run config-driven experiment batches.
- `core/`: pipeline loop, response parsing, and trajectory persistence.
- `games/`: Atari game registry, ALE helpers, and per-game prompts.
- `llm/`: model client adapters and thinking-mode configuration.
- `viz/`: render stored trajectories to video.
- `config/`: small reviewer-scale batch configuration.
- `tests/`: concise smoke tests for registry, parsing, and the local baseline.

## Setup

Create the Conda environment:

```bash
conda env create -f environment.yaml
conda activate ale
```

The environment installs Python dependencies, ALE support, and `ffmpeg` for video
rendering.

For live model runs, export the API key for the provider you use:

```bash
export GEMINI_API_KEY="..."
export OPENAI_API_KEY="..."
export ANTHROPIC_API_KEY="..."
export TOGETHER_API_KEY="..."
export DASHSCOPE_API_KEY="..."
```

The `random` model is a local baseline and does not require API keys.

## Quick Check

Run the smoke tests:

```bash
python -m unittest
```

Run a short local baseline without external API calls:

```bash
python main.py \
  --game breakout \
  --model random \
  --thinking off \
  --duration-seconds 5 \
  --minimal-logging
```

The output is written under `runs/<game>/<model>/`.

## Single Live Model Run

Example using Gemini:

```bash
python main.py \
  --game breakout \
  --model gemini-2.5-flash \
  --thinking off \
  --prompt-mode structured_history \
  --duration-seconds 30 \
  --minimal-logging
```

Supported prompt modes are:

- `structured_history`: current frame plus curated recent and reward-bearing clips.
- `append_only`: chronological transcript-style context.

Supported thinking modes are model-specific and declared in
`llm/model_thinking.json`.

## Batch Runs

The included config is intentionally small and uses the local `random` baseline:

```bash
python batch_run.py --common-config config/common.yaml --runs-config config/runs.yaml
```

To run live VLM settings, edit `config/runs.yaml` and replace `model_name` and
`thinking_mode` with a supported pair from `llm/model_thinking.json`. For the
30-second benchmark window, set `duration_seconds: 30` in `config/common.yaml`.

## Outputs

Each successful run writes a directory containing:

- `summary.json`: run configuration, reward, stop reason, and token totals.
- `turns.jsonl`: per-turn action, response, reward, and token metadata.
- `visualization.mp4`: rendered trajectory video when rendering succeeds.

Without `--minimal-logging`, runs also keep raw frames, prompt text/HTML, and raw
model responses for debugging.

Aggregated summaries are rebuilt under `runs/` after successful runs:

- `runs/<game>/model_summary.json`
- `runs/<game>/model_summary_30s.json`
- `runs/model_summary.json`
- `runs/model_summary_30s.json`

## Visualization

Render or re-render a saved run:

```bash
python visualize.py runs/breakout/random/<run_id>
```

## Notes For Reviewers

- The default batch is short so it can be run quickly on a fresh machine.
- Live model runs require provider API keys and may incur provider costs.
- The code writes generated artifacts only under ignored output folders.
- The repository is anonymized and includes only the core runtime needed to run
  reviewer-scale experiments.
