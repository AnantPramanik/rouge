#!/usr/bin/env bash
set -euo pipefail
cd /kaggle/working
if [ ! -d ComfyUI ]; then
  git clone https://github.com/Comfy-Org/ComfyUI.git
else
  echo "ComfyUI directory already exists; keeping current checkout."
fi
cd ComfyUI
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo "ComfyUI dependencies installed."
