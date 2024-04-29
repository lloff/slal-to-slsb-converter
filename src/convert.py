import logging
from Go import Go
import time

start = time.time()

logging.getLogger().setLevel(logging.INFO)

Go.parse_arguments()

Go.setup_folders()

Go.convert_all()

Go.clean()

total_time = time.time() - start

logging.getLogger().info(f"Time Taken: {round(total_time)}")
