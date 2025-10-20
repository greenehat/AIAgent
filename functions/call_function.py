from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file 
from functions.run_python_file import run_python_file
from google.genai import types

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    function_call_part.args["working_directory"] = "./calculator"

    functions_dict = {"get_files_info": get_files_info,
                      "get_file_content": get_file_content,
                      "write_file": write_file,
                      "run_python_file": run_python_file
                      }

    
    found_function = None
    for function in functions_dict:
        if function == function_call_part.name:
            found_function = function
        
    if found_function is not None:
        function_result = functions_dict[found_function](**function_call_part.args)
        return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"result": function_result},
                    )
                ],
            )
    else:
        return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )

    