import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

from functions.call_function import available_functions, call_function
from prompts import system_prompt


def call_model(client, messages):
    return client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )


def generate_content(client, messages, verbose):
    for iteration in range(20):
        try:
            response = call_model(client, messages)
        except APIError as e:
            if getattr(e, "code", None) == 429:
                print("Rate limit exceeded. Cannot continue agent loop.")
                sys.exit(1)
            raise

        # ---- 1️⃣ Add model responses to conversation history ----
        if not response.candidates:
            raise RuntimeError("Model returned no candidates")

        for candidate in response.candidates:
            messages.append(candidate.content)

        # ---- 2️⃣ Final response (no tool calls) ----
        if not response.function_calls:
            print("Final response:")
            print(response.text)
            return

        # ---- 3️⃣ Execute requested tool calls ----
        function_responses = []

        for function_call in response.function_calls:
            if verbose:
                print(f" - Calling function: {function_call.name}")

            result = call_function(function_call, verbose=verbose)

            if (
                not result.parts
                or not result.parts[0].function_response
                or result.parts[0].function_response.response is None
            ):
                raise RuntimeError(
                    f"Invalid or empty function response for {function_call.name}"
                )

            if verbose:
                print(f"-> {result.parts[0].function_response.response}")

            function_responses.append(result.parts[0])

        # ---- 4️⃣ Feed tool results back to the model ----
        messages.append(
            types.Content(
                role="user",
                parts=function_responses,
            )
        )

    # ---- 5️⃣ Safety exit if loop never converges ----
    print("Agent failed to converge after 20 iterations.")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(client, messages, args.verbose)


if __name__ == "__main__":
    main()
