from audio_toolkit import StatsReader

if __name__ == "__main__":
    with StatsReader() as reader:
        o = reader.read("test.wav")
        print(o)