import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    work_dir = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(work_dir, directory))
    valid_target_dir = os.path.commonpath([work_dir, target_dir]) == work_dir
    try:
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        else:
            return get_dir_info(os.listdir(target_dir), target_dir)
            #return f'Success: "{directory}" is within the working directory'
    except Exception as error:
        return f"Error: {error}"

def get_dir_info(dir_contents: list, target_dir: str) -> str:
    output_list = []

    try:
        for item in dir_contents:
            item_path = os.path.normpath(os.path.join(target_dir, item))
            dir_check = os.path.isdir(item_path)
            size = os.path.getsize(item_path)
            output_list.append(
                f"- {item}: file_size={size}, is_dir={dir_check}"
            )

    except Exception as error:
        return f'Error: {error}'

    return "\n".join(output_list)
