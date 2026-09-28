# Optional same-origin model packs

The app can stage WebLLM model artifacts into its service-worker cache, or import an offline model-pack folder from the AI Lab. This directory is intentionally empty in the base ZIP because model weights are hundreds of megabytes to multiple gigabytes.

For the default compatible fallback model, run `python tools/download_default_model_pack.py`. Then either deploy the generated pack with your site or choose the generated folder from **AI Resilience & Offline Model Packs**.
