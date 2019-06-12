import base64
import io

import websockets
import asyncio

from covers import process_root
from PIL import Image


def base64_image(path):
    img = Image.open(path)

    mem = io.BytesIO()
    img.save(mem, format='PNG')
    return base64.b64encode(mem.getvalue())


async def server(ws, path):
    root_path = await ws.recv()
    for path, albums in process_root(root_path):
        print(path)
        for status, *args in albums():
            print(status, args)
            if 'candidates' in status:
                if not args[1]:
                    await ws.send(['bad', args[0]])
                    continue

                await ws.send(['candidates', args[0], str(len(args[1]))] + list(args[1]))
                # await ws.send([b'images-base64'] + list(map(base64_image, args[1])))
                head, decision = await ws.recv(), await ws.recv()
                print(head, decision)
            else:
                await ws.send(['ok', args[0]])
    print('done')


if __name__ == '__main__':
    start_server = websockets.serve(server, 'localhost', 21157)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
