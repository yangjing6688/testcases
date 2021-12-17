import argparse
from collections import abc
from sys import exit
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("file", help="File that contains the list of testbed yaml files", type=str)
args = parser.parse_args()

# Comment to test without the need to read in a list of files from a file
try:
    with open(args.file, "r") as f:
        list_of_testbed_files = f.read().strip()
except Exception as e:
    raise Exception('The CI script encountered a problem.') from e

list_of_testbed_files = list_of_testbed_files.split(",") if list_of_testbed_files else  []

# Uncomment to test without the need to read in a list of files from a file
# list_of_testbed_files = ["TestBeds\\RDU\\Dev\\rdu_x590_pod5_3node.yam", "TestBeds\\RDU\\Dev\\rdu_x690_stk_pod1_3node.yaml"]

rc=0

# yields every key from a nested dict
def nested_dict_iter(nested):
    for key, value in nested.items():
        if isinstance(value, abc.Mapping):
            yield from nested_dict_iter(value)
        else:
            yield key

def find_bad_keys(file):
    global rc
    try:
        with open(file, "r") as stream:
            testbed_file = yaml.safe_load(stream)
            # print(testbed_file)
    except Exception as e:
        print(f"[*] FAIL: {file} failed! Unable to load Testbed YAML file. Exception: {e}")
        rc=1
        return

    yaml_reader = nested_dict_iter(testbed_file)

    offending_keys = []
    for key in yaml_reader:
        if not key.islower():
            offending_keys.append(key)

    if offending_keys:
        print(f"[*] FAIL: {file} failed! Uppercase keys found.")
        print(f"[**] Offending keys: {offending_keys}")
        rc=1
    else:
        print(f"[*] PASS: {file} passed!")

if list_of_testbed_files:
    for file in list_of_testbed_files:
        find_bad_keys(file)
        print()
else:
    print("[*] No testbed files found. Skipping these tests...")

exit(rc)
