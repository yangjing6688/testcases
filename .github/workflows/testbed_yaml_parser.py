from argparse import ArgumentParser
from collections import abc
from re import compile, fullmatch, VERBOSE, IGNORECASE
from sys import exit
from yaml import safe_load as safe_load_yaml

parser = ArgumentParser()
parser.add_argument("file", help="File that contains the list of testbed yaml files", type=str)
parser.add_argument('--warn', help="Don't return a bad return code. Only print problems.", action='store_true')
args = parser.parse_args()

# Comment to test without the need to read in a list of files from a file

try:
    with open(args.file, "r") as f:
        list_of_testbed_files = f.read().strip()
except Exception as e:
    raise Exception('The CI script encountered a problem.') from e

list_of_testbed_files = list_of_testbed_files.split(",") if list_of_testbed_files else  []
# End comment here --------------------

# Uncomment to test without the need to read in a list of files from a file
# list_of_testbed_files = ["TestBeds\RDU\Dev\\rdu_x590_pod5_3node.yam", "TestBeds\BANGALORE\Prod\\testbed2.yaml"]

rc=0
# VALID_MAKES = ["Controllers", "Extreme - Aerohive", "VOSS", "EXOS", "Dell", "Universal Appliance", "XMC"]
# XMC MAKES = [A10, APC, Advantage, Albis, Allied Telesyn, Apple, Avaya, Broadcom, Brocade, Cannon, Cisco, Clickarray, D-Link, Dell, Extreme, HP, IBM, Intel, Juniper, KCP, Konica, Lantronix, Microsoft, NetSNMP, Nokia, Oracle, Packeteer, Palo Alto, Panasonic, RuggedCom, SNMP Research, Siemens, Sigma, Sonus, UCD, UNIX, VMware, Xerox]
VALID_MAKES_REGEX = compile(r"Controllers|Extreme - Aerohive|VOSS|EXOS|Dell|Universal Appliance|XMC|A10|APC|Advantage|Albis|Allied Telesyn|Apple|Avaya|Broadcom|Brocade|Cannon|Cisco|Clickarray|D-Link|Dell|Extreme|HP|IBM|Intel|Juniper|KCP|Konica|Lantronix|Microsoft|NetSNMP|Nokia|Oracle|Packeteer|Palo Alto|Panasonic|RuggedCom|SNMP Research|Siemens|Sigma|Sonus|UCD|UNIX|VMware|Xerox", IGNORECASE)
VALID_TOP_LEVEL_KEYS = [r"ap[0-9]+", r"netelem[0-9]+", r"mu[0-9]+", r"mails", r"lab", r"tgen[0-9]+", r"tgen_ports", r"a3server[0-9]+", r"endsys[0-9]+", r"kali[0-9]+", r"nettools_fpp[0-9]+", r"radius[0-9]*"]
VALID_TOP_LEVEL_KEYS_REGEX = compile( "|".join(VALID_TOP_LEVEL_KEYS) )
# DEVICES_WITH_MAKE = ["ap", "netelem"]
APS_NETELEMS = compile(r"ap[0-9]+|netelem[0-9]+")
VALID_LOCATIONS = compile(r"""
                            auto_location_01,San Jose,building_01,floor_01
                            |auto_location_01,San Jose,building_01,floor_02
                            |auto_location_01,Santa Clara,building_02,floor_03
                            |auto_location_01,Santa Clara,building_02,floor_04
                            """, VERBOSE)

WARN_PREFIX="[*] WARNING: "
FAIL_PREFIX="[*] FAIL: "
LINE_BREAK="-" * 10

print_prefix = WARN_PREFIX if args.warn else FAIL_PREFIX


# yields every key from a nested dict
def nested_dict_iter(nested):
    for key, value in nested.items():
        if isinstance(value, abc.Mapping):
            yield from nested_dict_iter(value)
        else:
            yield key

def find_bad_keys(file):
    yaml_reader = nested_dict_iter(file)

    bad_keys = []
    for key in yaml_reader:
        if not key.islower():
            bad_keys.append(key)

    return bad_keys

if list_of_testbed_files:
    for file_path in list_of_testbed_files:
        file_passed = True
        # Read in testbed yaml file
        try:
            with open(file_path, "r") as stream:
                testbed_file = safe_load_yaml(stream)
                print(f"{LINE_BREAK} Checking file: {file_path}. {LINE_BREAK}", end='\n\n')
        except Exception as e:
            print(f"{print_prefix}{file_path} failed! Unable to load Testbed YAML file. Exception: {e}", end='\n\n')
            rc=1
            continue

        # Look for uppercase or otherwise bad keys in yaml
        #
        keys_bad = find_bad_keys(testbed_file)

        keys_missing_model = []
        keys_bad_make = []
        keys_invalid_name = []
        for top_level_key in testbed_file:
            # Invalid top-level keys check
            #
            if not fullmatch(VALID_TOP_LEVEL_KEYS_REGEX, top_level_key):
                keys_invalid_name.append(top_level_key)
                # Skip other tests. We don't know what tests to run because key is invalid
                continue

            # print(f"Key: {top_level_key}, Val: {testbed_file[top_level_key]}")

            # Make, Model, and Location checks
            #
            if fullmatch(APS_NETELEMS, top_level_key):
                if not isinstance(testbed_file[top_level_key].get("model", None), str):
                    keys_missing_model.append(top_level_key)

                make = testbed_file[top_level_key].get("make", "")
                if not fullmatch(VALID_MAKES_REGEX, make):
                    keys_bad_make.append(top_level_key)

        # Print file results
        #
        if keys_bad:
            print(f"{print_prefix}{file_path} failed! Uppercase keys found.")
            print(f"[**] Offending keys: {keys_bad}", end='\n\n')

        if keys_missing_model:
            print(f"{print_prefix}{file_path} failed! One or more network elements do not contain a valid 'model' value.")
            print(f"[**] Offending network elements: {keys_missing_model}")
            print(f"[**] model must be a string.", end='\n\n')

        if keys_bad_make:
            print(f"{print_prefix}{file_path} failed! One or more network elements do not contain a valid 'make' value.")
            print(f"[**] Offending network elements: {keys_bad_make}")
            print(f"[**] Valid make values: {VALID_MAKES_REGEX.pattern.split('|')}.", end='\n\n')

        if keys_invalid_name:
            print(f"{print_prefix}{file_path} failed! One or more invalid top-level keys found.")
            print(f"[**] Offending keys: {keys_invalid_name}")
            print(f"[**] Valid top-level keys: {VALID_TOP_LEVEL_KEYS}.", end='\n\n')

        if keys_bad or keys_missing_model or keys_bad_make or keys_invalid_name:
            file_passed = False
            rc=1

        if file_passed:
            print(f"[*] PASS: {file_path} passed!")

        print() # Add blank line between files

else:
    print("[*] No testbed files found. Skipping these tests...")

if args.warn:
    rc=0
exit(rc)
