from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uvicorn
import streams
from runner import stablediffusion, llammlein1b

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.post("/image")
async def generate_image(request: Request):
    data = await request.json()
    prompt = data.get('prompt')
    total_steps = data.get('total_steps')
    stream = streams.DiffuserStream(total_steps)

    if not prompt:
        raise HTTPException(status_code=400, detail="Missing prompt")
            
    asyncio.create_task(stablediffusion.run_prompt(prompt, stream))
    return StreamingResponse(stream.get_async_generator(), media_type='application/json')

@app.post("/text")
async def generate_text(request: Request):
    data = await request.json()
    prompt = data.get('prompt')
    stream = streams.TransformerStream()

    if not prompt:
        raise HTTPException(status_code=400, detail="Missing prompt")

    asyncio.create_task(llammlein1b.run_prompt(prompt, "user", stream))
    return StreamingResponse(stream.get_async_generator(), media_type='application/json')

@app.get("/list-models")
async def list_models():
    return JSONResponse({"models": [
        {
            "name": "Stable Diffusion v1.5",
            "id": "stablediffusion",
            "type": "python",
            "outputType": "imageStream",
            "inputType": ["text"],
            "endpoint": "îmage/"
        },
        {
            "name": "LläMmlein-1b",
            "id": "llammlein1b",
            "type": "python",
            "outputType": "textStream",
            "inputType": ["text"],
            "endpoint": "text/"
        }
    ]})

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(uvicorn.run("service:app", host="127.0.0.1", port=8000, reload=True))