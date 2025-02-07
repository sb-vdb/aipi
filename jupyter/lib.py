import os
import pathlib
import json
import time
import requests
import base64
from io import BytesIO
from PIL import Image
import torch
from IPython.display import display, HTML

##############################################################################################################################
# For PyTorch
# Huggingface's Pipeline libraries often allow to pass a function or a streamer-object to be passed to the generation-function
# I use it for both Transformer and Diffuser pipelines to extract tokens or intermediate images from the running process.
# by default, these libraries only print final answers or generation meta info to the process output.

# pass the whole object to the TransformerPipeline
class TransformerStream:
    def __init__(self):
        # specific to the used model, so has to be set (see method) during runtime
        self.tokenizer = None 
        
    # required by the TransformeerPipeline to write each output to
    def put(self, message):
        token = self.tokenizer.decode(message[0], skip_special_tokens=False)
        print(token, end="")

    # also required to handle the final step
    def end(self):
        print("\n", "Generation function output:")
        print("\n")
    
    # pass the same tokenizer instance you (would) use for running the model
    def set_tokenizer(self, tokenizer):
        self.tokenizer = tokenizer

class DiffuserStream:
    def __init__(self, total_steps, init_step=0):
        # Variables to help keep track of times
        self.init_step = init_step
        self.total_steps = total_steps
        self.step = init_step
        self.start_time = time.time()
        self.checkpoint = time.time()
        self.step_elapsed = None
        self.step = 0
        self.total_elapsed = 0
        self.remaining = None
    
    # the function required by the DiffuserPipeline
    # with DiffuerPipelines, only this method is passed, not the whole DiffuserStream object
    def write(self,p,i,t, callback_kwargs):

        # helper function that makes time-strings like 24:59:59 or 01:01:01
        def get_time_str(total_seconds):
            def get_digits(number):
                return f"0{number}" if number < 10 else f"{number}"
            total_seconds = total_seconds
            days = total_seconds // (24 * 3600)
            remaining_seconds = total_seconds % (24 * 3600)
            hours = remaining_seconds // 3600
            remaining_seconds %= 3600
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60
            if days > 0:
                return f"{days}:{get_digits(hours)}:{get_digits(minutes)}:{get_digits(seconds)}"
            elif hours > 0:
                return f"{get_digits(hours)}:{get_digits(minutes)}:{get_digits(seconds)}"
            elif minutes > 0:
                return f"{get_digits(minutes)}:{get_digits(seconds)}"
            else:
                return f"{get_digits(seconds)}" + "s"

        # calculate new step meta data    
        now = time.time()
        self.total_elapsed = now - self.start_time
        self.step_elapsed = now - self.checkpoint
        self.remaining = int((self.total_elapsed / (self.step)) * (self.total_steps - (self.step))) if self.step >= (self.init_step + 1) else None
        self.checkpoint = time.time()
        # extract intermediate image data and convert to a base64 string
        latents = callback_kwargs["latents"]
        image = self.latents_to_rgb(latents[0])
        img_b64  = f"data:image/png;base64,{self.image_to_base64(image)}"

        # this HTML piece is to be rendered in Jupyter's process output
        html = HTML(f"""
           <div style="display: flex; flex-direction: row">
              <img src=\"{img_b64}\" width=\"150px\" height=\"150px\"/>
              <div style="margin-left: 20px; margin-top: 5px; font-family: monospace">
                  <p>Step {self.step}/{self.total_steps}</p>
                  <p>Time elapsed (total): {get_time_str(self.total_elapsed)}</p>
                  <p>Time elapsed (last step): {get_time_str(self.step_elapsed) if self.step_elapsed else 'na' }</p>
                  <p>Time remaining (total): {(get_time_str(self.remaining) if self.remaining else 'na')}</p>
              </div>
            </div>
        """)      
        
        display(html, clear=True)
        self.step += 1
        return callback_kwargs

    def get_total_steps(self):
        return self.total_steps
    
    # this function is part of huggingface's guide on how to extract progress data,
    # such as every intermediate image generated during the diffusion process
    # https://huggingface.co/docs/diffusers/main/en/using-diffusers/callback
    def latents_to_rgb(self, latents):
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
    def image_to_base64(self, image: Image) -> str:
        """Convert PIL Image to base64 string."""
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str

# as per ollama documentation, the rest api accepts image data as a json-embedded base64 bytecode
# as per ChatGPT, this code converts it (so far it actually does)
def image_file_to_base64(image_path):
    with Image.open(image_path) as img:
        # Save the image to a bytes buffer
        buffered = BytesIO()
        img.save(buffered, format="PNG")  # You can change format if needed (e.g., JPEG)
        # Convert the bytes to base64
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_base64


def ensure_dest_folder(foldername):
    path = pathlib.Path(foldername)
    if not path.is_dir():
        os.mkdir(foldername)


################################################################################################
# For OLLAMA
# if stream attr is false, then the response will not be created until all tokens are generated. 
# the response will contain all token records that need to be extracted 
def extract_responses(response, history=False):
    text = ""
    agg = ""    # aggregator to help add newline chars that belong to record,
    # but are wrongfully removed, because:
    # text is split by newline chars, due to the collection being a string of newline-separated strings of json,
    # simply converting as json would not work because of missing commas in the string
    for item in response.text.split("\n"):
        if item.endswith("}"):
            obj = json.loads(agg + item)
            record = obj.get("message").get("content") if history else obj.get("response")
            if obj.get("done"):
                text += f"\n Query Data:\n{record}"
            agg = ""
        else:
            agg += item + "\n"
    print(text)
    return text

# if stream attr is true, then the response will be created with the first token record that arrives back.
# its method iter_lines() will provide all received and incoming records (subsequent responses) as an iterator
def extract_response_stream(response, history=False):
    text = ""
    for message in response.iter_lines():
        obj = json.loads(message)
        record = obj.get("message").get("content") if history else obj.get("response")
        text += record
        print(record, end="")
        if obj.get("done"):
            metadata = f"\n Query Data:\n{obj}"
            text += metadata
            print(metadata)
    return text

def without_chain_of_thought(text: str, model):
    if model == "deepseek-r1":
        return text.split("</think>")[1].lstrip()
    else:
        return text


def unload_model(url, model):
    requests.post(url, json={
        "model": model,
        "keep_alive": 0
    })

def to_message(role, text, image=None, images=None):
    msg = {
        "role": role,
        "content": text
    }
    if image:
        msg["images"] = [image]
    elif images:
        msg["images"] = images
    return msg