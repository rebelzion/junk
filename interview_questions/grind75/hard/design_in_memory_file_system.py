from typing import Dict, Any, Optional, Union, Tuple, List
from dataclasses import dataclass, field
import pytest

@dataclass
class Directory:
    dirs: Dict[str, "Directory"] = field(default_factory=dict)
    files: Dict[str, str] = field(default_factory=dict)

class FileSystem:

    def __init__(self):
        self.root = Directory()

    def ls(self, path: str) -> List[str]:
        if not path:
            return []

        subdirs = path.split("/")
        d = self.root
        for i in range(1, len(subdirs)):
            fname = subdirs[i]
            if not fname:
                continue
            if fname in d.files:
                return [fname]
            if fname not in d.dirs:
                return []
            d = d.dirs[fname]
        files = [fn for fn in d.files.keys()]
        dirs = [dn for dn in d.dirs.keys()]
        return sorted(files + dirs)


    def mkdir(self, path: str) -> None:
        if not path or path == "/":
            return

        subdirs = path.split("/")
        d = self.root
        for i in range(1, len(subdirs)):
            fname = subdirs[i]
            if fname not in d.dirs:
                d.dirs[fname] = Directory()
            d = d.dirs[fname]


    def addContentToFile(self, filePath: str, content: str) -> None:

        subdirs = filePath.split("/")
        d = self.root
        for i in range(1, len(subdirs)):
            fname = subdirs[i]
            if fname in d.dirs:
                d = d.dirs[fname]
            else:
                if i < len(subdirs)-1:
                    d.dirs[fname] = Directory()
                    d = d.dirs[fname]
                else:
                    if fname not in d.files:
                        d.files[fname] = ""
                    d.files[fname] += content

    def readContentFromFile(self, filePath: str) -> str:

        subdirs = filePath.split("/")
        d = self.root
        for i in range(1, len(subdirs)):
            fname = subdirs[i]
            if fname in d.dirs:
                d = d.dirs[fname]
            else:
                return d.files[fname]
        return ""



def generate_tests():
    tests = [
        ((["ls","mkdir","addContentToFile","ls","readContentFromFile"], [["/"],["/a/b/c"],["/a/b/c/d","hello"],["/"],["/a/b/c/d"]]), [[],None, None,["a"],"hello"])
    ]

    return tests

@pytest.mark.parametrize("inp,exp", generate_tests())
def test_solution(inp, exp):

    fs = FileSystem()

    methods, params = inp
    for method_name, param, expected in zip(methods, params, exp):
        func = getattr(fs, method_name)
        output = func(*param)
        assert output == expected
