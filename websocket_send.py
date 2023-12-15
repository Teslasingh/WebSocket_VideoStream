import cv2 as cv
import asyncio
import base64
import websockets
import time

# Server IP address and port for WebSocket connection
WEBSOCKET_SERVER = "ws://34.93.212.15:8765"
# Topic on which frame will be sent
WEBSOCKET_SEND = "/home/server"

# Object to capture the frames
cap = cv.VideoCapture(0)

# Set the resolution to 640p (1280x720)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

async def send_frame(websocket, path):
    try:
        while True:
            start = time.time()
            # Read Frame
            _, frame = cap.read()
            # Encoding the Frame
            _, buffer = cv.imencode(".jpg", frame)
            # Converting into encoded bytes
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            # Sending the Frame to the WebSocket server
            await websocket.send(jpg_as_text)
            #end = time.time()
            #t = end - start
            #fps = 1 / t
            #print(fps)
            await asyncio.sleep(0.1)  # Adjust as needed to control frame rate
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()

async def main():
    async with websockets.connect(WEBSOCKET_SERVER + WEBSOCKET_SEND) as websocket:
        await send_frame(websocket, WEBSOCKET_SEND)

if __name__ == "__main__":
    #asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

