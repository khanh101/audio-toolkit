#!/usr/bin/env python
import json
import os

from tqdm import tqdm

if __name__ == "__main__":
    cache_path = "/tmp/persistent_dict.json"
    
    cache = {}
    cache_str = open(self.cache_path).read().rstrip(",\n")
    o_list = json.loads(f"[{cache_str}]")
    for o in o_list:
        cache[o["key"]] = o["val"]
    
    with open(cache_path, "w") as f:
        for k, v in cache.items():
            f.write(json.dumps({
                "key": k,
                "val": v,
            }) + ",\n")