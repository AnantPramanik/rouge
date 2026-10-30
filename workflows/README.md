`image_edit_api.json` is an API-format workflow for a basic SD 1.5 image-to-image pipeline.
It uses only built-in ComfyUI nodes. Replace the checkpoint name with the exact filename
installed in `ComfyUI/models/checkpoints/`.

This is a starter workflow, not a dedicated instruction-following image-edit model.
For semantic edits, use a model and official ComfyUI workflow designed for image editing,
then update the node mapping in `app/gradio_app.py`.
