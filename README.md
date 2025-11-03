# BlockedIn-Backend

BlockedIn-Backend is a FastAPI application that analyzes a user's focus during gameplay by combining real-time biometric data with in-game performance metrics.

The service uses a webcam to track facial expressions and gaze direction, and it receives game statistics (like accuracy and lines per minute) via a WebSocket. This combined data is then sent to a Groq AI model to generate a real-time "focus" score and a textual reason for that score.

## Features

  * **Real-time Emotion Detection**: Uses `deepface` and OpenCV to capture webcam video and determine the user's dominant facial expression.
  * **Gaze Tracking**: Implements a `gazetracking` module using `dlib` and OpenCV to track the user's gaze and determine if they are looking left, right, or at the center of the screen.
  * **AI-Powered Focus Analysis**: Collects emotion history, gaze history, and game metrics (accuracy, lines per minute) and sends them to a Groq LLM to generate a JSON response with a "focus" percentage and "reason".
  * **WebSocket API**: Uses FastAPI to provide a WebSocket endpoint (`/ws`) for real-time, bidirectional communication with a client application.
  * **Asynchronous Tracking**: Gaze and emotion tracking run in separate asynchronous tasks to continuously collect data without blocking the main server.

## How It Works

1.  **Startup**: When the FastAPI server starts, it initializes the `GazeController` and `EmotionController`, which begin capturing data from the user's webcam in the background.
2.  **Client Connection**: A client (e.g., a web-based game) connects to the `/ws` endpoint.
3.  **Data Exchange**: The client can send JSON messages to the server to:
      * Report game accuracy: `{"endpoint": "sendAverage", "message": 0.85}`
      * Report lines per minute: `{"endpoint": "sendLineGrowth", "message": 10}`
      * Request the latest gaze history: `{"endpoint": "gaze"}`
      * Request the latest emotion history: `{"endpoint": "emotion"}`
      * Request a new focus analysis: `{"endpoint": "getFocus"}`
4.  **AI Analysis**: When a `getFocus` request is received, the server's `Algorithm` class compiles all the data (gaze, emotion, accuracy, etc.) into a prompt, sends it to the Groq API, and returns the AI's JSON response to the client.

## Setup

### Prerequisites

  * Python 3.10+
  * A webcam
  * A Groq API key

### Installation

1.  Clone the repository:

    ```sh
    git clone <repository-url>
    cd BlockedIn-Backend
    ```

2.  Create a virtual environment and activate it:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4.  This project requires `dlib`. You may need to install its system dependencies first.

      * **macOS**: `brew install cmake dlib`
      * **Ubuntu**: `sudo apt-get install build-essential cmake libopenblas-dev libx11-dev dlib-bin`

5.  Create a `.env` file in the root directory and add your Groq API key:

    ```env
    KEY="gsk_YourGroqApiKeyHere"
    ```

### Running the Server

Run the application using `uvicorn`:

```sh
uvicorn main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.

## WebSocket API

Connect to `ws://127.0.0.1:8000/ws`.

**Client to Server Messages (Send):**

  * `{"endpoint": "sendAverage", "message": <float>}`: Sends the user's current game accuracy (e.g., `0.9` for 90%).
  * `{"endpoint": "sendLineGrowth", "message": <float>}`: Sends the user's current lines per minute.
  * `{"endpoint": "gaze"}`: Requests the recent gaze history.
  * `{"endpoint": "emotion"}`: Requests the recent emotion history.
  * `{"endpoint": "getFocus"}`: Requests a new focus analysis from the AI.

**Server to Client Messages (Receive):**

  * `{"message": ["center", "center", "left", ...]}`: Response for `gaze` request.
  * `{"message": ["happy", "neutral", "happy", ...]}`: Response for `emotion` request.
  * `{"message": {"focus": 92, "reason": "User is maintaining central gaze..."}}`: Response for `getFocus` request.
  * `{"message": []}`: Default response if the endpoint is not recognized.
