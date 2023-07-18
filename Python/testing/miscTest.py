import time

def wait(sleepTime: int) -> None:
        """ A function to precisly wait a given time in seconds."""
        initial = time.time()
        x = 1
        while time.time() - initial < sleepTime:
            x += 1


print(1)
wait(1)
print(2)