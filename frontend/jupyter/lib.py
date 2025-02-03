import json
from PIL import Image
import io
import base64

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
def image_to_base64(image_path):
    with Image.open(image_path) as img:
        # Save the image to a bytes buffer
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")  # You can change format if needed (e.g., JPEG)
        # Convert the bytes to base64
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_base64