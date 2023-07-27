from audio_toolkit import AudioStats

if __name__ == "__main__":
    with AudioStats() as audio_stats:
        o = audio_stats.get("test.wav")
        print(o)