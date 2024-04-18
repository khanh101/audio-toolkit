#!/usr/bin/env python
import json
import os
import sys

from tqdm import tqdm

if __name__ == "__main__":
    cache_path = sys.argv[1]
    
    cache = {}
    cache_str = open(self.cache_path).read().rstrip(",\n")
    o_list = json.loads(f"[{cache_str}]")
    for o in o_list:
        cache[o["key"]] = o["val"]
    
    for k, v in cache.items():
        sys.stdout.write(json.dumps({
            "key": k,
            "val": v,
        }) + ",\n")