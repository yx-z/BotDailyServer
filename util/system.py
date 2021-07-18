import _thread as thread
from importlib import reload

import config
import logging
import os
import sys
import threading
import traceback
from typing import Callable, Dict

from util.data_src.data_src import DataSrc
from util.data_src.file_data_src import FileDataSrc


def get_resource_path(*sub_path_to_file: str) -> str:
    path = os.path.join("res", *sub_path_to_file)
    logging.debug(f"Opening resource {path}")
    return path


def resource_exists(*sub_path_to_file: str) -> bool:
    return os.path.exists(get_resource_path(*sub_path_to_file))


def threaded(job_func: Callable):
    def job(*args, **kwargs):
        job_thread = threading.Thread(target=job_func, args=args, kwargs=kwargs)
        job_thread.start()

    return job


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


def setup_log(log_file: str) -> DataSrc:
    LOG_DIR = "log"
    log_path = os.path.join(LOG_DIR, log_file)
    src = FileDataSrc(log_path)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-10s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
    )
    return src


def get_config() -> Dict:
    config = reload(config)
    return dict(filter(lambda p: not p[0].startswith("__"), vars(config).items()))
