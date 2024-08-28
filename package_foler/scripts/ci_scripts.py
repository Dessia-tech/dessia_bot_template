#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excute Scripts.
"""

import os
import time

scripts = ["script_1.py"]

# Testing if all scripts exists before launching them
for script_name in scripts:
    if not os.path.isfile(script_name):
        raise FileNotFoundError(f"Script {script_name} does not exists in CI scripts")

# Executing scripts
print("Executing scripts for CI:")
total_time = time.time()
top_level_dir = os.getcwd()
times = {}
for script_name in scripts:
    print(f"\t* {script_name}")
    # Reset dir
    os.chdir(top_level_dir)
    # Change cwd
    if "/" in script_name:
        script_folder = "/".join(script_name.split("/")[:-1])
        if script_folder:
            script_folder = os.path.join(top_level_dir, script_folder)
            os.chdir(script_folder)
    file_name = script_name.split("/")[-1]
    t = time.time()
    with open(file_name, "r", encoding="utf-8") as script:
        exec(script.read())
    t = time.time() - t
    times[script_name] = t

print("Computation times:")
for script_name, t in sorted(times.items(), key=lambda x: x[1]):
    print(f"* script {script_name}: {round(t, 3)} seconds ")

total_time = time.time() - total_time
print(f"Total time for CI scripts: {total_time}")