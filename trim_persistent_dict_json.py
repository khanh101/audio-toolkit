#!/usr/bin/env python
import json
import os
import sys
import time
from tqdm import tqdm

if __name__ == "__main__":
    cache_path = sys.argv[1]
    
    cache = {}

    t0 = time.time()
    cache_str = open(cache_path).read().rstrip(",\n")
    o_list = json.loads(f"[{cache_str}]")
    for o in o_list:
        cache[o["key"]] = o["val"]
    t1 = time.time()
    print(f"cache load time {cache_path}: {t1-t0}", file=sys.stderr)

    for k, v in tqdm(cache.items(), desc="writing cache ..."):
        sys.stdout.write(json.dumps({
            "key": k,
            "val": v,
        }) + ",\n")