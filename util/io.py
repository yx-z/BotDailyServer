import os


def get_resource_path(*sub_path_to_file: str) -> str:
    return os.path.join("res", *sub_path_to_file)


def resource_exists(*sub_path_to_file: str) -> bool:
    return os.path.exists(get_resource_path(*sub_path_to_file))
