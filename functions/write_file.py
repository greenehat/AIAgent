import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes data to existing files in the specified directory or creates a new file and directories if needed, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write files to, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file provided in file_path",
            ),
        },
        required=["file_path","content"]
    ),
)

def write_file(working_directory, file_path, content):
    working_directory_abs = os.path.abspath(working_directory)
    
    if os.path.isabs(file_path):
        full_file_path = file_path
    else:
        full_file_path = os.path.join(working_directory_abs, file_path)

    work_dir_real = os.path.realpath(working_directory_abs)
    full_file_path_real = os.path.realpath(full_file_path)

    
    if os.path.commonpath([work_dir_real, full_file_path_real]) != work_dir_real:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    parent = os.path.dirname(full_file_path_real)
    try:
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(full_file_path_real, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"