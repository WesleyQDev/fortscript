import time


def test_loop():
    """Simple loop that prints a test message every 5 seconds."""
    while True:
        print("Running test")
        time.sleep(5)


if __name__ == "__main__":
    test_loop()
