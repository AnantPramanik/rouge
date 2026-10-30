# ComfyUI Kaggle Image Editor

A reproducible ComfyUI image-to-image editing starter project for a Kaggle GPU notebook. GitHub stores code and workflows; Kaggle provides the temporary GPU runtime.

## Included
- Full ComfyUI node-based interface
- Lightweight Gradio browser interface
- Kaggle notebook for setup and launch
- Basic Stable Diffusion 1.5 img2img API workflow
- No model weights (attach your own Kaggle Dataset)

## Important limitations
1. Kaggle sessions are temporary, quota-limited, and not an always-on host.
2. A compatible checkpoint must be supplied by you as a Kaggle Dataset. Review its license.
3. The included workflow is a generic SD 1.5 img2img template, not Qwen Image Edit or another instruction-following editor.
4. Public share/tunnel links may be accessible to anyone who has the URL. Do not upload private or sensitive images.
5. Use models and services according to their licenses, platform terms, applicable law, and consent requirements. Do not create non-consensual intimate imagery or sexual content involving minors.

## Kaggle quick start
1. Open `kaggle/ComfyUI_Kaggle.ipynb` in Kaggle (Code → New Notebook → Import Notebook).
2. Enable a GPU in Notebook Options and enable Internet if available.
3. Attach a Kaggle Dataset containing a compatible SD 1.5 `.safetensors` checkpoint.
4. Set `MODEL_DATASET_DIR` in the notebook to the attached dataset directory under `/kaggle/input/`.
5. Run the notebook cells from top to bottom.
6. Open the generated Gradio link for the simple interface, or the ComfyUI link for the full interface.

## Interfaces
- **ComfyUI:** full node-based workflow editor (port 8188).
- **Gradio:** simple image + prompt + denoise-strength interface (port 7860).

The optional Cloudflare quick tunnel is best-effort; Kaggle/network policy may block it. Kaggle sessions can stop and erase working files, so save outputs before the session ends.

## Model placement
The notebook copies a compatible checkpoint into `ComfyUI/models/checkpoints/`. Do not commit model weights, API tokens, passwords, or private images to this repository.

## Workflow mapping
The Gradio app expects API workflow node IDs 1–8 as documented in `workflows/README.md`. If you modify the graph, preserve those IDs or update `app/gradio_app.py`.

## Troubleshooting
- **No model found:** attach a dataset with a compatible checkpoint and set `MODEL_DATASET_DIR`.
- **CUDA out of memory:** use a smaller/lower-VRAM checkpoint or reduce image dimensions.
- **Tunnel URL missing:** tunnel startup may be blocked; the local services may still be running.
- **Workflow/model error:** check the checkpoint filename and API workflow node IDs.
- **Custom nodes:** this starter uses built-in ComfyUI nodes only.

## Security
Treat public tunnel URLs as bearer links. Stop the notebook session when finished. Never put Kaggle API tokens, GitHub tokens, passwords, or sensitive images in this repository.
