import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt


def main():
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="AI Agent Prompt")
    parser.add_argument(
        "user_prompt",
        type=str,
        help="User prompt",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")    
    args = parser.parse_args()
    if args.verbose:
        print("User prompt:", args.user_prompt)




    # Load environment variables and get API key
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables.")

    # Create Gemini client
    client = genai.Client(api_key=api_key)

    # Build messages
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)]
        )
    ]

    # Call the model
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    # Check usage metadata
    if response.usage_metadata is None:
        raise RuntimeError("Usage metadata is missing in the response.")

    # Print usage and response
    if args.verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print(response.text)


if __name__ == "__main__":
    main()

