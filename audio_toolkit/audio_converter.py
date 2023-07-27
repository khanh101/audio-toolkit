import subprocess


def convert_to_wav_mono_16k(path_in: str, path_out: str):
    command = ["ffmpeg", "-i", f"\"{path_in}\"",  "-ac", "1", "-ar", "16000", f"\"{path_out}\""]
    p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate()
