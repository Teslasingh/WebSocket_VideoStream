import asyncio
import websockets
import base64

# WebSocket Server address and port
WEBSOCKET_SERVER = "0.0.0.0"
WEBSOCKET_PORT = 8765

# Store connected clients
clients = set()

async def on_connect(websocket, path):
    global clients
    print(f"Client connected from {websocket.remote_address}")
    clients.add(websocket)

    try:
        while True:
            data = await websocket.recv()
            # Broadcast the received frame to all connected clients
            await asyncio.gather(
                *[client.send(data) for client in clients if client != websocket]
            )

    except websockets.ConnectionClosed:
        print(f"Client {websocket.remote_address} disconnected")
        clients.remove(websocket)

async def main():
    server = await websockets.serve(on_connect, WEBSOCKET_SERVER, WEBSOCKET_PORT)

    print(f"WebSocket server started on ws://{WEBSOCKET_SERVER}:{WEBSOCKET_PORT}")

    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())

