import logging
from dataclasses import dataclass
from typing import List


logger = logging.getLogger(__name__)


@dataclass
class Task:
    url: str

@dataclass
class Result:
    error_code: str
    src_url: str
    extracted_urls: List[str]


class Crawler:


    def __init__(self):
        pass

    def extract_urls(self, url: str):
        pass

    def _download(self, url: str):
        pass

    def download_resources(self, List[str]):
        pass
