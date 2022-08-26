import warnings
warnings.filterwarnings("ignore")
import argparse
import copy
import fnmatch
import ipaddress
import os
import paramiko
import re
import socket
import subprocess
import yaml
from termcolor import colored

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

def get_devices_params(yaml_files):
    devices_params = list()
    for yaml_file in yaml_files:
        try:
            with open(yaml_file) as yaml_file_handler:
                yaml_dict = yaml.safe_load(yaml_file_handler)
        except FileNotFoundError:
            print("Couldn't find file '" + yaml_file + "'!")
            continue
        for device_id in yaml_dict.keys():
            if not re.search("^ap[0-9]{1,2}$|^aerohive_sw[0-9]{1,2}$|^netelem[0-9]{1,2}$|^router[0-9]{1,2}$|"
                             "^wing[0-9]{1,2}$|^mu[0-9]{1,2}$|^(a3|inband|kali|radius|tftp)_server[0-9]{1,2}$", device_id):
                continue
            device_dict = yaml_dict.get(device_id)
            device_params = dict()
            device_params['yaml_file'] = yaml_file
            device_params['device'] = device_id
            try:
                device_keys = device_dict.keys()
            except AttributeError:
                error_message = "Device has no parameters configured"
                log_error('parse', error_message, device_params)
                continue
            for device_key in ['name', 'ip', 'port', 'connection_method', 'username', 'password']:
                device_key_value = str(device_dict.get(device_key)).strip()
                if device_key_value not in ['None', '']:
                    if device_key == 'ip':
                        try:
                            ipaddress.ip_address(device_key_value)
                        except ValueError:
                            error_message = "Invalid value for the 'ip' parameter: '" + device_key_value+ "'"
                            log_error('parse', error_message, device_params)
                            continue
                    if device_key == 'port':
                        invalid_port_value = False
                        try:
                            if int(device_key_value) != 22:
                                invalid_port_value = True
                        except ValueError:
                            invalid_port_value = True
                        if invalid_port_value:
                            error_message = "Invalid value for the 'port' parameter: '" +\
                                            device_key_value + "' (expected '22')"
                            log_error('parse', error_message, device_params)
                            continue
                    if device_key == 'connection_method':
                        if device_key_value != 'ssh':
                            error_message = "Invalid value for the 'connection_method' parameter: '" +\
                                            device_key_value + "' (expected 'ssh')"
                            log_error('parse', error_message, device_params)
                            continue
                    device_params[device_key] = device_key_value
                else:
                    log_error_flag = True
                    if device_key == 'password' and device_key_value == '':
                        device_params['password'] = ''
                        log_error_flag = False
                    if device_key == 'connection_method' and device_key_value == 'None':
                        log_error_flag = False
                    if log_error_flag:
                        error_message = "Parameter '" + device_key + "' is not configured"
                        log_error('parse', error_message, device_params)
            if device_params.get('ip') and device_params.get('port'):
                devices_params.append(device_params)
    return devices_params

def ping(ip_address, pkt_count=3, timeout=10):
    command = ['ping', '-c', str(pkt_count), '-w', str(timeout), ip_address]
    result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return (result.returncode == 0)

def log_error(error_type, error_message, device_params):
    device_params['error_type'] = error_type
    device_params['error_message'] = error_message
    errors.append(copy.deepcopy(device_params))

def print_errors(args, errors):
    if not errors:
        return
    print()
    error_types = ['parse', 'ping', 'ssh']
    if args.parse_only:
        error_types = ['parse']
    if args.ping_only:
        error_types = ['parse', 'ping']
    for error_type in error_types:
        error_type_items = list()
        for error in errors:
            if error.get('error_type') == error_type:
                error_type_items.append(error)
        print("=== " + error_type.upper() + " Errors (" + str(len(error_type_items)) + ") ===\n")
        for error_type_item in error_type_items:
            for error_type_item_key in ['yaml_file', 'device', 'name', 'ip', 'port', 'username', 'password', 'error_message']:
                if error_type_item_key in error_type_item.keys():
                    print(str(error_type_item_key) + ': ' + str(error_type_item.get(error_type_item_key)))
            print()

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers(dest='command')

        get_sites_parser = subparser.add_parser("get-sites", help="list the available testbeds sites")
        get_sites_parser.add_argument("--tb-dir", action='store', help="absolute path of the testbeds directory")

        get_yaml_dirs_parser = subparser.add_parser("get-yaml-dirs", help="list the available yaml directories for a given site")
        get_yaml_dirs_parser.add_argument("--tb-dir", action='store', help="absolute path of the testbeds directory")
        get_yaml_dirs_parser.add_argument("--site", action='store', help="name of the testbeds site (e.g. 'SJ')")

        get_yaml_files_parser = subparser.add_parser("get-yaml-files", help="list the available yaml files for a given site or yaml directory")
        get_yaml_files_parser.add_argument("--tb-dir", action='store', help="absolute path of the testbeds directory")
        get_yaml_files_parser.add_argument("--site", action='store', help="name of the testbeds site (e.g. 'SJ')")
        get_yaml_files_parser.add_argument("--yaml-dir", action='store', help="relative path of the yaml directory (e.g. 'Prod/wireless')")

        test_parser = subparser.add_parser("test", help="test for yaml parse, ping and SSH errors")
        test_parser.add_argument("--tb-dir", action='store', help="absolute path of the testbeds directory")
        test_parser.add_argument("--site", action='store', help="name of the testbeds site (e.g. 'SJ')")
        test_parser.add_argument("--yaml-dir", action='store', help="relative path of the yaml directory (e.g. 'Prod/wireless')")
        test_parser.add_argument("--yaml-file", action='store', help="absolute path of the yaml file")
        test_parser.add_argument("--parse-only", action='store_true', help="test only for yaml parse errors")
        test_parser.add_argument("--ping-only", action='store_true', help="test only for yaml parse and ping errors")

        args = parser.parse_args()
        tb_dir = args.tb_dir if args.tb_dir else os.path.join(os.path.dirname(os.getcwd()), 'TestBeds')
        if not os.path.isdir(tb_dir):
            print("Invalid path for the testbeds directory '" + tb_dir + "'!")
            exit()
        errors = list()

        if args.command == 'get-sites':
            tb_sites = next(os.walk(tb_dir))[1]
            if 'Templates' in tb_sites:
                tb_sites.remove('Templates')
            for tb_site in tb_sites:
                print(tb_site)

        if args.command == 'get-yaml-dirs':
            if args.site:
                site_root_dir = os.path.join(tb_dir, args.site)
                if not os.path.isdir(site_root_dir):
                    print("Couldn't find directory '" + site_root_dir + "'!")
                    exit()
                os.chdir(site_root_dir)
                site_all_dirs = list()
                for root, dirs, files in os.walk(r'.'):
                    site_all_dirs.append(root)
                site_tb_dirs = list()
                for site_dir in site_all_dirs:
                    os.chdir(os.path.join(site_root_dir + site_dir.lstrip('.')))
                    for root, dirs, files in os.walk(r'.'):
                        for file in files:
                            if os.path.splitext(file)[1] == '.yaml':
                                if site_dir not in site_tb_dirs:
                                    site_tb_dirs.append(site_dir)
                                break
                site_tb_dirs = [dir.replace('./', '') for dir in site_tb_dirs]
                site_tb_dirs.sort()
                if site_tb_dirs:
                    for site_tb_dir in site_tb_dirs:
                        print(site_tb_dir)
                else:
                    print("No yaml directories found!")
            else:
                print("No value for the '--site' argument!")
                exit()

        if args.command == 'get-yaml-files':
            yaml_files = get_yaml_files(args)
            if yaml_files:
                for yaml_file in yaml_files:
                    print(yaml_file)
            else:
                exit()

        if args.command == 'test':
            yaml_files = list()
            if args.site and args.yaml_file:
                print("'--site' and '--yaml-file' are mutually exclusive arguments!")
                exit()
            if args.yaml_dir and args.yaml_file:
                print("--yaml-dir' and '--yaml-file' are mutually exclusive arguments!")
                exit()
            if args.yaml_file:
                yaml_files.append(args.yaml_file)
            else:
                yaml_files = get_yaml_files(args)
            if not yaml_files:
                exit()
            devices_params = get_devices_params(yaml_files)
            if args.parse_only:
                print_errors(args, errors)
                exit()
            if not (args.parse_only or args.ping_only):
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            for device_params in devices_params:
                print()
                for parameter in ['yaml_file', 'device', 'name', 'ip', 'port', 'connection_method', 'username', 'password']:
                    parameter_value = str(device_params.get(parameter))
                    if parameter_value != 'None':
                        print(parameter + ": " + parameter_value)

                ip = str(device_params.get('ip'))
                port = str(device_params.get('port'))
                username = str(device_params.get('username'))
                password = str(device_params.get('password'))
                error = tuple()
                if ping(ip):
                    print(colored("Ping OK :)", 'green'))
                    if not args.ping_only:
                        if 'None' not in [username, password]:
                            try:
                                client.connect(ip, port=22, username=username, password=password, timeout=10,
                                               allow_agent=False, look_for_keys=False)
                                client.close()
                                print(colored("SSH OK :)", 'green'))
                            except paramiko.ssh_exception.BadHostKeyException:
                                error = ('ssh', "SSH NOT OK, device host key could not be verified :(")
                            except paramiko.ssh_exception.AuthenticationException:
                                error = ('ssh', "SSH NOT OK, authentication failed :(")
                            except paramiko.ssh_exception.SSHException:
                                error = ('ssh', "SSH NOT OK, protocol negotiation failed :(")
                            except socket.error:
                                error = ('ssh', "SSH NOT OK, connection timed out :(")
                else:
                    error = ('ping', "Ping NOT OK :(")
                if error:
                    print(colored(error[1], 'red'))
                    log_error(error[0], error[1], device_params)
            print_errors(args, errors)

    except KeyboardInterrupt:
        print('\nKeyboard interrupt!')
        print_errors(args, errors)
        exit()
