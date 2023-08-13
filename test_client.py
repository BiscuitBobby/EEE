import asyncio
import websockets


async def test():
    async with websockets.connect('ws://localhost:8000') as websocket:
        await websocket.send("hello")