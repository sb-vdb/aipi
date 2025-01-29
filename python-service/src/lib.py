import time
import torch
import base64
from io import BytesIO
from PIL import Image
import json


def get_total_steps():
    return 25

# this function is part of huggingface's guide on how to extract progress data,
# such as every intermediate image generated during the diffusion process
# https://huggingface.co/docs/diffusers/main/en/using-diffusers/callback
def latents_to_rgb(latents):
    weights = (
        (60, -60, 25, -70),
        (60,  -5, 15, -50),
        (60,  10, -5, -35),
    )

    weights_tensor = torch.t(torch.tensor(weights, dtype=latents.dtype).to(latents.device))
    biases_tensor = torch.tensor((150, 140, 130), dtype=latents.dtype).to(latents.device)
    rgb_tensor = torch.einsum("...lxy,lr -> ...rxy", latents, weights_tensor) + biases_tensor.unsqueeze(-1).unsqueeze(-1)
    image_array = rgb_tensor.clamp(0, 255).byte().cpu().numpy().transpose(1, 2, 0)

    return Image.fromarray(image_array)

#Copilot
def image_to_base64(image: Image) -> str:
    """Convert PIL Image to base64 string."""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def read_buffer(step):
    try:
        with open(f"output/buffer_{step}.txt", "r") as f:
            buf = f.read()
    except (FileNotFoundError):
            buf = None
    return buf
        
        
def buffer_generator():
    start_time = time.time()
    checkpoint = 0
    step_time = time.time()
    step = 0
    total_steps = get_total_steps()
    seconds = 0

    while step <= total_steps:
        time.sleep(1)
        now = time.time()
        seconds += 1
        buffer_image = read_buffer(step)
        total_elapsed = now - start_time
        if buffer_image:
            step += 1
            step_time = now
            checkpoint = total_elapsed
            seconds = 0
            
        
        remaining = ((checkpoint / (step - 1)) * (total_steps - (step - 1)) - seconds) if step > 1 else None
        
        
        yield json.dumps({
            "elapsed_step": int(now - step_time),
            "elapsed_total": int(total_elapsed),
            "remaining": int(remaining),
            "status": "init" if step == 0 else "generating" if step <= total_steps else "done",
            "step": step,
            "total_steps": total_steps,
            "image": buffer_image
        }) + "\n"