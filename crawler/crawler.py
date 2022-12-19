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


    def __init__(self, seed_url: str, download_dir: str):

        if not os.path.exists(download_dir):
            os.makedirs(download_dir, exist_ok=True)
        self._download_dir = download_dir
        self._seed_url = seed_url

    def extract_urls(self, url: str):
        pass

    def _download(self, url: str, out
        pass

    def download_resources(self, List[str]):
        pass
