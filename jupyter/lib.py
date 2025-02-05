import json
from PIL import Image
import time
import base64
from io import BytesIO
from PIL import Image
import torch
from IPython.display import display, HTML

class TransformerStream:
    def __init__(self):
        self.tokenizer = None
        
    def put(self, message):
        token = self.tokenizer.decode(message[0], skip_special_tokens=False)
        print(token, end="")

    def end(self):
        print("\n", "Generation function output:")
        print("\n")
    
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
    
    def write(self,p,i,t, callback_kwargs):

        def get_time_str(total_seconds):
            def get_digits(number):
                number = int(number)
                return f"0{number}" if number < 10 else f"{number}"
            time_str = ""
            h = 0
            m = 0
            s = total_seconds % 60
            time_str = get_digits(s)
            remaining = total_seconds - s
            if total_seconds > 60:
                m_part = remaining % 3600
                m = int(m_part / 60)
                time_str = get_digits(m) + ":" + time_str
                if total_seconds > 3600:
                    h = int((total_seconds - s - m_part) / 3600)
                    time_str = get_digits(h) + ":" + time_str
            else:
                time_str += "s"

            return time_str

        now = time.time()
        self.total_elapsed = now - self.start_time
        self.step_elapsed = now - self.checkpoint
        self.remaining = ((self.start_time - self.checkpoint / (self.step - 1)) * (self.total_steps - (self.step - 1)) - self.step_elapsed) if self.step > (self.step + 1) else None
        self.checkpoint = time.time()
        latents = callback_kwargs["latents"]
        image = self.latents_to_rgb(latents[0])
        img_b64  = f"data:image/png;base64,{self.image_to_base64(image)}"

        html = HTML(f"""
           <div style="display: flex; flex-direction: row">
              <img src=\"{img_b64}\" width=\"150px\" height=\"150px\"/>
              <div style="margin-left: 20px;">
                  <p>Step {self.step}/{self.total_steps}</p>
                  <p>Time elapsed (total): {get_time_str(self.total_elapsed)}</p>
                  <p>Time elapsed (last step): {get_time_str(self.step_elapsed) if self.step_elapsed else 'na' }</p>
                  <p>Time remaining (total): {(get_time_str(self.remaining) if self.remaining else 'na')}"</p>
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

# if stream attr is false, then the response will not be created until all tokens are generated. 
# the response will contain all token records that need to be extracted 
def extract_responses(response):
    text = ""
    agg = ""    # aggregator to help add newline chars that belong to record,
    # but are wrongfully removed, because:
    # text is split by newline chars, due to the collection being a string of newline-separated strings of json,
    # simply converting as json would not work because of missing commas in the string
    for item in response.text.split("\n"):
        if item.endswith("}"):
            obj = json.loads(agg + item)
            text += obj.get("response")
            if obj.get("done"):
                text += f"\n Query Data:\n{item}"
            agg = ""
        else:
            agg += item + "\n"
    print(text)
    return text

# if stream attr is true, then the response will be created with the first token record that arrives back.
# its method iter_lines() will provide all received and incoming records (subsequent responses) as an iterator
def extract_response_stream(response):
    text = ""
    for message in response.iter_lines():
        obj = json.loads(message)
        record = obj.get("response")
        text += record
        print(record, end="")
        if obj.get("done"):
            metadata = f"\n Query Data:\n{obj}"
            text += metadata
            print(metadata)
    return text

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