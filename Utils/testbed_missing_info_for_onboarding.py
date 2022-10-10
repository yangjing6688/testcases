import warnings
warnings.filterwarnings("ignore")
import argparse
import fnmatch
import os
import yaml


def get_yaml_files(args):
    yaml_files_dir = tb_dir
    if args.site:
        yaml_files_dir = os.path.join(tb_dir, args.site)
    if args.yaml_dir:
        if args.site:
            if args.yaml_dir != '.':
                yaml_files_dir = os.path.join(tb_dir, args.site, args.yaml_dir)
        else:
            print("No value for the '--site' argument!")
            return
    yaml_files = list()
    if os.path.isdir(yaml_files_dir):
        for root, dirs, files in os.walk(yaml_files_dir):
            filtered_files = fnmatch.filter(files, "*.yaml")
            yaml_files.extend(os.path.join(root, filtered_file) for filtered_file in filtered_files)
        if yaml_files:
            yaml_files.sort()
        else:
            print("No yaml files found!")
            return
    else:
        print("Couldn't find directory '" + yaml_files_dir + "'!")
        return
    return yaml_files


def get_yaml_content(yaml_file):
    try:
        with open(yaml_file) as yaml_file_handler:
            yaml_dict = yaml.safe_load(yaml_file_handler)
            return yaml_dict
    except FileNotFoundError:
        print("Couldn't find file '" + yaml_file + "'!")

def verify_real_device_params(info, name):
    not_found_param = []
    device_type_real = ["serial", "mac", "make", "location"]
    for param in device_type_real:
        if info.get(param) is None:
            not_found_param.append(param)
    print(f"For {name} we did not find: {not_found_param}")

def verify_simulated_device_params(info, name):
    not_found_param = []
    device_type_simulated = ["model", "simulated_count"]
    for param in device_type_simulated:
        if info.get(param) is None:
            not_found_param.append(param)
    print(f"For {name} we did not find: {not_found_param}")

def verify_digital_device_params(info, name):
    not_found_param = []
    device_type_digital = ["model", "digital_twin_version", "digital_twin_persona"]
    for param in device_type_digital:
        if info.get(param) is None:
            not_found_param.append(param)
    print(f"For {name} we did not find: {not_found_param}")

def verify_device_params(file_info, name):
    for value in file_info.values():
        if type(value) == dict:
            device_type = value.get("onboard_device_type")
            if device_type is None:
                continue
            elif device_type == "Real":
                verify_real_device_params(value, name)
            elif device_type == "Simulated":
                verify_simulated_device_params(value, name)
            elif device_type == "Digital Twin":
                verify_digital_device_params(value, name)
        else:
            continue


if __name__ == "__main__":
    yaml_info = {}
    try:
        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers(dest='command')

        get_yaml_files_parser = subparser.add_parser("get-yaml-files", help="list the available yaml files for a given site or yaml directory")
        get_yaml_files_parser.add_argument("--tb-dir", action='store', help="absolute path of the testbeds directory")
        get_yaml_files_parser.add_argument("--site", action='store', help="name of the testbeds site (e.g. 'SJ')")
        get_yaml_files_parser.add_argument("--yaml-dir", action='store', help="relative path of the yaml directory (e.g. 'Prod/wireless')")

        args = parser.parse_args()
        tb_dir = args.tb_dir if args.tb_dir else os.path.join(os.path.dirname(os.getcwd()), 'TestBeds')
        if not os.path.isdir(tb_dir):
            print("Invalid path for the testbeds directory '" + tb_dir + "'!")
            exit()

        if args.command == 'get-yaml-files':
            yaml_files = get_yaml_files(args)
            if yaml_files:
                for yaml_file in yaml_files:
                    yaml_info = get_yaml_content(yaml_file)
                    # print(yaml_info)
                    verify_device_params(yaml_info, yaml_file)
            else:
                exit()

    except KeyboardInterrupt:
        print('\nKeyboard interrupt!')
        exit()



