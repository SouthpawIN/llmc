# ACE-Step Model Zoo & Hardware Guide

Complete model specs and GPU selection matrix from the official README.

## DiT Models (Audio Decoder)

### 2B Models

| Model | CFG | Steps | Text2Music | Cover | Repaint | Extract | Lego | Complete | Quality | HuggingFace |
|-------|:---:|:-----:|:----------:|:-----:|:------:|:-------:|:----:|:--------:|---------|-------------|
| `acestep-v15-base` | ✅ | 50 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | Medium | [Link](https://huggingface.co/ACE-Step/acestep-v15-base) |
| `acestep-v15-sft` | ✅ | 50 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | High | [Link](https://huggingface.co/ACE-Step/acestep-v15-sft) |
| `acestep-v15-turbo` | ❌ | 8 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | Very High | [Link](https://huggingface.co/ACE-Step/Ace-Step1.5) |

### 4B XL Models (Released 2026-04-02)

| Model | CFG | Steps | Quality | HuggingFace |
|-------|:---:|:-----:|---------|-------------|
| `acestep-v15-xl-base` | ✅ | 50 | High | [Link](https://huggingface.co/ACE-Step/acestep-v15-xl-base) |
| `acestep-v15-xl-sft` | ✅ | 50 | Very High | [Link](https://huggingface.co/ACE-Step/acestep-v15-xl-sft) |
| `acestep-v15-xl-turbo` | ❌ | 8 | Very High | [Link](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo) |

## LM Models (Planner)

| Model | Base | CoT | Query Rewrite | Audio Understanding | Composition | Copy Melody |
|-------|------|:---:|:------------:|:-------------------:|:-----------:|:-----------:|
| `acestep-5Hz-lm-0.6B` | Qwen3-0.6B | ✅ | ✅ | Medium | Medium | Weak |
| `acestep-5Hz-lm-1.7B` | Qwen3-1.7B | ✅ | ✅ | Medium | Medium | Medium |
| `acestep-5Hz-lm-4B` | Qwen3-4B | ✅ | ✅ | Strong | Strong | Strong |

## GPU Selection Matrix

| GPU VRAM | Recommended DiT | Recommended LM | Backend |
|----------|-----------------|----------------|---------|
| ≤6GB | 2B turbo | None (DiT only) | — |
| 6-8GB | 2B turbo | `acestep-5Hz-lm-0.6B` | `pt` |
| 8-16GB | 2B turbo/sft | `acestep-5Hz-lm-0.6B` / `1.7B` | `vllm` |
| 16-20GB | 2B sft or XL turbo | `acestep-5Hz-lm-1.7B` | `vllm` |
| 20-24GB | XL turbo/sft | `acestep-5Hz-lm-1.7B` | `vllm` |
| ≥24GB | XL sft (or xl-base) | `acestep-5Hz-lm-4B` | `vllm` |

## VRAM Footprint (Approximate)

| Component | VRAM (bf16) |
|-----------|-------------|
| DiT 2B | ~4-5 GB |
| DiT 4B XL | ~9 GB |
| LM 0.6B | ~1.5 GB |
| LM 1.7B | ~3.5 GB |
| LM 4B | ~8 GB |
| LoRA training (2B) | ~12-17 GB |
| LoRA training (4B XL) | ~20-24 GB |

## Performance Benchmarks

| Metric | A100 | RTX 3090 |
|--------|------|----------|
| Full song (2B turbo) | <2s | <10s |
| Full song (2B sft, 50 steps) | ~5s | ~20s |
| LoRA training (8 songs, 100 epochs) | ~20 min | ~1 hour |

## Architecture

Hybrid architecture — LM functions as an **omni-capable planner**:
- Transforms simple queries into comprehensive song blueprints
- Synthesizes metadata, lyrics, captions via **Chain-of-Thought** to guide the DiT
- Alignment achieved through **intrinsic reinforcement learning** (no external reward models)

## Configuration via .env

```bash
cp .env.example .env
# Key settings:
ACESTEP_CONFIG_PATH=acestep-v15-turbo     # DiT model
ACESTEP_LM_MODEL_PATH=acestep-5Hz-lm-1.7B  # LM model
PORT=7860                                   # Gradio port
LANGUAGE=en
```

## Launch Scripts

| Platform | Gradio UI | API Server |
|----------|-----------|------------|
| Linux (CUDA) | `start_gradio_ui.sh` | `start_api_server.sh` |
| macOS (MLX) | `start_gradio_ui_macos.sh` | `start_api_server_macos.sh` |
| Windows (CUDA) | `start_gradio_ui.bat` | `start_api_server.bat` |
| Windows (ROCm) | `start_gradio_ui_rocm.bat` | `start_api_server_rocm.bat` |
