import _thread as thread
import logging
import os
import sys
import threading
import traceback


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
