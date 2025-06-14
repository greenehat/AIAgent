import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description= "AI Code Assistant",
        epilog= 'Example: python3 main.py "What is the meaning of life?"'
    )
    parser.add_argument(
        "user_prompt", help='Usage: python3 main.py "your AI prompt here"'
    )
    parser.add_argument(
        "--verbose", "--Verbose", action="store_true",
        required=False, help="Includes user prompt, and token information in returned content"
    )
    
    args = parser.parse_args()

        
    user_prompt = args.user_prompt
    verbose = args.verbose

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
   
    if verbose:
        print(f"User prompt: {user_prompt}")
    
    generate_content(client,messages,verbose)
     

def generate_content(client, messages, verbose):
    
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents= messages
    )
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}") 
    print("Response:")
    print(response.text)



if __name__ == "__main__":
    main()