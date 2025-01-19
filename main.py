# main.py
from fastapi import FastAPI, WebSocket
from controller import GazeController, EmotionController

app = FastAPI()

focus: GazeController | None = None
expression: EmotionController | None = None

@app.on_event("startup")
async def startup_event():
    global gaze
    global expression
    # Create the MainFocus instance *after* FastAPI’s loop is ready
    gaze = GazeController()
    expression = EmotionController()
    # Now start the async tracking
    await gaze.start_tracking()
    await expression.start_tracking()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # Wait for the client to send a message
            endpoint = await websocket.receive_text()

            if (endpoint == "gaze"):
                await websocket.send_json({"message": gaze.getHistory()})
            elif (endpoint == "emotion"):
                await websocket.send_json({"message": expression.getHistory()})
            else:
                await websocket.send_json({"message": []})

        except Exception as e:
            break
           
            