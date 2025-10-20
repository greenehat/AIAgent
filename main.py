import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

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
     

system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

def generate_content(client, messages, verbose):
    
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents= messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),
    )
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
         
    print("Response:")
    if response.function_calls:
        called_function = response.function_calls[0]
        function_call_result = call_function(called_function,verbose=verbose)
        if not (hasattr(function_call_result,"parts")
            and len(function_call_result.parts) != 0
            and hasattr(function_call_result.parts[0],"function_response")
            and hasattr(function_call_result.parts[0].function_response,"response")):
            raise Exception("Error calling function")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)



if __name__ == "__main__":
    main()