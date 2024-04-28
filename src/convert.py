from Go import Go
import time

start = time.time()

Go.parse_arguments()

Go.setup_folders()

Go.convert_all()

Go.clean()

total_time = time.time() - start

print(f"Time Taken: {round(total_time)}")
