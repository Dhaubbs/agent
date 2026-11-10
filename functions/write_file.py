import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes to a file in a specified directory relative to the working directory, and lists the amount of characters used",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to file to work from, relative to the working directory",
                },
                "content:": {
                    "type": "string",
                    "description": "Content to be written to the file, usually a string",
                }
            },
        },
    },
}

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
