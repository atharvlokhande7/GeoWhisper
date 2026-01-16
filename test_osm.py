import asyncio
import httpx
import sys

async def test():
    print("Testing imports...", flush=True)
    try:
        url = "https://overpass-api.de/api/interpreter"
        query = """[out:json];node(around:500,48.8584,2.2945)["amenity"];out body;"""
        
        print(f"Connecting to {url}...", flush=True)
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, data={"data": query}, timeout=10.0)
            print(f"Status: {resp.status_code}", flush=True)
            print(f"Data length: {len(resp.content)}", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
