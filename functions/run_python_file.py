import subprocess
import os
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python files in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python file to run, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments that can be passed to the python file being run",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    working_directory_abs = os.path.abspath(working_directory)
    
    if os.path.isabs(file_path):
        full_file_path = file_path
    else:
        full_file_path = os.path.join(working_directory_abs, file_path)

    work_dir_real = os.path.realpath(working_directory_abs)
    full_file_path_real = os.path.realpath(full_file_path)

    if os.path.exists(full_file_path_real) != True:
        return f'Error: File "{file_path}" not found.'
    if full_file_path_real.endswith(".py") != True:
        return f'Error: "{file_path}" is not a Python file.'
    if os.path.commonpath([work_dir_real, full_file_path_real]) != work_dir_real:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    try:
        result = subprocess.run(['python3', file_path, *args], cwd=work_dir_real, timeout= 30, capture_output= True, text=True, check=True )
        if result.stdout == "" and result.stderr == "":
            return "No Output produced."
        if result.stdout != "":
            return f"STDOUT:{result.stdout}"
        elif result.stderr != "":
            return f"STDERR:{result.stderr}"
    except subprocess.CalledProcessError as e:
        return f"STDERR: Process exited with code {e.returncode}\n{e}"