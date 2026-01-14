import os
import argparse
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="AI Agent Prompt")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables.")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=args.user_prompt
    )
    if response.usage_metadata is None:
        raise RuntimeError("Usage metadata is missing in the response.")
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print(response.text)
if __name__ == "__main__":
    main()

