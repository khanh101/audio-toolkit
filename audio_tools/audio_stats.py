from __future__ import annotations

import json
import os
from typing import *

from tqdm import tqdm

from .flac_reader import get_flac_duration
from .wav_reader import get_wav_duration

get_duration = {
    ".wav": get_wav_duration,
    ".flac": get_flac_duration,
}


class AudioStats:
    def __init__(self, cache_path: str = "/tmp/audio_stats.tmp"):
        self.cache_path = cache_path
        self.cache = {}

        self.opened = False
        self.f = None

    def __enter__(self) -> AudioStats:
        if self.opened:
            raise RuntimeError("context cannot be entered multiple times")

        self.opened = True
        # init cache
        cache_dir = os.path.dirname(self.cache_path)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        if os.path.exists(self.cache_path):
            # read cache
            with open(self.cache_path) as f:
                for line in tqdm(list(f), desc=f"loading cache {self.cache_path}"):
                    o = json.loads(line)
                    path, frame_count, sample_rate = o["path"], o["frame_count"], o["sample_rate"]
                    self.cache[path] = {
                        "frame_count": frame_count,
                        "sample_rate": sample_rate,
                    }
        # open file
        self.f = open(self.cache_path, "a")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.opened:
            raise RuntimeError("context cannot be exited without entering")

        self.opened = False
        self.f.close()
        self.f = None

    def read(self, path: str) -> Dict[str, Union[int, float]]:
        if not self.opened:
            raise RuntimeError("read only within context")

        path = os.path.realpath(path)

        if path not in self.cache:
            ext = os.path.splitext(path)[1]
            frame_count, sample_rate = get_duration[ext](path)

            o = {
                "path": path,
                "frame_count": frame_count,
                "sample_rate": sample_rate,
            }
            self.cache[path] = o
            self.f.write(json.dumps(o) + "\n")

        return self.cache[path]
