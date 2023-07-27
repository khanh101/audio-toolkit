from __future__ import annotations

import contextlib
import wave
from typing import *


def get_wav_duration(filename: str) -> Tuple[int, int]:
    with contextlib.closing(wave.open(filename, "rb")) as f:
        return f.getnframes(), f.getframerate()
