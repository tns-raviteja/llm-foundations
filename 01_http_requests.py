"""
01_http_requests.py
-------------------
Demonstrates:
1. Sending a POST request with headers and JSON payload using httpx.
2. Defensive error handling (network exceptions, status codes).
3. Safe JSON extraction using .get() with fallbacks.
"""

import httpx

def send_mock_ai_request():
    url = "https://httpbin.org/post"
    
    headers = {
        "Authorization": "Bearer mock-api-key-xyz",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "mock-llm-v1",
        "prompt": "Hello! How do HTTP requests work in Python?",
        "temperature": 0.7
    }

    print(f"Sending POST request to {url}...")

    try:
        # Timeout after 10 seconds so the script never hangs indefinitely
        response = httpx.post(url, headers=headers, json=payload, timeout=10.0)
        
        print(f"Received HTTP Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            
            # httpbin echoes our sent JSON under the "json" key
            sent_data = data.get("json", {})
            prompt_echo = sent_data.get("prompt", "No prompt found")
            model_used = sent_data.get("model", "Unknown")
            
            print("\n[SUCCESS] Response parsed successfully:")
            print(f"  Model echoed : {model_used}")
            print(f"  Prompt echoed: {prompt_echo}")
        else:
            print(f"\n[ERROR] Server returned non-200 code: {response.status_code}")
            print(f"Response body: {response.text}")

    except httpx.TimeoutException:
        print("\n[ERROR] The request timed out. The server took too long to reply.")
    except httpx.RequestError as exc:
        print(f"\n[ERROR] An HTTP network error occurred: {exc}")

if __name__ == "__main__":
    send_mock_ai_request()
