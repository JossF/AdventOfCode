import os


def get_file_location(name: str) -> str:
    file = os.path.join(os.path.dirname(__file__), "data", name)
    return file
