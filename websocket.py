# websocket_server.py
import asyncio
import datetime

import websockets


async def send_time(websocket):
    await websocket.send("start")
    await asyncio.sleep(2)
    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # await websocket.send(f"The current time is: {now}")
        await websocket.send("rotate")
        await asyncio.sleep(0.5)
        await websocket.send("left")
        await asyncio.sleep(0.5)
        await websocket.send("right")
        await asyncio.sleep(0.5)
        await websocket.send("drop")
        await asyncio.sleep(0.5)


async def consumer_handler(websocket):
    async for message in websocket:
        print(f"Message received from client: {message}")
        await websocket.send(f"Echo: {message}")


async def handler(websocket, path):
    consumer_task = asyncio.create_task(consumer_handler(websocket))
    producer_task = asyncio.create_task(send_time(websocket))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
