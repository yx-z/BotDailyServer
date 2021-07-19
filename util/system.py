import _thread as thread
import datetime

import logging
import sys
import threading
import traceback
from typing import Callable


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


def get_days(dt: datetime.datetime) -> int:
    return (datetime.datetime.today() - dt).days
