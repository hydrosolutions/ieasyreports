import importlib


def import_from_string(import_path: str):
    """
    Attempt to import a class from a string representation or raise an ImportError.
    """
    try:
        path_parts = import_path.split('.')
        module_path, class_name = '.'.join(path_parts[:-1]), path_parts[-1]
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError):
        raise ImportError("Could not import '{}'".format(import_path))
