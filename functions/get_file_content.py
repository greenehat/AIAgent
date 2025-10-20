import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads file contents truncated to 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to read, relative to the working directory. If not provided, reads files in the working directory itself.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    working_directory_abs = os.path.abspath(working_directory)
    
    if os.path.isabs(file_path):
        full_file_path = file_path
    else:
        full_file_path = os.path.join(working_directory_abs, file_path)

    
    if not full_file_path.startswith(working_directory_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    MAX_CHARS = 10000
    try:
        with open(full_file_path,"r") as f:
            file_content_string = f.read(MAX_CHARS)
    except Exception as e:
        return f"Error: {e}"

    return file_content_string