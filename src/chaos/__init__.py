import datetime
import os
import socket

from robyn import Robyn

app = Robyn(__file__)


async def get_random_system_data() -> str:
    """
    Gets 32 bytes of random data from the host system and returns it as a hexadecimal string
    """
    return os.urandom(32).hex()


@app.get("/")
async def h(request):
    return {
        "host": socket.getfqdn(),
        "timestamp": datetime.datetime.now(datetime.UTC),
        "data": await get_random_system_data()
    }


app.start(port=8080)
