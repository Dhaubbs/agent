import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a Python file in a specified directory relative to the working directory, capturing the returncode, and timing out after 30 seconds",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to file to work from, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                }
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    work_dir = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(work_dir, file_path))
    valid_target_dir = os.path.commonpath([work_dir, target_dir]) == work_dir
    try:
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        else:
            command = ["python", target_dir]
            if args:
                command.extend(args)
            result = subprocess.run(
                command,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                return f'Process exited with code {result.returncode}\nSTDERR: {result.stderr}'
            if not result.stdout and not result.stderr:
                return 'No output produced'
            return f'STDOUT: {result.stdout} STDERR: {result.stderr}\n'

    except Exception as error:
        return f"Error: executing Python file: {error}"
