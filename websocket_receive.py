import asyncio
import websockets
import cv2
import numpy as np
import base64

# WebSocket Server address and port
WEBSOCKET_SERVER = "ws://34.93.212.15:8765"  # Change this to your server IP or hostname
WEBSOCKET_RECEIVE = "/home/server"

async def receive_frames(websocket):
    try:
        while True:
            data = await websocket.recv()
            #print(data)
            # Decode the received base64-encoded image
            img_data = base64.b64decode(data)
            # Convert the binary data to a NumPy array
            nparr = np.frombuffer(img_data, np.uint8)
            # Decode the NumPy array to an OpenCV image
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Display the frame or process it as needed
            cv2.imshow('Received Frame', frame)
            cv2.waitKey(1)  # Adjust as needed to control display rate

    except websockets.ConnectionClosed:
        print("Connection to the WebSocket server closed.")

async def main():
    async with websockets.connect(WEBSOCKET_SERVER + WEBSOCKET_RECEIVE) as websocket:
        await receive_frames(websocket)

if __name__ == "__main__":
    asyncio.run(main())

