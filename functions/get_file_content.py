import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads a file in a specified directory relative to the working directory, and truncates the output if it surpases a maximum number of characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to file to work from, relative to the working directory",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    work_dir = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(work_dir, file_path))
    valid_file_path = os.path.commonpath([work_dir, target_file]) == work_dir

    try:
        if not valid_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(target_file, "r") as f:
                file_content_string = f.read(MAX_CHARS)
                if f.read(1):
                    file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return file_content_string

    except Exception as error:
        return f"Error: {error}"
