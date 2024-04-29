import logging
from Go import Go
import time

start = time.time()

logging.getLogger().setLevel(logging.WARNING)

Go.parse_arguments()

Go.setup_folders()

Go.convert_all()

Go.clean()

total_time = time.time() - start

logging.getLogger().log(f"Time Taken: {round(total_time)}")
