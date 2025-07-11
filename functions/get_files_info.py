import os


def get_files_info(working_directory, directory=None):
    working_directory_abs = os.path.abspath(working_directory)
    if directory is None:
        directory_abs = working_directory_abs
    else:
        if os.path.isabs(directory):
            directory_abs = os.path.abspath(directory)
        else:
            directory_abs = os.path.abspath(os.path.join(working_directory_abs, directory))
    if not directory_abs.startswith(working_directory_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(directory_abs):
        return f'Error: "{directory}" is not a directory'
    file_info = []
    try:
        for content in os.listdir(directory_abs):
            file_info.append(f"- {content}: file_size={os.path.getsize(os.path.join(directory_abs,content))} bytes, is_dir={os.path.isdir(os.path.join(directory_abs,content))}")
    except Exception as e:
        return f"Error: {e}"
    return "\n".join(file_info)
    