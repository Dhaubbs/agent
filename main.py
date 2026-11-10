import os
import argparse
import sys
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_functions import available_functions, call_function

def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    token_usage = []

    for _ in range(20):
        loop_capture = generate_content(client, messages, args.verbose, token_usage)
        if loop_capture is not None:
            print(f'User tokens: {sum(t[0] for t in token_usage)}')
            print(f'Response tokens: {sum(t[1] for t in token_usage)}')
            print(loop_capture)
            return
    print("Exceeded 20 iterations, cancelling process")
    sys.exit(1)

def generate_content(client, messages, verbose: bool, token_usage: list) -> None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    message = response.choices[0].message
    messages.append(message) #lets the ai loop dummy

    if response.usage is None:
        raise RuntimeError("usage was None, possible failed API request")

    if verbose:
        print(f"User prompt: {messages}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    tokens = (response.usage.prompt_tokens, response.usage.completion_tokens)
    token_usage.append(tokens)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose)
            if not result_message["content"]:
                raise Exception("Tool returned empty content")
            if verbose == True:
                print(f"-> {result_message['content']}")
            messages.append(result_message)
        return None
    else:
        return message.content

if __name__ == "__main__":
    main()
