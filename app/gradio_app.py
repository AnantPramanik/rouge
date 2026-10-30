import copy, json, os, random, time
from pathlib import Path
import gradio as gr
import requests

COMFY_URL = os.environ.get("COMFY_URL", "http://127.0.0.1:8188")
WORKFLOW_PATH = Path(os.environ["WORKFLOW_PATH"])
CHECKPOINT_DIR = Path("/kaggle/working/ComfyUI/models/checkpoints")

def run_edit(image, prompt, negative, strength, steps, cfg, checkpoint):
    if image is None or not prompt or not prompt.strip():
        raise gr.Error("Upload an image and enter an edit prompt.")
    if not checkpoint:
        raise gr.Error("Attach a compatible SD 1.5 checkpoint Kaggle Dataset.")
    try:
        if not requests.get(f"{COMFY_URL}/system_stats", timeout=5).ok:
            raise gr.Error("ComfyUI is not responding.")
    except requests.RequestException as exc:
        raise gr.Error(f"ComfyUI is not responding: {exc}")
    workflow = json.loads(WORKFLOW_PATH.read_text(encoding="utf-8"))
    with open(image, "rb") as f:
        uploaded = requests.post(f"{COMFY_URL}/upload/image",
            files={"image": (Path(image).name, f, "application/octet-stream")},
            data={"overwrite": "true"}, timeout=120)
    uploaded.raise_for_status()
    workflow["1"]["inputs"]["ckpt_name"] = checkpoint
    workflow["2"]["inputs"]["image"] = uploaded.json()["name"]
    workflow["4"]["inputs"]["text"] = prompt.strip()
    workflow["5"]["inputs"]["text"] = (negative or "").strip()
    workflow["6"]["inputs"].update(seed=random.randint(1, 2**31-1),
        steps=int(steps), cfg=float(cfg), denoise=float(strength))
    response = requests.post(f"{COMFY_URL}/prompt",
        json={"prompt": workflow, "client_id": f"gradio-{random.randint(1,10**9)}"}, timeout=60)
    if not response.ok:
        raise gr.Error(f"ComfyUI rejected workflow: {response.text[:1000]}")
    prompt_id = response.json()["prompt_id"]
    deadline = time.time() + 900
    while time.time() < deadline:
        history = requests.get(f"{COMFY_URL}/history/{prompt_id}", timeout=20)
        history.raise_for_status()
        entry = history.json().get(prompt_id)
        if entry:
            for output in entry.get("outputs", {}).values():
                for item in output.get("images", []):
                    if item.get("type") == "output":
                        result = requests.get(f"{COMFY_URL}/view",
                            params={"filename": item["filename"], "subfolder": item.get("subfolder",""), "type":"output"},
                            timeout=120)
                        result.raise_for_status()
                        path = f"/kaggle/working/result_{prompt_id[:8]}.png"
                        Path(path).write_bytes(result.content)
                        return path
            if entry.get("status", {}).get("status_str") == "error":
                raise gr.Error("ComfyUI execution failed. Inspect the notebook logs.")
        time.sleep(2)
    raise gr.Error("Timed out waiting for ComfyUI. Inspect notebook logs.")

choices = sorted(p.name for p in CHECKPOINT_DIR.glob("*") if p.suffix.lower() in (".safetensors",".ckpt",".pt"))
with gr.Blocks(title="ComfyUI Image Editor") as demo:
    gr.Markdown("# ComfyUI Image Editor\nUpload an image and describe the edit.")
    with gr.Row():
        with gr.Column():
            source = gr.Image(type="filepath", label="Input image")
            prompt = gr.Textbox(label="Edit prompt", lines=3)
            negative = gr.Textbox(label="Negative prompt", value="low quality, blurry, distorted")
            checkpoint = gr.Dropdown(choices=choices, value=choices[0] if choices else None, label="Checkpoint")
            strength = gr.Slider(0.1, 1.0, value=0.55, step=0.05, label="Edit strength")
            steps = gr.Slider(10, 35, value=20, step=1, label="Steps")
            cfg = gr.Slider(1, 12, value=7, step=0.5, label="CFG")
            button = gr.Button("Generate edit", variant="primary")
        with gr.Column():
            result = gr.Image(type="filepath", label="Edited result")
    button.click(run_edit, [source,prompt,negative,strength,steps,cfg,checkpoint], result)
    gr.Markdown("This simple interface uses the included SD 1.5 img2img workflow. Use ComfyUI for node-based editing.")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
