import base64
import io

import websockets
import asyncio
from PIL import Image


async def client():
    async with websockets.connect('ws://localhost:21157') as ws:
        await ws.send(r'D:\fuck163music')
        while True:
            head = await ws.recv()
            if head == 'ok':
                op = await ws.recv()
                print(op, 'was ok')
            elif head == 'bad':
                op = await ws.recv()
                print(op, 'was bad')
            elif head == 'candidates':
                op = await ws.recv()
                print(op, 'has candidates')
                paths = []
                for i in range(await ws.recv()):
                    paths.append(await ws.recv())
                    Image.open(paths[-1]).show()

                # while True:
                #     op = await ws.recv()
                #     if op == b'images-base64':
                #         break
                #     else:
                #         paths.append(paths)
                #
                # candidate_images = []
                # for _ in paths:
                #     data = base64.b64decode(await ws.recv())
                #     mem = io.BytesIO(data)
                #     candidate_images.append(Image.open(mem))
                #
                # candidates = dict(zip(paths, candidate_images))
                # for album_art_path, img in candidates.items():
                #     img.show()

                ws.send(['candidate', 2])


asyncio.get_event_loop().run_until_complete(client())
