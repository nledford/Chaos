import datetime
import os
import random
import socket

import httpx
from robyn import Robyn

app = Robyn(str(__file__))


async def fetch_random_system_data() -> str:
    """
    Fetches 32 bytes of random data from the host system and returns it as a hexadecimal string
    """
    return os.urandom(32).hex()


async def fetch_blockcypher_seeds() -> str:
    """
    Fetch multiple cryptocurrency hashes from blockcypher and return as a single string
    """
    result = ""

    async with httpx.AsyncClient() as client:
        for name in ["btc", "doge", "ltc"]:
            res = await client.get(f"https://api.blockcypher.com/v1/{name}/main")
            json = res.json()
            result += json["hash"]

        return result


async def fetch_lavarand_seed() -> str:
    """
    Fetches random data from Cloudflare lavarand
    """
    async with httpx.AsyncClient() as client:
        res = await client.get("https://csprng.xyz/v1/api")
        json = res.json()
        return json["Data"]


async def fetch_nist_beacon() -> str:
    """
    Fetches random data from NIST beacon
    """
    async with httpx.AsyncClient() as client:
        res = await client.get("https://beacon.nist.gov/beacon/2.0/pulse/last")
        json = res.json()
        return json["pulse"]["outputValue"]


async def fetch_qrandom_seed() -> str:
    """
    Fetch random data from `qrandom`
    """
    async with httpx.AsyncClient() as client:
        res = await client.get("https://qrandom.io/api/random/string?length=32")
        json = res.json()
        return json["string"][0]


async def fetch_all_data() -> str:
    """
    Fetches random data from all sources and shuffles it together
    """

    # Fetch data from various sources
    # Concat all random data into one string
    mixed = (
        await fetch_blockcypher_seeds()
        + await fetch_lavarand_seed()
        + await fetch_nist_beacon()
        + await fetch_qrandom_seed()
        + await fetch_random_system_data()
    )

    # Shuffle the string
    mixed = "".join(random.sample(mixed, len(mixed)))

    return mixed


@app.get("/")
async def h(request):
    return {
        "host": socket.gethostname(),
        "utcTimestamp": datetime.datetime.now(datetime.UTC),
        "data": await fetch_all_data(),
    }


app.start(port=8080)
