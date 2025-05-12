import asyncio
import datetime
import os
import random
import socket
import time

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

    async def fetch_blockcypher_seed(name: str) -> str:
        res = await client.get(f"https://api.blockcypher.com/v1/{name}/main")
        json = res.json()
        return json["hash"]

    async with httpx.AsyncClient() as client:
        coins = ["btc", "doge", "ltc"]
        results = await asyncio.gather(
            *[fetch_blockcypher_seed(name) for name in coins]
        )
        return "".join(results)


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
    seeds = await asyncio.gather(
        fetch_blockcypher_seeds(),
        fetch_lavarand_seed(),
        fetch_nist_beacon(),
        fetch_qrandom_seed(),
        fetch_random_system_data(),
    )
    mixed = "".join(seeds)

    # Shuffle the string
    mixed = "".join(
        random.sample(mixed, len(mixed))  # ty: ignore[invalid-argument-type]
    )

    return mixed


@app.get("/")
async def h(request):
    start = time.time()
    data = await fetch_all_data()

    return {
        "host": socket.gethostname(),
        "elapsedTime": time.time() - start,
        "utcTimestamp": datetime.datetime.now(datetime.UTC),
        "data": data,
    }


app.start(port=8080)
