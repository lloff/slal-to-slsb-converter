import logging
from Go import Go
import time

start = time.time()

logging.basicConfig(level=logging.INFO)

Go.go()

total_time = time.time() - start

logging.getLogger().info(f"Time Taken: {round(total_time)}")


