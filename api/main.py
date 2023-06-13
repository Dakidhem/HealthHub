import uvicorn
from fastapi import FastAPI, File, UploadFile , WebSocket
import keras.utils as image
from model import model
import numpy as np
from PIL import Image
from io import BytesIO
from keras.applications.imagenet_utils import decode_predictions
from fastapi.middleware.cors import CORSMiddleware
import flwr as fl
import cv2
import asyncio
import json


app = FastAPI()
    
def predict(image: Image.Image):
    all_labels=['Atelectasis', 'Cardiomegaly', 'Consolidation', 'Edema', 'Effusion', 'Emphysema', 'Fibrosis', 'Hernia', 'Infiltration', 'Mass', 'Nodule', 'Pleural_Thickening', 'Pneumonia', 'Pneumothorax']
    image = np.asarray(image.resize((224, 224)))
    image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
    image = np.expand_dims(image, 0)
    image = image / 255
    result = model.predict(image)
    pred_str = [f'{n_class[:4]}:{p_score*100:.2f}%'
        for n_class, p_score 
        in zip(all_labels,result[0]) 
        if (p_score>0.1)]
    return pred_str

def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict")
async def predict_api(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        
        return str(file.filename.split(".")[-1])
    image = read_imagefile(await file.read())
    prediction = predict(image)
    return prediction



async def send_output(websocket):
    
    process = await asyncio.create_subprocess_exec(
        "python", "start_flower_server.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    while True:
        try:
            stdout_data = await asyncio.wait_for(process.stdout.readline(), timeout=0.1)
            stdout_data = stdout_data.decode().strip()
            if stdout_data:
                stdout_message = {"type": "info", "text": stdout_data}
                await websocket.send_text(json.dumps(stdout_message))
        except asyncio.TimeoutError:
            pass

        try:
            stderr_data = await asyncio.wait_for(process.stderr.readline(), timeout=0.1)
            stderr_data = stderr_data.decode().strip()
            if stderr_data:
                stderr_message = {"type": "warning", "text": stderr_data}
                await websocket.send_text(json.dumps(stderr_message))
        except asyncio.TimeoutError:
            pass

        if process.returncode is not None:
            # Process has finished, break the loop
            break

    await websocket.close()



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    starting_message={"type":"success","text":"Starting the federated process ..."}
    await websocket.send_text(json.dumps(starting_message))
    # Start a task to send the Flower server output to the WebSocket client
    await send_output(websocket)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app,port=7000)
