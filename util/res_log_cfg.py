import logging
import os
from importlib import reload
from typing import Dict

from util.data_src.data_src import DataSrc
from util.data_src.file_data_src import FileDataSrc


def get_res(*sub_path_to_file: str) -> str:
    RES_DIR = "res"
    path = os.path.join(RES_DIR, *sub_path_to_file)
    logging.debug(f"Getting resource {path}")
    return path


def res_exists(*sub_path_to_file: str) -> bool:
    return os.path.exists(get_res(*sub_path_to_file))


def setup_log(log_file: str) -> DataSrc:
    LOG_DIR = "log"
    log_path = os.path.join(LOG_DIR, log_file)
    src = FileDataSrc(log_path)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)-10s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
    )
    return src


def get_cfg() -> Dict:
    import cfg

    cfg = reload(cfg)
    return dict(filter(lambda p: not p[0].startswith("__"), vars(cfg).items()))
