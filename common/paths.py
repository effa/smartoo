import os

# absolute path to base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def project_path(path):
    """
    Transforms project root relative path to full absolute path

    Args:
        path (unicode): path inside project
    Returns:
        absolute path
    """
    return os.path.join(BASE_DIR, path)
