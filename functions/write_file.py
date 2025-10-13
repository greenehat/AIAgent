import os

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