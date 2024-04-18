from __future__ import annotations

import json
import os
from typing import Callable, Any
import time
import sys

class PersistentDict:
    def __init__(self, cache_path: str = "/tmp/persistent_dict.json"):
        self.cache_path = os.path.realpath(cache_path)
        self.cache = {}
        self.f = None

    def __enter__(self) -> PersistentDict:
        assert self.f is None
        cache_dir = os.path.dirname(self.cache_path)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        if os.path.exists(self.cache_path):
            # load cache file
            t0 = time.time()
            cache_str = open(self.cache_path).read().rstrip(",\n")
            o_list = json.loads(f"[{cache_str}]")
            for o in o_list:
                self.cache[o["key"]] = o["val"]
            t1 = time.time()
            print(f"cache load time {self.cache_path}: {t1-t0}", file=sys.stderr)

        # open cache file to write
        self.f = open(self.cache_path, "a")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert self.f is not None
        self.f.close()
        self.f = None

    def get_or_set(self, key: str, get: Callable[[], Any]) -> Any:
        assert self.f is not None
        if key not in self.cache:
            val = get()
            self.cache[key] = val
            self.f.write(json.dumps({
                "key": key,
                "val": val,
            }) + ",\n")

        return self.cache[key]
