"""
03_call_llm_direct.py
---------------------
Phase 1: Direct LLM API call using pure HTTP (httpx).
No frameworks, no SDKs.

Target: Google Gemini 1.5 Flash via REST API.
"""

import os
import httpx
from dotenv import load_dotenv

# 1. Load the secret API key from our git-ignored .env file
load_dotenv()

def generate_ai_response(prompt: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing! Please set it in your .env file.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    print(f"Sending prompt to Gemini: '{prompt}'...")

    try:
        response = httpx.post(url, headers=headers, json=payload, timeout=20.0)
        
        print(f"HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Defensive navigation through the response dictionary
            candidates = data.get("candidates", [])
            if not candidates:
                return "Error: No candidates returned by model."
            
            first_candidate = candidates[0]
            parts = first_candidate.get("content", {}).get("parts", [])
            if not parts:
                return "Error: Candidate has no content parts."
            
            text = parts[0].get("text", "")
            return text
        else:
            print(f"[API ERROR] Status: {response.status_code}")
            print(f"Details: {response.text}")
            return f"Error: Request failed with status {response.status_code}"

    except httpx.TimeoutException:
        return "Error: The request timed out waiting for the LLM to reply."
    except httpx.RequestError as exc:
        return f"Error: Network issue occurred: {exc}"

if __name__ == "__main__":
    user_prompt = "Explain why the sky is blue in two simple sentences."
    answer = generate_ai_response(user_prompt)
    print("\n--- Model Response ---")
    print(answer)
    print("----------------------")
