# Texas Master Systems OS v2.3.0 — Resilient AI PWA

This branch adds service-worker model staging, shard-level retry, offline folder model-pack import, a same-origin WebLLM runtime slot, optional local OpenAI-compatible endpoint fallback, and deterministic final fallback.

# v2.3.0 Resilient AI + Offline Model Packs

- Automatically detects browser-exposed WebGPU features/limits, shader-f16 support, CPU concurrency, browser-reported system-memory hints and origin storage.
- Builds a conservative hardware profile without claiming to measure exact GPU VRAM.
- Automatically selects the lowest-declared-VRAM compatible WebLLM model as the default.
- Adds Lightest / Balanced / Higher-capacity model recommendations based on the compatible catalog and hardware profile.
- Keeps manual model selection available and leaves larger recommendations opt-in.

# Texas Master Systems OS v2.3.0-resilient-ai

Experimental comparison branch of v2.2.2. The primary WebLLM path is now the direct `CreateMLCEngine` factory, with optional dedicated-worker fallback.

## Why this branch exists

The v2.2.2 compatibility build used the Connectivity v5 worker/IndexedDB pattern first. This edition intentionally reverses that choice so the same browser/network can be tested with the newer direct-engine factory path. If both architectures fail at the same host request, the problem is network/artifact reachability rather than the worker abstraction.

## AI changes

- Direct `CreateMLCEngine` first by default.
- Strategy selector: Direct → worker fallback, Direct only, or Worker only.
- Runtime import attempts `esm.run` first and a jsDelivr `+esm` URL second.
- Cache API is the default cache backend; IndexedDB and OPFS remain selectable.
- `Test model hosts` checks runtime CDN routes, the selected Hugging Face model config path, and the compiled WebGPU library route.
- Model catalog is grouped into collapsible Tiny / Light / Medium / Heavy / Extreme sections, with each model itself collapsible.
- Download/cache success is still verified with WebLLM cache inspection before being reported.

## Network reality

Engine switching can bypass a worker/module-runtime problem. It cannot bypass a firewall/content blocker that prevents the browser from reaching the model repository or compiled model library host. Host diagnostics are included specifically to distinguish those cases.

All other v2.2.2 systems, PWA, multiplayer, Nexus, Cascade Lab, evidence, quests, storage, and offline features are retained.


## v2.2.4 GPU feature-aware patch

This build fixes a diagnostic bug where an `https://` URL in a JavaScript stack trace could cause a WebGPU compatibility failure to be mislabeled as a network error. Error classification now uses the error message first and checks GPU compatibility before network conditions.

The model catalog now queries the browser WebGPU adapter, compares `required_features` and `buffer_size_required_bytes` against each WebLLM model record, defaults to **Compatible only**, disables unsupported models, and automatically selects the lowest-VRAM compatible model if the prior selection is incompatible. The readiness panel explicitly reports whether `shader-f16` is exposed.
