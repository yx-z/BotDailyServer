import _thread as thread
import logging
import os
import sys
import threading
import traceback
from pathlib import Path


def get_resource_path(*sub_path_to_file: str) -> str:
    path = os.path.join("res", *sub_path_to_file)
    logging.debug(f"Opening resource {path}")
    return path


def resource_exists(*sub_path_to_file: str) -> bool:
    return os.path.exists(get_resource_path(*sub_path_to_file))


def interrupt_after(seconds: int):
    def quit_function(function_name: str):
        logging.error(f"Function {function_name} timeout with {seconds} seconds")
        sys.stderr.flush()
        thread.interrupt_main()

    def outer(f):
        if seconds <= 0:
            return f

        def inner(*args, **kwargs):
            timer = threading.Timer(seconds, quit_function, args=[f.__name__, seconds])
            timer.start()
            try:
                result = f(*args, **kwargs)
            finally:
                timer.cancel()
            return result

        return inner

    return outer


def exception_as_str(exception: Exception) -> str:
    return f"Exception: {exception}\nTraceback: {traceback.format_exc()}"


def create_log(log_path: str):
    if not os.path.exists(log_path):
        Path.mkdir(Path(os.path.dirname(log_path)), exist_ok=True, parents=True)
        with open(log_path, "w"):
            pass


def setup_log(log_path: str):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-10s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
    )


def get_log(log_path: str, reverse: bool = False) -> str:
    with open(log_path) as f:
        log = f.readlines()
        if reverse:
            log.reverse()
    return "\n".join(log)
