"""
Execute specific scripts for CI.
"""

import os
import subprocess
import time

# List of scripts to execute
scripts = [
    "script_1.py",
]

# Testing if all scripts exist before launching them
for script_name in scripts:
    if not os.path.isfile(script_name):
        raise FileNotFoundError(f"Script {script_name} does not exist in CI scripts")

# Executing scripts
print("Executing scripts for CI:")
total_time = time.perf_counter()
top_level_dir = os.getcwd()
times = {}

for script_name in scripts:
    print(f"\t* {script_name}")
    # Reset dir
    os.chdir(top_level_dir)
    # Change cwd if necessary
    if "/" in script_name:
        script_folder = os.path.dirname(script_name)
        if script_folder:
            os.chdir(script_folder)

    # Start the timer
    start_time = time.perf_counter()

    # Run the script using subprocess
    result = subprocess.run(["python3", script_name], check=True, text=True)

    # Stop the timer
    elapsed_time = time.perf_counter() - start_time
    times[script_name] = elapsed_time

print("Computation times:")
for script_name, elapsed_time in sorted(times.items(), key=lambda x: x[1]):
    print(f"* script {script_name}: {round(elapsed_time, 3)} seconds")

total_time = time.perf_counter() - total_time
print(f"Total time for CI scripts: {round(total_time, 3)} seconds")
