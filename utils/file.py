
import json


def read_json(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    return json.loads(data)


async def async_write_stream(file_path, stream):
    with open(file_path, 'wb') as fd:
        while True:
            chunk = await stream.content.read()
            if not chunk:
                break
            print("w.")
            fd.write(chunk)


def write_bytes(file_path, bytes):
    with open(file_path, 'wb') as f:
        f.write(bytes)