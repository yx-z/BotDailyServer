import _thread as thread
import logging
import os
import sys
import threading
import time
import traceback
from datetime import datetime, timedelta
from math import ceil
from pathlib import Path
from typing import Callable


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


def get_log(log_path: str, last_n_lines: int = 10) -> str:
    with open(log_path) as f:
        log = f.readlines()
    return "\n".join(log[len(log) - last_n_lines :])


def sleep_until_next_minute():
    now = datetime.now()
    next_minute = datetime(
        now.year, now.month, now.day, now.hour, now.minute
    ) + timedelta(minutes=1)
    sleep_time = max(0, ceil((next_minute - datetime.now()).total_seconds()))
    time.sleep(sleep_time)
