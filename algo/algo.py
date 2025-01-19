from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()



class Algorithm():

    def __init__(self):
        self.accuracy = []
        self.correction = []
        self.key = os.getenv("KEY")

    def addAccuracy(self, accuracy):
        self.accuracy.append(accuracy)

        if len(self.accuracy) > 20:
            self.accuracy.pop(0)

    def addCorrection(self, correction):
        self.correction.append(correction)

        if len(self.correction) > 20:
            self.correction.pop(0)
        
    def buildPrompt(self, face, gaze):

        print(self.key)
        client = Groq(api_key=self.key)

        
        data = str({
            "Accuracy": self.accuracy,
            "linesPerMinute": self.correction,
            "emotion": face,
            "gaze": gaze
        })

        print(data)

        completion = client.chat.completions.create(
            # model="llama-3.3-70b-versatile",
            model="llama-3.2-3b-preview",        
            messages=[
                {
                    "role": "system",
                    "content": 'You are now BlockedIn api which can determine how focused a user is playing Tetris based on the datasets given. Your job is to determine how much weight to give each data given and produce a percentage that determines how focused the user is.  You have to reasoning and make a proper estimation. The data sets given are:   Percentage of correct choices made in the game of Tetris (anything under 70% is bad; 90%+ is exceptional. PUT MORE WEIGHT INTO THIS FACTOR. Rember to clearly use this value, the lower it is the worse the user is doing thus you should give worse score): PERCENTAGE Lines per minute (anything under 8 lines per minute is mediocre; anything under 3 is shit): FLOAT Where the user is looking for the last 5 seconds to determine how focused he is (centre is the screen is good; any other string that indicates a sense of unfocusedness is bad): STRING Facial Expression of the user for the last minute (angry, fear, and surprised are bad): STRING Using this please return a json put like {"focus ": PERCENTAGE, "reason": STRING}. Please be strict'
                },
                {
                    "role": "user",
                    "content": str(data)
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )

        msg_str = str(completion.choices[0].message.content)

        # print(msg_str)

        return json.loads(msg_str)





