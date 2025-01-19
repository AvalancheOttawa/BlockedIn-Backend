# main.py
from fastapi import FastAPI, WebSocket
from controller import GazeController, EmotionController
from algo import Algorithm

app = FastAPI()

focus: GazeController | None = None
expression: EmotionController | None = None
algo: Algorithm | None = None

@app.on_event("startup")
async def startup_event():
    global gaze
    global expression
    global algo
    # Create the MainFocus instance *after* FastAPI’s loop is ready
    gaze = GazeController()
    expression = EmotionController()
    # Now start the async tracking
    await gaze.start_tracking()
    await expression.start_tracking()
    algo = Algorithm()





@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # Wait for the client to send a message
            data = await websocket.receive_json()
            # print(data)
            endpoint = data["endpoint"]

            # print(endpoint)


            if (endpoint == "gaze"):
                # print("hi")
                await websocket.send_json({"message": gaze.getHistory()})
            elif (endpoint == "emotion"):
                # print("hi1")
                await websocket.send_json({"message": expression.getHistory()})
            elif (endpoint == "sendAverage"):
                # print("hi2")
                algo.addAccuracy(data["message"])
            elif (endpoint == "sendLineGrowth"):
                algo.addCorrection(data["message"])
            elif (endpoint == "getFocus"):
                dum = algo.buildPrompt(expression.getHistory(), gaze.getHistory())
                print(dum)
                await websocket.send_json({"message": dum })
            else:
                await websocket.send_json({"message": []})

        except Exception as e:
            # print(e)
            # break
            data = await websocket.receive_text()
            print(data)
           
            