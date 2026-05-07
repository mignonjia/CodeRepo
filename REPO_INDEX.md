# Repository Index

This submission package contains the core AtariBench runtime.

## Entry Points

- `main.py`: single-run CLI for one game/model setting.
- `batch_run.py`: config-driven batch orchestration.
- `visualize.py`: render a saved run directory to video.

## Runtime Modules

- `core/pipeline.py`: main environment/model/action loop.
- `core/clip.py`: parses model text into executable Atari actions.
- `core/trajectory.py`: persists frames, prompts, responses, turns, and summaries.
- `run_storage.py`: canonical output layout and summary aggregation.

## Game And Prompt Modules

- `games/registry.py`: supported games and selection aliases.
- `games/env.py`: ALE environment creation and frame/info helpers.
- `games/prompt_builder.py`: prompt assembly for `structured_history` and `append_only`.
- `games/prompts/`: per-game action maps and prompt text.

## Model Adapters

- `llm/__init__.py`: model client factory.
- `llm/common.py`: provider inference, token usage helpers, thinking-mode validation.
- `llm/gemini_client.py`: Gemini adapter.
- `llm/openai_client.py`: OpenAI adapter.
- `llm/anthropic_client.py`: Anthropic adapter.
- `llm/together_client.py`: Together adapter.
- `llm/dashscope_client.py`: DashScope adapter.
- `llm/random_client.py`: local random-action baseline.
- `llm/retry.py`: transient provider-error retry handling.
- `llm/model_thinking.json`: supported thinking modes by model.

## Configuration And Tests

- `config/common.yaml`: shared reviewer-scale defaults.
- `config/runs.yaml`: small batch example using the local random baseline.
- `tests/test_smoke.py`: concise smoke coverage for registry, parsing, and local model setup.
