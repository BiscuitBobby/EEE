import asyncio
import websockets

# cumulative sockets
cum_sock = []

# for each connection
async def handler(websocket, path):
    data = await websocket.recv()
    cum_sock.append(websocket)
    response = "connection active"

    while not websocket.closed:
        await asyncio.sleep(1)
        await websocket.send(response)
    cum_sock.remove(websocket)

initialize_server = websockets.serve(handler, "localhost", 800)

asyncio.get_event_loop().run_until_complete(initialize_server)
asyncio.get_event_loop().run_forever()