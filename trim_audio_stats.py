#!/usr/bin/env python
import json
import os

from tqdm import tqdm

if __name__ == "__main__":
    cache_path: str = "/tmp/audio_stats.tmp"
    cache = []
    with open(cache_path) as f:
        for line in tqdm(list(f), desc=f"loading cache {cache_path} ..."):
            o = json.loads(line)
            cache.append(o)

    cache.sort(key=lambda o: o["path"])

    with open("audio_stats.tmp", "w") as f:
        for o in tqdm(cache, desc=f"writing cache ..."):
            if not os.path.exists(o["path"]):
                continue
            f.write(json.dumps(o) + "\n")
