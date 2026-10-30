#!/usr/bin/env bash
set -euo pipefail
cd /kaggle/working/ComfyUI
python main.py --listen 0.0.0.0 --port 8188
