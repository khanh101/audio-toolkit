from audio_toolkit import AudioStats

if __name__ == "__main__":
    with AudioStats() as stats:
        o = stats.get("test.wav")
        print(o)
