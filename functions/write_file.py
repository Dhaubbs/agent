import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    work_dir = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(work_dir, file_path))
    valid_file_path = os.path.commonpath([work_dir, target_file]) == work_dir

    try:
        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        else:
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            with open(target_file, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as error:
        return f"Error: {error}"
