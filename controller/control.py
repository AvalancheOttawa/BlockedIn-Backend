# controller/main_focus.py
from .gaze import GazeData
from .emotion import FaceExpression
import asyncio


class GazeController:
    def __init__(self):
        self.gaze = GazeData()
        self.pastGaze = []
        # Notice: we do NOT call asyncio.create_task(...) here

    async def start_tracking(self):
        """Explicitly start the background task *after* the event loop is running."""
        asyncio.create_task(self._gazing())

    async def _gazing(self):
        while True:
            gaze_data = await asyncio.to_thread(self.gaze.getGaze)
            self.pastGaze.append(gaze_data)

            if len(self.pastGaze) > 15:
                self.pastGaze.pop(0)
            await asyncio.sleep(0.01)
        
    def end(self):
        self.gaze.end()

    def getHistory(self):
        return self.pastGaze


class EmotionController:
    
    def __init__(self):
        self.face = FaceExpression()
        self.emotionHistory = []

    async def start_tracking(self):
        asyncio.create_task(self._expression())

    async def _expression(self):
        while True:
            emotion = await asyncio.to_thread(self.face.getEmotion)
            self.emotionHistory.append(emotion)
            if len(self.emotionHistory) > 15:
                self.emotionHistory.pop(0)
            await asyncio.sleep(2)

    def end(self):
        self.face.end()

    def getHistory(self):
        return self.emotionHistory
