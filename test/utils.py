import os

mydir = os.path.abspath(os.path.dirname(__file__))


def normalize_path(file_path):
    return os.path.join(mydir, file_path)