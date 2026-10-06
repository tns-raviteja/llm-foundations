"""
02_async_http.py
----------------
Demonstrates:
1. Asynchronous HTTP requests using httpx.AsyncClient.
2. Running multiple concurrent calls with asyncio.gather().
3. Loading environment variables with python-dotenv.
4. Timing execution to see concurrency in action.
"""

import asyncio
import os
import time
import httpx
from dotenv import load_dotenv

# Load any variables defined in a local .env file
load_dotenv()

async def fetch_ai_completion(client: httpx.AsyncClient, request_id: int) -> dict:
    url = "https://httpbin.org/post"
    payload = {
        "request_id": request_id,
        "prompt": f"Simulated prompt #{request_id}"
    }

    print(f"[{time.strftime('%X')}] -> Request #{request_id} SENT")
    
    # Non-blocking async network call:
    response = await client.post(url, json=payload, timeout=10.0)
    
    print(f"[{time.strftime('%X')}] <- Request #{request_id} RECEIVED (Status: {response.status_code})")
    return response.json()

async def main():
    api_key = os.environ.get("LLM_API_KEY", "mock-default-key")
    print(f"Loaded API key from environment: {api_key[:4]}***\n")

    start_time = time.perf_counter()

    # Reuse a single AsyncClient connection pool
    async with httpx.AsyncClient() as client:
        # Create 3 concurrent tasks:
        tasks = [
            fetch_ai_completion(client, 1),
            fetch_ai_completion(client, 2),
            fetch_ai_completion(client, 3)
        ]
        
        # Fire all 3 at the same time:
        results = await asyncio.gather(*tasks)

    elapsed_time = time.perf_counter() - start_time
    print(f"\nAll 3 requests completed in: {elapsed_time:.2f} seconds!")
    print(f"Received {len(results)} valid responses.")

if __name__ == "__main__":
    # asyncio.run starts the Python Event Loop
    asyncio.run(main())
