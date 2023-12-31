from __future__ import annotations

import contextlib
import json
import os
import struct
import wave
from typing import *

from tqdm import tqdm


def bytes_to_int(bytes: list) -> int:
    result = 0
    for byte in bytes:
        result = (result << 8) + byte
    return result


def get_flac_duration(filename: str) -> Tuple[int, int]:
    """
    Returns the duration of a FLAC file in seconds

    https://xiph.org/flac/format.html
    """
    with open(filename, 'rb') as f:
        if f.read(4) != b'fLaC':
            raise ValueError('File is not a flac file')
        header = f.read(4)
        while len(header):
            meta = struct.unpack('4B', header)  # 4 unsigned chars
            block_type = meta[0] & 0x7f  # 0111 1111
            size = bytes_to_int(header[1:4])

            if block_type == 0:  # Metadata Streaminfo
                streaminfo_header = f.read(size)
                unpacked = struct.unpack('2H3p3p8B16p', streaminfo_header)
                """
                https://xiph.org/flac/format.html#metadata_block_streaminfo

                16 (unsigned short)  | The minimum block size (in samples)
                                       used in the stream.
                16 (unsigned short)  | The maximum block size (in samples)
                                       used in the stream. (Minimum blocksize
                                       == maximum blocksize) implies a
                                       fixed-blocksize stream.
                24 (3 char[])        | The minimum frame size (in bytes) used
                                       in the stream. May be 0 to imply the
                                       value is not known.
                24 (3 char[])        | The maximum frame size (in bytes) used
                                       in the stream. May be 0 to imply the
                                       value is not known.
                20 (8 unsigned char) | Sample rate in Hz. Though 20 bits are
                                       available, the maximum sample rate is
                                       limited by the structure of frame
                                       headers to 655350Hz. Also, a value of 0
                                       is invalid.
                3  (^)               | (number of channels)-1. FLAC supports
                                       from 1 to 8 channels
                5  (^)               | (bits per sample)-1. FLAC supports from
                                       4 to 32 bits per sample. Currently the
                                       reference encoder and decoders only
                                       support up to 24 bits per sample.
                36 (^)               | Total samples in stream. 'Samples'
                                       means inter-channel sample, i.e. one
                                       second of 44.1Khz audio will have 44100
                                       samples regardless of the number of
                                       channels. A value of zero here means
                                       the number of total samples is unknown.
                128 (16 char[])      | MD5 signature of the unencoded audio
                                       data. This allows the decoder to
                                       determine if an error exists in the
                                       audio data even when the error does not
                                       result in an invalid bitstream.
                """

                samplerate = bytes_to_int(unpacked[4:7]) >> 4
                sample_bytes = [(unpacked[7] & 0x0F)] + list(unpacked[8:12])
                total_samples = bytes_to_int(sample_bytes)
                return total_samples, samplerate

            header = f.read(4)


def get_wav_duration(filename: str) -> Tuple[int, int]:
    with contextlib.closing(wave.open(filename, "rb")) as f:
        return f.getnframes(), f.getframerate()


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
                    self.cache[path] = o
        # open file
        self.f = open(self.cache_path, "a")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.opened:
            raise RuntimeError("context cannot be exited without entering")

        self.opened = False
        self.f.close()
        self.f = None

    def get(self, path: str) -> Dict[str, Union[int, float]]:
        if not self.opened:
            raise RuntimeError("read only within context")

        path = os.path.realpath(path)

        if path not in self.cache:
            ext = os.path.splitext(path)[1]
            frame_count, sample_rate = get_duration[ext.lower()](path)

            o = {
                "path": path,
                "frame_count": frame_count,
                "sample_rate": sample_rate,
            }
            self.cache[path] = o
            self.f.write(json.dumps(o) + "\n")

        return self.cache[path]
