import os

def write_file(working_directory, file_path, content):
    working_directory_abs = os.path.abspath(working_directory)
    
    if os.path.isabs(file_path):
        full_file_path = file_path
    else:
        full_file_path = os.path.join(working_directory_abs, file_path)

    
    if not full_file_path.startswith(working_directory_abs):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_file_path):
        return os.makedirs(full_file_path, exist_ok=False)