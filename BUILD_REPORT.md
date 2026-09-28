# v2.3.0 resilient AI additions

- Added `ai-resilience.js` and dedicated `tx-ai-assets-v1` cache.
- Service worker now cache-first intercepts known WebLLM/model asset hosts after successful staging.
- Added file-by-file model staging with retry and verification.
- Added offline model-pack folder importer and runtime vendor slot.
- Added local OpenAI-compatible endpoint fallback and resilient auto-run.
- Retained hardware feature checks and deterministic fallback.

# v2.3.0 Resilient AI + Offline Model Packs

- Automatically detects browser-exposed WebGPU features/limits, shader-f16 support, CPU concurrency, browser-reported system-memory hints and origin storage.
- Builds a conservative hardware profile without claiming to measure exact GPU VRAM.
- Automatically selects the lowest-declared-VRAM compatible WebLLM model as the default.
- Adds Lightest / Balanced / Higher-capacity model recommendations based on the compatible catalog and hardware profile.
- Keeps manual model selection available and leaves larger recommendations opt-in.

# v2.2.4 GPU feature-aware patch

- Fixed WebGPU errors being misclassified as network errors because stack traces contained `https://` URLs.
- Added adapter feature detection and per-model compatibility evaluation.
- Added Compatible / Incompatible model filtering and disabled unsupported model actions.
- Added automatic lowest-VRAM compatible model selection.
- Added explicit shader-f16 readiness reporting.

# BUILD REPORT — Texas Master Systems OS v2.3.0-resilient-ai

## Changes
- Direct WebLLM `CreateMLCEngine` is primary.
- Dedicated Web Worker engine remains selectable/fallback.
- Dual runtime CDN import attempts added.
- Host reachability diagnostics added.
- Model catalog converted to nested collapsible compute-tier/model lists.
- Service-worker cache bumped to `tx-master-os-v2.3.0-resilient-ai`.

## Verification
PASS: app.js syntax checked with Node.
PASS: collaboration.js syntax checked with Node.
PASS: webllm-worker.js syntax checked with Node.
PASS: bundled static verifier.
PASS: direct-engine, worker fallback, dual runtime-CDN, host-probe, cache-verification and collapsible catalog markers.
PASS: localhost HTTP shell/core assets checked during packaging.
PASS: ZIP integrity checked after packaging.

Live WebGPU model downloads still require a real browser/network and are not claimed as tested in this container.

## v2.3.0 validation performed

- `python tools/verify.py`: PASS, including resilient-AI/PWA markers.
- `node --check`: PASS for `app.js`, `ai-resilience.js`, `webllm-worker.js`, `sw.js`, and collaboration code.
- Python helper scripts compile successfully.
- Local HTTP smoke: HTTP 200 for index, app, AI resilience module, service worker, worker, manifest, offline page, resilience documentation, and model-pack helper.
- Chromium headless DOM automation was attempted but timed out in this container because of its DBus/zygote environment; it is not reported as a passed browser test.
- Live WebGPU inference, hundreds-of-megabytes model transfer, and the optional GitHub Actions deployment cannot be executed in this container and remain destination-browser/deployment tests.

## Design boundary

The service worker improves retryability and offline reuse. It cannot bypass unsupported WebGPU features, origin security policy, or an upstream host that has never been reachable. Those cases are addressed by the offline folder pack, optional same-origin Pages pack, local WebLLM runtime slot, optional local endpoint, and deterministic final fallback.
